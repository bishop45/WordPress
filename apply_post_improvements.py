"""
WordPress ブログ記事の改善を自動適用するスクリプト
Phase 2.3 拡張: メタディスクリプション、画像、内部リンク、まとめセクションの自動追加
"""

import os
import re
import csv
import sys
import glob
import time
import argparse
from datetime import datetime

import requests
import html as html_module
from dotenv import load_dotenv
from bs4 import BeautifulSoup


def load_config():
    """環境変数から設定を読み込む"""
    load_dotenv()

    required_vars = [
        "WORDPRESS_URL",
        "WORDPRESS_USERNAME",
        "WORDPRESS_APPLICATION_PASSWORD",
    ]
    config = {}
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            print(f"エラー: 環境変数 {var} が設定されていません。")
            sys.exit(1)
        config[var] = value

    return config


def get_all_posts(config):
    """WordPress REST APIで全記事を取得する"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/posts"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    all_posts = []
    page = 1

    print("WordPress記事を取得中...")
    while True:
        params = {"per_page": 100, "page": page, "status": "publish"}
        response = requests.get(url, params=params, auth=auth)

        if response.status_code != 200:
            if page == 1:
                print(f"エラー: 記事の取得に失敗しました (HTTP {response.status_code})")
                print(f"レスポンス: {response.text[:200]}")
                sys.exit(1)
            break

        posts = response.json()
        if not posts:
            break

        all_posts.extend(posts)
        total_pages = int(response.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1

    print(f"取得完了: {len(all_posts)}記事\n")
    return all_posts


def get_single_post(post_id, config):
    """特定の記事を取得"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/posts/{post_id}"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    response = requests.get(url, params={'context': 'edit'}, auth=auth)

    if response.status_code != 200:
        print(f"エラー: 記事ID {post_id} の取得に失敗しました (HTTP {response.status_code})")
        sys.exit(1)

    return response.json()


def clean_text(text):
    """HTMLエンティティ除去、改行・空白正規化"""
    text = html_module.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)  # HTMLタグ除去
    text = re.sub(r'\s+', ' ', text).strip()  # 空白正規化
    return text


def update_post_content(post_id, new_content, config):
    """WordPress記事のコンテンツを更新"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/posts/{post_id}"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    payload = {
        "content": new_content
    }

    response = requests.post(url, json=payload, auth=auth)

    if response.status_code != 200:
        raise Exception(f"記事更新失敗 (HTTP {response.status_code}): {response.text[:200]}")

    return response.json()


# =============================================================================
# メタディスクリプション関連
# =============================================================================

def generate_meta_description(post):
    """記事からメタディスクリプションを生成（120-160文字）"""
    html_content = post['content']['rendered']
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. 最初の段落を抽出（pタグ）
    first_paragraphs = soup.find_all('p', limit=3)
    text = ''
    for p in first_paragraphs:
        p_text = p.get_text().strip()
        if len(p_text) > 20:  # 短すぎる段落をスキップ
            text = p_text
            break

    # 2. テキストが取得できない場合は見出し（h2）を使用
    if not text:
        h2 = soup.find('h2')
        if h2:
            text = h2.get_text().strip()

    # 3. それでもない場合はタイトルを使用
    if not text:
        text = html_module.unescape(post['title']['rendered'])

    # 4. HTMLエンティティ除去、改行削除
    text = clean_text(text)

    # 5. 120-160文字に調整
    # 理想は130-150文字
    if len(text) > 160:
        # 文の切れ目で切る（句点、！、？で探す）
        cut_points = [i for i, c in enumerate(text[:160]) if c in '。！？']
        if cut_points:
            text = text[:cut_points[-1] + 1]
        else:
            text = text[:157] + '...'
    elif len(text) < 120:
        # 120文字未満の場合は、次の段落も追加
        for p in first_paragraphs[1:]:
            additional = clean_text(p.get_text())
            if len(text) + len(additional) + 1 <= 160:
                text += ' ' + additional
            else:
                # 160文字を超えないように調整
                remaining = 160 - len(text) - 1
                if remaining > 20:
                    text += ' ' + additional[:remaining - 3] + '...'
                break

    return text


def set_meta_description(post_id, meta_desc, config):
    """Yoast SEOのメタディスクリプションを設定"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/posts/{post_id}"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    # metaフィールドを更新
    payload = {
        "meta": {
            "_yoast_wpseo_metadesc": meta_desc
        }
    }

    response = requests.post(url, json=payload, auth=auth)

    if response.status_code != 200:
        raise Exception(f"メタディスクリプション設定失敗 (HTTP {response.status_code}): {response.text[:200]}")

    return response.json()


