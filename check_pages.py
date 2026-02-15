#!/usr/bin/env python3
"""
固定ページの内容確認スクリプト
WordPress REST APIを使用して固定ページのHTML内容を取得する
"""

import os
import sys
import requests
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

def get_page_by_slug(slug, config):
    """固定ページをスラッグで取得"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/pages"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    params = {
        "slug": slug,
        "per_page": 1
    }

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        pages = response.json()
        if pages:
            return pages[0]

    return None

def main():
    config = load_config()

    # 確認するページのスラッグ
    page_slugs = {
        "profile": "プロフィール",
        "%e6%89%80%e6%9c%89%e8%b3%87%e6%a0%bc": "保有資格",
        "privacy-policy": "プライバシーポリシー",
        "%e3%81%8a%e5%95%8f%e3%81%84%e5%90%88%e3%82%8f%e3%81%9b": "お問い合わせ"
    }

    print("=" * 80)
    print("固定ページ内容確認")
    print("=" * 80)
    print()

    for slug, name in page_slugs.items():
        print(f"📄 {name} ({slug})")
        print("-" * 80)

        page = get_page_by_slug(slug, config)

        if page:
            print(f"ID: {page['id']}")
            print(f"タイトル: {page['title']['rendered']}")
            print(f"URL: {page['link']}")
            print(f"ステータス: {page['status']}")
            print(f"\nコンテンツ（最初の500文字）:")
            print(page['content']['rendered'][:500])
            print("...")
            print()
        else:
            print(f"❌ ページが見つかりませんでした")
            print()

        print()

if __name__ == "__main__":
    main()
