"""
WordPress ブログ記事の構造を改善するスクリプト
Phase 2.3: メタディスクリプション、内部リンク、記事構造の自動分析・改善
"""

import os
import re
import csv
import sys
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


def extract_text_content(html_content):
    """HTMLから純粋なテキストコンテンツを抽出"""
    # HTMLエンティティをデコード
    text = html_module.unescape(html_content)
    # HTMLタグを削除
    text = re.sub(r'<[^>]+>', '', text)
    # 複数の空白を1つに
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def analyze_post_structure(post, config):
    """記事の構造を分析"""
    html_content = post['content']['rendered']
    title = html_module.unescape(post['title']['rendered'])

    # BeautifulSoupでHTML解析
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. 見出し数（h2, h3）
    headings = soup.find_all(['h2', 'h3'])
    heading_count = len(headings)

    # 2. まとめセクションの有無
    has_summary = False
    summary_keywords = ['まとめ', '結論', '要約', 'ポイント', '総括']
    for heading in headings:
        heading_text = heading.get_text().strip()
        if any(keyword in heading_text for keyword in summary_keywords):
            has_summary = True
            break

    # 3. 画像数（本文中のみ、アイキャッチ除外）
    images = soup.find_all('img')
    image_count = len(images)

    # 4. 内部リンク数（同一ドメイン）
    links = soup.find_all('a', href=True)
    internal_links = [
        link for link in links
        if config['WORDPRESS_URL'] in link['href']
    ]
    internal_link_count = len(internal_links)

    # 5. メタディスクリプション取得（WordPress REST API経由）
    meta_desc = ''
    meta_desc_length = 0
    has_meta_desc = False

    # WordPress REST APIで記事のmetaを取得
    post_id = post['id']
    meta_url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/posts/{post_id}"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    try:
        response = requests.get(meta_url, params={'context': 'edit'}, auth=auth)
        if response.status_code == 200:
            post_data = response.json()
            if 'meta' in post_data and '_yoast_wpseo_metadesc' in post_data['meta']:
                meta_desc = post_data['meta']['_yoast_wpseo_metadesc']
                if meta_desc:
                    has_meta_desc = True
                    meta_desc_length = len(meta_desc)
    except Exception:
        pass  # メタディスクリプション取得失敗時はスキップ

    # 6. 文字数
    text_content = extract_text_content(html_content)
    word_count = len(text_content)

    # 改善項目のリスト作成
    improvements = []
    if heading_count < 3:
        improvements.append('見出し構造の改善')
    if not has_summary:
        improvements.append('まとめセクションの追加')
    if image_count < 3:
        improvements.append('画像の追加')
    if internal_link_count < 3:
        improvements.append('内部リンクの追加')
    if not has_meta_desc:
        improvements.append('メタディスクリプションの設定')
    if word_count < 1500:
        improvements.append('文字数の増加')

    needs_improvement = '要改善' if improvements else '良好'
    improvement_list = '; '.join(improvements) if improvements else ''

    return {
        'id': post['id'],
        'title': title,
        'url': post['link'],
        'word_count': word_count,
        'heading_count': heading_count,
        'has_summary': 'あり' if has_summary else 'なし',
        'image_count': image_count,
        'internal_link_count': internal_link_count,
        'has_meta_desc': 'あり' if has_meta_desc else 'なし',
        'meta_desc_length': meta_desc_length,
        'needs_improvement': needs_improvement,
        'improvement_list': improvement_list
    }


def generate_structure_report(analysis_results, output_path):
    """分析結果をCSV出力"""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            '記事ID', 'タイトル', 'URL', '文字数', '見出し数', 'まとめあり',
            '画像数', '内部リンク数', 'メタディスクリプションあり',
            'メタディスクリプション文字数', '改善推奨', '改善項目'
        ])

        for result in analysis_results:
            writer.writerow([
                result['id'],
                result['title'],
                result['url'],
                result['word_count'],
                result['heading_count'],
                result['has_summary'],
                result['image_count'],
                result['internal_link_count'],
                result['has_meta_desc'],
                result['meta_desc_length'],
                result['needs_improvement'],
                result['improvement_list']
            ])

    return output_path


def extract_keywords(post):
    """記事からキーワードを抽出"""
    keywords = set()

    # タイトルから
    title = html_module.unescape(post['title']['rendered'])
    # 簡易的な単語分割（スペース、句読点で分割）
    title_words = re.split(r'[\s、。！？「」（）【】\[\]]+', title)
    keywords.update([w for w in title_words if len(w) >= 2])

    return keywords


def calculate_similarity(keywords1, keywords2):
    """Jaccard係数で類似度を計算"""
    if not keywords1 or not keywords2:
        return 0.0

    intersection = len(keywords1 & keywords2)
    union = len(keywords1 | keywords2)

    if union == 0:
        return 0.0

    return intersection / union