# =============================================================================
# まとめセクション関連
# =============================================================================

def generate_summary_section(post):
    """記事の見出しから「まとめ」セクションを生成"""
    html_content = post['content']['rendered']
    soup = BeautifulSoup(html_content, 'html.parser')

    # 見出し（h2, h3）を取得
    headings = soup.find_all(['h2', 'h3'])

    # 「まとめ」「結論」などのキーワードを含む見出しは除外
    summary_keywords = ['まとめ', '結論', '要約', 'ポイント', '総括']
    content_headings = [
        h for h in headings
        if not any(kw in h.get_text() for kw in summary_keywords)
    ]

    if len(content_headings) < 2:
        # 見出しが少ない場合は段落から抽出
        paragraphs = soup.find_all('p', limit=5)
        summary_items = [
            p.get_text().strip()[:100] + ('...' if len(p.get_text().strip()) > 100 else '')
            for p in paragraphs if len(p.get_text().strip()) > 50
        ][:3]
    else:
        # 見出しテキストをリスト化（最大5件）
        summary_items = [h.get_text().strip() for h in content_headings[:5]]

    return summary_items


def insert_summary_section(html_content, summary_items):
    """まとめセクションを本文最後に挿入"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # まとめセクション作成
    summary_div = soup.new_tag('div', attrs={'class': 'summary-section'})

    # 見出し
    h2 = soup.new_tag('h2')
    h2.string = 'まとめ'
    summary_div.append(h2)

    # 箇条書きリスト
    ul = soup.new_tag('ul')
    for item in summary_items:
        li = soup.new_tag('li')
        li.string = item
        ul.append(li)
    summary_div.append(ul)

    # 本文の最後に挿入（既存のまとめがない場合のみ）
    existing_summary = soup.find(['h2', 'h3'], string=lambda t: t and any(kw in t for kw in ['まとめ', '結論']))
    if not existing_summary:
        # 最後の要素を探す
        last_elements = soup.find_all(['p', 'div', 'ul', 'ol'])
        if last_elements:
            last_elements[-1].insert_after(summary_div)
        else:
            # 要素が見つからない場合はsoupに直接追加
            soup.append(summary_div)

    return str(soup)


def add_summary_to_post(post, config, dry_run=False):
    """記事にまとめセクションを追加"""
    # 既にまとめがある場合はスキップ
    html_content = post['content']['rendered']
    soup = BeautifulSoup(html_content, 'html.parser')
    summary_keywords = ['まとめ', '結論', '要約', 'ポイント', '総括']
    existing_summary = soup.find(['h2', 'h3'], string=lambda t: t and any(kw in t for kw in summary_keywords))

    if existing_summary:
        return False, "既にまとめセクションが存在します"

    # まとめ生成
    summary_items = generate_summary_section(post)

    if not summary_items:
        return False, "まとめ項目を生成できませんでした"

    # HTML挿入
    new_content = insert_summary_section(html_content, summary_items)

    # WordPress更新
    if not dry_run:
        update_post_content(post['id'], new_content, config)

    return True, f"まとめセクション追加（{len(summary_items)}項目）"


# =============================================================================
# 内部リンク関連
# =============================================================================

def load_internal_link_suggestions(csv_path):
    """内部リンク提案CSVを読み込み"""
    suggestions = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            source_id = int(row['記事ID'])
            if source_id not in suggestions:
                suggestions[source_id] = []

            suggestions[source_id].append({
                'target_id': int(row['提案リンク先ID']),
                'target_title': row['提案リンク先タイトル'],
                'target_url': row['提案リンク先URL'],
                'similarity': float(row['類似度スコア']),
                'keywords': row['共通キーワード']
            })

    return suggestions


def insert_internal_links(html_content, link_suggestions, max_links=5):
    """HTMLコンテンツに内部リンクを挿入"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # 類似度でソート（高い順）
    sorted_links = sorted(link_suggestions, key=lambda x: x['similarity'], reverse=True)[:max_links]

    # 「関連記事」セクションを最後に追加
    related_section = soup.new_tag('div', attrs={'class': 'related-articles'})
    heading = soup.new_tag('h2')
    heading.string = '関連記事'
    related_section.append(heading)

    ul = soup.new_tag('ul')
    for link in sorted_links[:min(5, len(sorted_links))]:  # 最大5件をリストに追加
        li = soup.new_tag('li')
        a = soup.new_tag('a', href=link['target_url'])
        a.string = link['target_title']
        li.append(a)
        ul.append(li)

    related_section.append(ul)

    # 本文の最後に挿入
    last_elements = soup.find_all(['p', 'div', 'ul', 'ol'])
    if last_elements:
        last_elements[-1].insert_after(related_section)
    else:
        soup.append(related_section)

    return str(soup)


