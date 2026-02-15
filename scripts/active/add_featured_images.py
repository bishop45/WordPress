"""
WordPress ブログ記事にUnsplash画像をアイキャッチとして自動設定するスクリプト
"""

import os
import re
import random
import time
import sys

import requests
from dotenv import load_dotenv


# --- 日本語キーワード → 英語マッピング ---
JAPANESE_KEYWORD_MAP = {
    "プログラミング": "programming",
    "アプリ": "application",
    "開発": "software development",
    "ブログ": "blog writing",
    "副業": "side business",
    "投資": "investment",
    "仮想通貨": "cryptocurrency",
    "セキュリティ": "cybersecurity",
    "データ": "data",
    "クラウド": "cloud computing",
    "自動化": "automation",
    "効率化": "productivity",
    "ツール": "tools",
    "スマホ": "smartphone",
    "パソコン": "computer",
    "ネットワーク": "network",
    "デザイン": "design",
    "マーケティング": "marketing",
    "ビジネス": "business",
    "学習": "learning",
    "入門": "beginner guide",
    "解説": "tutorial",
    "比較": "comparison",
    "レビュー": "review",
    "おすすめ": "recommendation",
    "使い方": "how to use",
    "始め方": "getting started",
    "議事録": "meeting notes",
    "会議": "meeting",
    "ChatGPT": "artificial intelligence",
    "生成AI": "artificial intelligence",
    "機械学習": "machine learning",
    "ディープラーニング": "deep learning",
    "ウェブ": "web",
    "サーバー": "server",
    "データベース": "database",
    "コード": "coding",
    "エンジニア": "engineer",
    "転職": "career change",
    "収益": "revenue",
    "SEO": "search engine optimization",
    "SNS": "social media",
    "動画": "video",
    "写真": "photography",
    "節約": "saving money",
    "時短": "time saving",
    "リモートワーク": "remote work",
    "フリーランス": "freelance",
}

FALLBACK_KEYWORDS = ["technology", "computer", "digital", "workspace", "coding"]


def load_config():
    """環境変数から設定を読み込む"""
    load_dotenv()

    required_vars = [
        "WORDPRESS_URL",
        "WORDPRESS_USERNAME",
        "WORDPRESS_APPLICATION_PASSWORD",
        "UNSPLASH_ACCESS_KEY",
    ]
    config = {}
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            print(f"エラー: 環境変数 {var} が設定されていません。")
            sys.exit(1)
        config[var] = value

    return config


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


def get_all_posts(config):
    """WordPress REST APIで全記事を取得する"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/posts"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    all_posts = []
    page = 1

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

    return all_posts


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

    return media["id"]


def set_featured_image(post_id, media_id, config):
    """記事にアイキャッチ画像を設定する"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/posts/{post_id}"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    response = requests.post(url, json={"featured_media": media_id}, auth=auth)

    if response.status_code != 200:
        raise Exception(f"アイキャッチ設定失敗 (HTTP {response.status_code}): {response.text[:200]}")


def wait_for_rate_limit(rate_remaining):
    """レート制限に近い場合は待機する"""
    if rate_remaining <= 5:
        print("\n⏳ Unsplash APIレート制限に近づいています。60分待機します...")
        print("   (Ctrl+Cで中断できます)")
        for remaining in range(3600, 0, -60):
            print(f"   残り {remaining // 60} 分...")
            time.sleep(60)
        print("   待機完了。処理を再開します。\n")


def main():
    config = load_config()

    # 全記事を取得
    print("WordPress記事を取得中...")
    all_posts = get_all_posts(config)
    print(f"取得完了: {len(all_posts)}記事")

    # アイキャッチ画像がない記事をフィルタリング
    posts_without_image = [p for p in all_posts if p.get("featured_media", 0) == 0]
    print(f"アイキャッチ画像なし: {len(posts_without_image)}記事\n")

    if not posts_without_image:
        print("すべての記事にアイキャッチ画像が設定されています。")
        return

    success_count = 0
    fail_count = 0
    total = len(posts_without_image)

    print("処理開始...")
    for i, post in enumerate(posts_without_image, 1):
        title = post["title"]["rendered"]
        # HTMLエンティティをデコード
        title = title.replace("&#8211;", "–").replace("&#8230;", "…").replace("&amp;", "&")

        print(f"[{i}/{total}] 「{title}」... ", end="", flush=True)

        try:
            # キーワード抽出
            keyword = extract_keywords(title)

            # Unsplashで画像検索
            image_info, rate_remaining = search_unsplash_image(keyword, config)

            # 見つからなければフォールバックキーワードで再検索
            if image_info is None:
                fallback = random.choice(FALLBACK_KEYWORDS)
                image_info, rate_remaining = search_unsplash_image(fallback, config)

            if image_info is None:
                print("❌ 失敗: 画像が見つかりませんでした")
                fail_count += 1
                continue

            # Unsplashダウンロードトリガー（利用規約準拠）
            trigger_unsplash_download(image_info["download_location"], config)

            # 画像ダウンロード
            image_data = download_image(image_info["url"])

            # WordPressにアップロード
            filename = f"unsplash-{post['id']}.jpg"
            alt_text = f"{title} - Photo by {image_info['photographer']} on Unsplash"
            media_id = upload_to_wordpress(image_data, filename, alt_text, config)

            # アイキャッチ画像を設定
            set_featured_image(post["id"], media_id, config)

            print("✅ 完了")
            success_count += 1

            # レート制限チェック
            wait_for_rate_limit(rate_remaining)

            # リクエスト間の待機
            time.sleep(2)

        except KeyboardInterrupt:
            print("\n\n中断されました。")
            break
        except Exception as e:
            print(f"❌ 失敗: {e}")
            fail_count += 1
            time.sleep(2)

    # サマリー表示
    print(f"\n{'='*40}")
    print("処理完了！")
    print(f"  成功: {success_count}件")
    print(f"  失敗: {fail_count}件")
    print(f"  合計: {total}件")
    print(f"{'='*40}")


if __name__ == "__main__":
    main()
