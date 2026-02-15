#!/usr/bin/env python3
"""
backup_posts.py - WordPress記事の完全バックアップツール

全記事のデータをJSON形式でバックアップします。
- WordPress REST APIから全記事を取得
- AIOSEO APIからメタディスクリプションを取得
- タイムスタンプ付きでbackups/ディレクトリに保存
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

# .envファイルから環境変数を読み込む
load_dotenv()

def load_config():
    """環境変数から設定を読み込む"""
    config = {
        "WORDPRESS_URL": os.getenv("WORDPRESS_URL"),
        "WORDPRESS_USERNAME": os.getenv("WORDPRESS_USERNAME"),
        "WORDPRESS_APPLICATION_PASSWORD": os.getenv("WORDPRESS_APPLICATION_PASSWORD"),
    }

    # 必須設定の確認
    for key, value in config.items():
        if not value:
            raise ValueError(f"{key} が.envファイルに設定されていません")

    return config


def get_all_posts(config):
    """WordPress REST APIから全記事を取得"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/posts"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    all_posts = []
    page = 1

    print("📥 WordPress記事を取得中...")

    while True:
        params = {
            "per_page": 100,
            "page": page,
            "status": "publish",
            "_embed": True  # カテゴリ・タグ・アイキャッチ画像も取得
        }

        response = requests.get(url, params=params, auth=auth)

        if response.status_code != 200:
            print(f"❌ エラー: {response.status_code}")
            print(response.text)
            break

        posts = response.json()

        if not posts:
            break

        all_posts.extend(posts)

        total_pages = int(response.headers.get("X-WP-TotalPages", 1))
        print(f"   ページ {page}/{total_pages} 取得完了 ({len(posts)}記事)")

        if page >= total_pages:
            break

        page += 1

    print(f"✅ 合計 {len(all_posts)} 記事を取得しました")
    return all_posts


def get_meta_description(post_id, config):
    """AIOSEO APIからメタディスクリプションを取得"""
    url = f"{config['WORDPRESS_URL']}/wp-json/aioseo/v1/post"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    try:
        payload = {"id": post_id}
        response = requests.post(url, json=payload, auth=auth, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if result.get('success') and 'post' in result:
                return result['post'].get('description', '')

        return ''
    except Exception as e:
        print(f"   ⚠️  記事ID {post_id} のメタディスクリプション取得失敗: {str(e)}")
        return ''


def strip_html_tags(html):
    """HTMLタグを除去してプレーンテキストを取得"""
    if not html:
        return ''

    soup = BeautifulSoup(html, 'html.parser')

    # スクリプト・スタイルタグを削除
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text()

    # 複数の空白・改行を整理
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)

    return text


def backup_posts(config):
    """全記事をバックアップ"""
    # 全記事を取得
    posts = get_all_posts(config)

    if not posts:
        print("❌ 取得できた記事がありません")
        return None

    # バックアップデータの構築
    print("\n📦 バックアップデータを作成中...")
    backup_data = {
        "backup_date": datetime.now().isoformat(),
        "total_posts": len(posts),
        "posts": []
    }

    for idx, post in enumerate(posts, 1):
        print(f"   [{idx}/{len(posts)}] {post['title']['rendered'][:50]}...")

        # カテゴリ情報の抽出
        categories = []
        if '_embedded' in post and 'wp:term' in post['_embedded']:
            for term_group in post['_embedded']['wp:term']:
                for term in term_group:
                    if term.get('taxonomy') == 'category':
                        categories.append({
                            'id': term['id'],
                            'name': term['name'],
                            'slug': term['slug']
                        })

        # タグ情報の抽出
        tags = []
        if '_embedded' in post and 'wp:term' in post['_embedded']:
            for term_group in post['_embedded']['wp:term']:
                for term in term_group:
                    if term.get('taxonomy') == 'post_tag':
                        tags.append({
                            'id': term['id'],
                            'name': term['name'],
                            'slug': term['slug']
                        })

        # アイキャッチ画像情報の抽出
        featured_image = None
        if '_embedded' in post and 'wp:featuredmedia' in post['_embedded']:
            media = post['_embedded']['wp:featuredmedia']
            if media and len(media) > 0:
                featured_image = {
                    'id': media[0].get('id'),
                    'url': media[0].get('source_url'),
                    'title': media[0].get('title', {}).get('rendered', ''),
                    'alt': media[0].get('alt_text', '')
                }

        # メタディスクリプションを取得
        meta_description = get_meta_description(post['id'], config)

        # 本文HTMLとプレーンテキスト
        content_html = post['content']['rendered']
        content_text = strip_html_tags(content_html)

        # バックアップデータに追加
        post_data = {
            'id': post['id'],
            'title': post['title']['rendered'],
            'slug': post['slug'],
            'url': post['link'],
            'status': post['status'],
            'date': post['date'],
            'modified': post['modified'],
            'content_html': content_html,
            'content_text': content_text,
            'content_length': len(content_text),
            'excerpt': post['excerpt']['rendered'],
            'categories': categories,
            'tags': tags,
            'featured_image': featured_image,
            'meta_description': meta_description,
            'meta_description_length': len(meta_description) if meta_description else 0
        }

        backup_data['posts'].append(post_data)

    # ファイルに保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backups/posts_backup_{timestamp}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ バックアップ完了: {filename}")
    print(f"   記事数: {len(posts)}")
    print(f"   ファイルサイズ: {os.path.getsize(filename) / 1024:.1f} KB")

    return filename


def main():
    """メイン処理"""
    print("=" * 60)
    print("WordPress記事バックアップツール")
    print("=" * 60)
    print()

    try:
        # 設定読み込み
        config = load_config()
        print(f"📍 WordPress URL: {config['WORDPRESS_URL']}")
        print()

        # バックアップ実行
        backup_file = backup_posts(config)

        if backup_file:
            print()
            print("=" * 60)
            print("✨ バックアップが正常に完了しました")
            print("=" * 60)
        else:
            print()
            print("=" * 60)
            print("⚠️  バックアップが完了しませんでした")
            print("=" * 60)

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