def add_internal_links_to_post(post, suggestions_dict, max_links, config, dry_run=False):
    """記事に内部リンクを追加"""
    post_id = post['id']

    if post_id not in suggestions_dict:
        return False, f"記事ID {post_id} の内部リンク提案がありません"

    link_suggestions = suggestions_dict[post_id]

    if not link_suggestions:
        return False, "内部リンク候補がありません"

    html_content = post['content']['rendered']

    # リンク挿入
    new_content = insert_internal_links(html_content, link_suggestions, max_links)

    # WordPress更新
    if not dry_run:
        update_post_content(post_id, new_content, config)

    return True, f"内部リンク追加（{min(len(link_suggestions), max_links)}個）"


# =============================================================================
# メイン処理
# =============================================================================

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='WordPress記事の改善を自動適用')
    parser.add_argument('--mode', choices=['meta-desc', 'summary', 'links', 'all'],
                        default='all', help='実行モード')
    parser.add_argument('--post-id', type=int, help='特定の記事IDのみ処理')
    parser.add_argument('--dry-run', action='store_true', help='実際に更新せず確認のみ')
    parser.add_argument('--max-links', type=int, default=5, help='追加する内部リンク数')

    args = parser.parse_args()

    # 設定読み込み
    config = load_config()

    # 内部リンク提案読み込み（linksモードの場合）
    suggestions_dict = None
    if args.mode in ['links', 'all']:
        csv_files = glob.glob('reports/internal_link_suggestions_*.csv')
        if csv_files:
            latest_csv = sorted(csv_files)[-1]
            print(f"内部リンク提案CSV読み込み: {latest_csv}")
            suggestions_dict = load_internal_link_suggestions(latest_csv)
            print(f"  {len(suggestions_dict)}記事分の提案を読み込みました\n")
        else:
            print("警告: 内部リンク提案CSVが見つかりません")
            print("  先に 'python improve_post_structure.py --mode suggest-links' を実行してください\n")
            if args.mode == 'links':
                sys.exit(1)

    # 記事取得
    if args.post_id:
        posts = [get_single_post(args.post_id, config)]
    else:
        posts = get_all_posts(config)

    print(f"処理対象: {len(posts)}記事")
    if args.dry_run:
        print("【DRY RUN モード】実際には更新しません\n")

    # 処理実行
    success_count = 0
    fail_count = 0

    for i, post in enumerate(posts, 1):
        title = html_module.unescape(post['title']['rendered'])[:50]
        print(f"\n[{i}/{len(posts)}] 「{title}...」")

        post_success = True

        try:
            # モード別処理
            if args.mode in ['meta-desc', 'all']:
                print("  [1/3] メタディスクリプション設定... ", end="", flush=True)
                meta_desc = generate_meta_description(post)
                print(f"{len(meta_desc)}文字")
                if args.dry_run:
                    print(f"        プレビュー: {meta_desc[:80]}...")
                else:
                    set_meta_description(post['id'], meta_desc, config)
                    print("        ✅ 設定完了")

            if args.mode in ['summary', 'all']:
                print("  [2/3] まとめセクション追加... ", end="", flush=True)
                success, message = add_summary_to_post(post, config, args.dry_run)
                if success:
                    print(f"✅ {message}")
                else:
                    print(f"⚠️ {message}")

            if args.mode in ['links', 'all']:
                print(f"  [3/3] 内部リンク追加（最大{args.max_links}個）... ", end="", flush=True)
                if suggestions_dict:
                    success, message = add_internal_links_to_post(post, suggestions_dict, args.max_links, config, args.dry_run)
                    if success:
                        print(f"✅ {message}")
                    else:
                        print(f"⚠️ {message}")
                else:
                    print("⚠️ スキップ（CSV未読み込み）")

            success_count += 1

            # レート制限対策の待機
            time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n中断されました。")
            break
        except Exception as e:
            print(f"  ❌ 失敗: {e}")
            fail_count += 1
            post_success = False

    # サマリー
    print(f"\n{'='*60}")
    print("処理完了！")
    print(f"  成功: {success_count}記事")
    print(f"  失敗: {fail_count}記事")
    if args.dry_run:
        print("  ※ DRY RUNモードのため、実際には更新されていません")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
