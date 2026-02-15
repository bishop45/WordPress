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
import random
import argparse
from datetime import datetime

import requests
import html as html_module
from dotenv import load_dotenv
from bs4 import BeautifulSoup


# Unsplash画像検索用のキーワードマッピング
JAPANESE_KEYWORD_MAP = {
    "AI": "artificial intelligence",
    "DX": "digital transformation",
    "セキュリティ": "security",
    "データ": "data",
    "クラウド": "cloud computing",
    "プログラミング": "programming",
    "アプリ": "application",
}

FALLBACK_KEYWORDS = ["technology", "computer", "digital", "workspace", "coding"]


def load_config():
    """環境変数から設定を読み込む"""
    load_dotenv()

    required_vars = [
        "WORDPRESS_URL",
        "WORDPRESS_USERNAME",
        "WORDPRESS_APPLICATION_PASSWORD",
    ]

    # Unsplash API Key（画像追加モード時のみ必須）
    optional_vars = ["UNSPLASH_ACCESS_KEY"]

    config = {}
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            print(f"エラー: 環境変数 {var} が設定されていません。")
            sys.exit(1)
        config[var] = value

    # オプション環境変数
    for var in optional_vars:
        value = os.getenv(var)
        if value:
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
    """All in One SEO (AIOSEO)のメタディスクリプションを設定"""
    url = f"{config['WORDPRESS_URL']}/wp-json/aioseo/v1/post"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    # AIOSEO API用のペイロード
    payload = {
        "id": post_id,
        "description": meta_desc
    }

    response = requests.post(url, json=payload, auth=auth)

    if response.status_code != 200:
        raise Exception(f"メタディスクリプション設定失敗 (HTTP {response.status_code}): {response.text[:200]}")

    result = response.json()
    if not result.get('success'):
        raise Exception(f"AIOSEO API エラー: {result.get('message', 'Unknown error')}")

    return result


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
# 画像追加関連
# =============================================================================

def extract_keywords(title):
    """記事タイトルから検索キーワードを抽出する"""
    # 1. ASCII英単語を抽出（2文字以上）
    english_words = re.findall(r"[A-Za-z]{2,}", title)
    # 一般的すぎる単語を除外
    stop_words = {"the", "and", "for", "with", "how", "what", "why", "can", "not", "you", "are", "its"}
    english_words = [w for w in english_words if w.lower() not in stop_words]

    # 2. 日本語キーワードマッピングからマッチを探す
    mapped_keywords = []
    for jp_word, en_word in JAPANESE_KEYWORD_MAP.items():
        if jp_word in title:
            mapped_keywords.append(en_word)

    # 3. キーワードを組み合わせる
    keywords = english_words + mapped_keywords

    if keywords:
        # 最大3キーワードを使用
        return " ".join(keywords[:3])

    # 4. フォールバック
    return random.choice(FALLBACK_KEYWORDS)


def search_unsplash_image(query, config):
    """Unsplash APIで画像を検索する。レート制限情報も返す。"""
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {config['UNSPLASH_ACCESS_KEY']}"}
    params = {"query": query, "per_page": 1, "orientation": "landscape"}

    response = requests.get(url, headers=headers, params=params)

    rate_remaining = int(response.headers.get("X-Ratelimit-Remaining", 50))

    if response.status_code != 200:
        return None, rate_remaining

    data = response.json()
    if data["total"] == 0 or not data["results"]:
        return None, rate_remaining

    photo = data["results"][0]
    return {
        "url": photo["urls"]["regular"],
        "download_location": photo["links"]["download_location"],
        "description": photo.get("description") or photo.get("alt_description") or query,
        "photographer": photo["user"]["name"],
    }, rate_remaining


def trigger_unsplash_download(download_location, config):
    """Unsplash利用規約に従いダウンロードをトリガーする"""
    headers = {"Authorization": f"Client-ID {config['UNSPLASH_ACCESS_KEY']}"}
    requests.get(download_location, headers=headers)


def download_image(image_url):
    """画像をダウンロードしてバイトデータを返す"""
    response = requests.get(image_url, timeout=30)
    response.raise_for_status()
    return response.content


def upload_to_wordpress(image_data, filename, alt_text, config):
    """WordPressメディアライブラリに画像をアップロードする"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/media"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    files = {
        "file": (filename, image_data, "image/jpeg"),
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; WP-Script/1.0)",
    }

    response = requests.post(url, headers=headers, files=files, auth=auth)

    if response.status_code not in (200, 201):
        raise Exception(f"メディアアップロード失敗 (HTTP {response.status_code}): {response.text[:200]}")

    media = response.json()

    # alt_textを設定
    update_url = f"{url}/{media['id']}"
    requests.post(update_url, json={"alt_text": alt_text}, auth=auth)

    return media["id"], media["source_url"]


def insert_images_into_content(html_content, images, post_title):
    """HTMLコンテンツに画像を挿入（h2見出しの後に均等配置）"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # h2見出しを取得
    h2_headings = soup.find_all('h2')

    if not h2_headings:
        # h2がない場合はpタグの後に挿入
        paragraphs = soup.find_all('p')
        if len(paragraphs) < 2:
            return html_content  # 挿入できる場所がない
        insert_positions = paragraphs[:len(images)]
    else:
        # 画像を均等配置する位置を決定
        num_images = len(images)
        num_h2 = len(h2_headings)

        if num_images == 1:
            insert_positions = [h2_headings[0]]
        elif num_images == 2:
            insert_positions = [h2_headings[0], h2_headings[-1] if num_h2 > 1 else h2_headings[0]]
        else:  # 3枚以上
            if num_h2 < 3:
                # h2が少ない場合は最初と最後
                insert_positions = [h2_headings[0], h2_headings[-1] if num_h2 > 1 else h2_headings[0], h2_headings[-1] if num_h2 > 1 else h2_headings[0]][:num_images]
            else:
                # h2が3つ以上ある場合は均等配置
                step = num_h2 // num_images
                insert_positions = [h2_headings[i * step] for i in range(num_images)]

    # 画像を挿入（後ろから挿入して位置ズレ防止）
    for position, image_info in zip(reversed(insert_positions), reversed(images)):
        figure = soup.new_tag('figure', attrs={'class': 'wp-block-image'})
        img_tag = soup.new_tag('img', src=image_info['url'], alt=image_info['alt'])
        figure.append(img_tag)

        # クレジット表記
        figcaption = soup.new_tag('figcaption')
        figcaption.string = f"Photo by {image_info['photographer']} on Unsplash"
        figure.append(figcaption)

        position.insert_after(figure)

    return str(soup)


