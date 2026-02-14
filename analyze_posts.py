"""
WordPress ブログ記事を分析して、削除候補をリストアップするスクリプト
AdSense 審査対策のため、質の低いコンテンツを特定します。
"""

import os
import re
import csv
import sys
from datetime import datetime

import requests
import html as html_module
from dotenv import load_dotenv


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


def analyze_post(post):
    """記事を分析して問題点を検出"""
    title = html_module.unescape(post['title']['rendered'])
    content = post['content']['rendered']
    text_content = extract_text_content(content)
    word_count = len(text_content)

    issues = []
    deletion_score = 0  # 削除スコア（高いほど削除候補）

    # 1. 文字数チェック
    if word_count < 800:
        issues.append(f"文字数不足: {word_count}文字")
        deletion_score += 10
    elif word_count < 1500:
        issues.append(f"文字数やや不足: {word_count}文字")
        deletion_score += 3

    # 2. プライバシーポリシー系
    if 'プライバシーポリシー' in title or 'Privacy Policy' in title:
        issues.append("プライバシーポリシー記事")
        deletion_score += 10

    # 3. タイトルパターン分析
    if '？' in title or '?' in title:
        issues.append("疑問形タイトル")
        deletion_score += 2

    # 4. プレスリリース的なパターン
    press_release_patterns = [
        r'まだ.*してる？',
        r'できてない？',
        r'2026年\d+月\d+日',
        r'発表された',
        r'新機能',
        r'サービス開始',
    ]

    press_release_matches = 0
    for pattern in press_release_patterns:
        if re.search(pattern, title) or re.search(pattern, text_content[:500]):
            press_release_matches += 1

    if press_release_matches >= 2:
        issues.append(f"プレスリリース的（マッチ数: {press_release_matches}）")
        deletion_score += 5

    # 5. 推測表現が多い
    speculative_patterns = [
        r'みたい',
        r'かもしれない',
        r'だって',
        r'じゃないかな',
        r'はず',
    ]

    speculative_count = sum(len(re.findall(pattern, text_content)) for pattern in speculative_patterns)
    if speculative_count > 10:
        issues.append(f"推測表現が多い（{speculative_count}箇所）")
        deletion_score += 3

    # 6. 実体験の兆候をチェック（残すべき記事の特徴）
    experience_patterns = [
        r'受験記',
        r'使ってみた',
        r'試してみた',
        r'実際に',
        r'やってみた',
        r'合格',
        r'勉強方法',
    ]

    has_experience = any(re.search(pattern, title) or re.search(pattern, text_content[:500])
                         for pattern in experience_patterns)

    if has_experience:
        issues.append("✅ 実体験の可能性あり（残すべき）")
        deletion_score -= 10

    return {
        'id': post['id'],
        'title': title,
        'url': post['link'],
        'word_count': word_count,
        'issues': issues,
        'deletion_score': deletion_score,
        'has_question_mark': ('？' in title or '?' in title),
        'is_privacy_policy': ('プライバシーポリシー' in title or 'Privacy Policy' in title),
    }


def main():
    config = load_config()

    # 全記事を取得
    all_posts = get_all_posts(config)

    # 各記事を分析
    print("記事を分析中...\n")
    analysis_results = []
    for post in all_posts:
        result = analyze_post(post)
        analysis_results.append(result)

    # 削除スコアでソート（高い順）
    analysis_results.sort(key=lambda x: x['deletion_score'], reverse=True)

    # 統計情報を表示
    print("="*100)
    print("【分析結果サマリー】")
    print("="*100)
    print(f"総記事数: {len(analysis_results)}記事\n")

    # 文字数統計
    word_counts = [r['word_count'] for r in analysis_results]
    print(f"平均文字数: {sum(word_counts)/len(word_counts):.0f}文字")
    print(f"最小文字数: {min(word_counts)}文字")
    print(f"最大文字数: {max(word_counts)}文字")
    print(f"800文字未満: {sum(1 for wc in word_counts if wc < 800)}記事")
    print(f"1,500文字以上: {sum(1 for wc in word_counts if wc >= 1500)}記事\n")

    # パターン統計
    question_mark_count = sum(1 for r in analysis_results if r['has_question_mark'])
    privacy_policy_count = sum(1 for r in analysis_results if r['is_privacy_policy'])

    print(f"「？」を含むタイトル: {question_mark_count}記事（{question_mark_count/len(analysis_results)*100:.1f}%）")
    print(f"プライバシーポリシー系: {privacy_policy_count}記事\n")

    # 削除候補
    deletion_candidates = [r for r in analysis_results if r['deletion_score'] >= 5]
    keep_candidates = [r for r in analysis_results if r['deletion_score'] < 5]

    print("="*100)
    print(f"【削除候補】 {len(deletion_candidates)}記事（削除スコア5以上）")
    print("="*100)
    for i, result in enumerate(deletion_candidates[:20], 1):
        print(f"\n{i}. [{result['deletion_score']}点] {result['title'][:60]}")
        print(f"   文字数: {result['word_count']}文字")
        print(f"   問題点: {', '.join(result['issues'])}")
        print(f"   URL: {result['url']}")

    if len(deletion_candidates) > 20:
        print(f"\n... 他 {len(deletion_candidates) - 20}記事")

    print("\n" + "="*100)
    print(f"【残すべき記事】 {len(keep_candidates)}記事（削除スコア5未満）")
    print("="*100)
    for i, result in enumerate(keep_candidates[:10], 1):
        print(f"\n{i}. [{result['deletion_score']}点] {result['title'][:60]}")
        print(f"   文字数: {result['word_count']}文字")
        if result['issues']:
            print(f"   備考: {', '.join(result['issues'])}")

    if len(keep_candidates) > 10:
        print(f"\n... 他 {len(keep_candidates) - 10}記事")

    # CSVファイルに出力
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"post_analysis_{timestamp}.csv"

    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['記事ID', 'タイトル', '文字数', '削除スコア', '問題点', 'URL', '削除推奨'])

        for result in analysis_results:
            delete_recommend = '削除' if result['deletion_score'] >= 5 else '残す'
            writer.writerow([
                result['id'],
                result['title'],
                result['word_count'],
                result['deletion_score'],
                '; '.join(result['issues']),
                result['url'],
                delete_recommend
            ])

    print("\n" + "="*100)
    print(f"分析結果をCSVファイルに保存しました: {csv_filename}")
    print("="*100)

    # 推奨アクション
    print("\n【推奨アクション】")
    print(f"1. 削除推奨: {len(deletion_candidates)}記事")
    print(f"2. 残す推奨: {len(keep_candidates)}記事")
    print(f"3. 削除後の公開記事数: 約{len(keep_candidates)}記事")
    print(f"\n※ 目標: 20〜30記事に絞り、すべて1,500文字以上、独自性のある記事のみ残す")

    if len(keep_candidates) > 30:
        print(f"\n⚠️ 警告: 残す記事が{len(keep_candidates)}記事と多いです。")
        print(f"   さらに厳選して20〜30記事に絞ることを推奨します。")
    elif len(keep_candidates) < 20:
        print(f"\n⚠️ 警告: 残す記事が{len(keep_candidates)}記事と少ないです。")
        print(f"   新規記事の作成が必要です。")
    else:
        print(f"\n✅ 残す記事数は適切です（{len(keep_candidates)}記事）")


if __name__ == "__main__":
    main()