def suggest_internal_links(all_posts):
    """内部リンク候補を提案"""
    suggestions = []

    for target_post in all_posts:
        target_keywords = extract_keywords(target_post)
        target_title = html_module.unescape(target_post['title']['rendered'])

        # 他の記事との類似度を計算
        similarities = []
        for other_post in all_posts:
            if other_post['id'] == target_post['id']:
                continue  # 自分自身は除外

            other_keywords = extract_keywords(other_post)
            similarity = calculate_similarity(target_keywords, other_keywords)

            if similarity > 0:  # 類似度が0より大きい場合のみ
                similarities.append({
                    'post': other_post,
                    'similarity': similarity,
                    'common_keywords': list(target_keywords & other_keywords)
                })

        # 類似度でソートして上位5件を取得
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        top_suggestions = similarities[:5]

        # 提案リストに追加
        for suggestion in top_suggestions:
            other_post = suggestion['post']
            other_title = html_module.unescape(other_post['title']['rendered'])

            suggestions.append({
                'source_id': target_post['id'],
                'source_title': target_title,
                'source_url': target_post['link'],
                'target_id': other_post['id'],
                'target_title': other_title,
                'target_url': other_post['link'],
                'similarity': suggestion['similarity'],
                'common_keywords': ', '.join(suggestion['common_keywords'][:5])  # 最大5個
            })

    return suggestions


def generate_links_report(suggestions, output_path):
    """提案結果をCSV出力"""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            '記事ID', 'タイトル', 'URL', '提案リンク先ID',
            '提案リンク先タイトル', '提案リンク先URL',
            '類似度スコア', '共通キーワード'
        ])

        for suggestion in suggestions:
            writer.writerow([
                suggestion['source_id'],
                suggestion['source_title'],
                suggestion['source_url'],
                suggestion['target_id'],
                suggestion['target_title'],
                suggestion['target_url'],
                f"{suggestion['similarity']:.3f}",
                suggestion['common_keywords']
            ])

    return output_path


def run_analyze_mode(config, all_posts):
    """Phase 1: 記事構造分析モード"""
    print("=" * 60)
    print("Phase 1: 記事構造分析")
    print("=" * 60 + "\n")

    analysis_results = []
    success_count = 0
    fail_count = 0

    for i, post in enumerate(all_posts, 1):
        title = html_module.unescape(post['title']['rendered'])[:50]
        print(f"[{i}/{len(all_posts)}] 「{title}...」 ", end="", flush=True)

        try:
            result = analyze_post_structure(post, config)
            analysis_results.append(result)
            print("✅ 完了")
            success_count += 1
        except KeyboardInterrupt:
            print("\n\n中断されました。")
            break
        except Exception as e:
            print(f"❌ 失敗: {e}")
            fail_count += 1

    # レポート生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"reports/post_structure_analysis_{timestamp}.csv"
    generate_structure_report(analysis_results, csv_filename)

    print(f"\n{'=' * 60}")
    print("処理完了！")
    print(f"  成功: {success_count}件")
    print(f"  失敗: {fail_count}件")
    print(f"  レポート: {csv_filename}")
    print(f"{'=' * 60}\n")


def run_suggest_links_mode(config, all_posts):
    """Phase 2: 内部リンク提案モード"""
    print("=" * 60)
    print("Phase 2: 内部リンク提案")
    print("=" * 60 + "\n")

    print("記事間の類似度を計算中...")
    suggestions = suggest_internal_links(all_posts)

    # レポート生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"reports/internal_link_suggestions_{timestamp}.csv"
    generate_links_report(suggestions, csv_filename)

    print(f"\n{'=' * 60}")
    print("処理完了！")
    print(f"  提案数: {len(suggestions)}件")
    print(f"  レポート: {csv_filename}")
    print(f"{'=' * 60}\n")


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='WordPress記事の構造を改善するスクリプト'
    )
    parser.add_argument(
        '--mode',
        choices=['analyze', 'suggest-links', 'all'],
        default='analyze',
        help='実行モード (default: analyze)'
    )

    args = parser.parse_args()

    # 設定読み込み
    config = load_config()

    # 全記事取得
    all_posts = get_all_posts(config)

    if not all_posts:
        print("記事が見つかりませんでした。")
        sys.exit(1)

    # モードに応じて処理実行
    if args.mode == 'analyze':
        run_analyze_mode(config, all_posts)
    elif args.mode == 'suggest-links':
        run_suggest_links_mode(config, all_posts)
    elif args.mode == 'all':
        run_analyze_mode(config, all_posts)
        print()  # 空行
        run_suggest_links_mode(config, all_posts)


if __name__ == "__main__":
    main()