def add_images_to_post(post, max_images, config, dry_run=False):
    """記事に画像を追加"""
    if 'UNSPLASH_ACCESS_KEY' not in config:
        return False, "Unsplash APIキーが設定されていません"

    title = html_module.unescape(post['title']['rendered'])
    html_content = post['content']['rendered']

    # キーワード抽出
    keyword = extract_keywords(title)

    # 画像検索（複数枚）
    images_to_insert = []
    rate_remaining = 50

    for i in range(max_images):
        # Unsplashで画像検索
        image_info, rate_remaining = search_unsplash_image(keyword, config)

        # 見つからなければフォールバックキーワードで再検索
        if image_info is None:
            fallback = random.choice(FALLBACK_KEYWORDS)
            image_info, rate_remaining = search_unsplash_image(fallback, config)

        if image_info is None:
            break  # これ以上画像が見つからない

        if not dry_run:
            # Unsplashダウンロードトリガー（利用規約準拠）
            trigger_unsplash_download(image_info["download_location"], config)

            # 画像ダウンロード
            image_data = download_image(image_info["url"])

            # WordPressにアップロード
            filename = f"article-{post['id']}-image-{i+1}.jpg"
            alt_text = f"{title} - {image_info['description']}"
            media_id, source_url = upload_to_wordpress(image_data, filename, alt_text, config)

            images_to_insert.append({
                'url': source_url,
                'alt': alt_text,
                'photographer': image_info['photographer']
            })
        else:
            # DRY RUNモードでは画像情報のみ記録
            images_to_insert.append({
                'url': image_info['url'],
                'alt': f"{title} - {image_info['description']}",
                'photographer': image_info['photographer']
            })

        # レート制限チェック
        if rate_remaining <= 5:
            print(f"\n        ⚠️ Unsplash APIレート制限に近づいています（残り{rate_remaining}）")
            break

        time.sleep(0.5)  # API負荷軽減

    if not images_to_insert:
        return False, "画像が見つかりませんでした"

    # HTML挿入
    new_content = insert_images_into_content(html_content, images_to_insert, title)

    # WordPress更新
    if not dry_run:
        update_post_content(post['id'], new_content, config)

    return True, f"画像追加（{len(images_to_insert)}枚、レート残り{rate_remaining}）"


# =============================================================================
# メイン処理
# =============================================================================

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='WordPress記事の改善を自動適用')
    parser.add_argument('--mode', choices=['meta-desc', 'summary', 'links', 'images', 'all'],
                        default='all', help='実行モード')
    parser.add_argument('--post-id', type=int, help='特定の記事IDのみ処理')
    parser.add_argument('--dry-run', action='store_true', help='実際に更新せず確認のみ')
    parser.add_argument('--max-links', type=int, default=5, help='追加する内部リンク数')
    parser.add_argument('--max-images', type=int, default=3, help='追加する画像数')

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
            step_total = 4 if args.mode == 'all' else 1
            step_num = 0

            if args.mode in ['meta-desc', 'all']:
                step_num += 1
                print(f"  [{step_num}/{step_total}] メタディスクリプション設定... ", end="", flush=True)
                meta_desc = generate_meta_description(post)
                print(f"{len(meta_desc)}文字")
                if args.dry_run:
                    print(f"        プレビュー: {meta_desc[:80]}...")
                else:
                    set_meta_description(post['id'], meta_desc, config)
                    print("        ✅ 設定完了")

            if args.mode in ['summary', 'all']:
                step_num += 1
                print(f"  [{step_num}/{step_total}] まとめセクション追加... ", end="", flush=True)
                success, message = add_summary_to_post(post, config, args.dry_run)
                if success:
                    print(f"✅ {message}")
                else:
                    print(f"⚠️ {message}")

            if args.mode in ['links', 'all']:
                step_num += 1
                print(f"  [{step_num}/{step_total}] 内部リンク追加（最大{args.max_links}個）... ", end="", flush=True)
                if suggestions_dict:
                    success, message = add_internal_links_to_post(post, suggestions_dict, args.max_links, config, args.dry_run)
                    if success:
                        print(f"✅ {message}")
                    else:
                        print(f"⚠️ {message}")
                else:
                    print("⚠️ スキップ（CSV未読み込み）")

            if args.mode in ['images', 'all']:
                step_num += 1
                print(f"  [{step_num}/{step_total}] 画像追加（最大{args.max_images}枚）... ", end="", flush=True)
                success, message = add_images_to_post(post, args.max_images, config, args.dry_run)
                if success:
                    print(f"✅ {message}")
                else:
                    print(f"⚠️ {message}")

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
