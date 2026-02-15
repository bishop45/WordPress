#!/usr/bin/env python3
"""WordPress記事一覧バックアップスクリプト

記事作成・更新後に実行して、記事データの履歴を保存します。
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_URL', 'https://techsimpleapp.main.jp')
BACKUP_DIR = Path('backups')
BACKUP_DIR.mkdir(exist_ok=True)


def get_all_posts():
    """全記事を取得（ページネーション対応）"""
    posts = []
    page = 1
    per_page = 100

    print(f"🔄 記事一覧を取得中...")

    while True:
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"
        params = {'per_page': per_page, 'page': page}

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ エラー: {e}")
            return posts

        batch = response.json()
        if not batch:
            break

        posts.extend(batch)
        print(f"  ページ {page}: {len(batch)}件取得")

        # 次のページがあるかチェック
        total_pages = int(response.headers.get('X-WP-TotalPages', 1))
        if page >= total_pages:
            break

        page += 1

    return posts


def save_json_backup(posts, timestamp):
    """JSON形式でバックアップ（完全なデータ）"""
    filename = BACKUP_DIR / f"posts_backup_{timestamp}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"✓ JSON backup saved: {filename}")
    return filename


def save_csv_backup(posts, timestamp):
    """CSV形式でバックアップ（主要データのみ）"""
    filename = BACKUP_DIR / f"posts_backup_{timestamp}.csv"

    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        # ヘッダー
        writer.writerow([
            'ID', 'タイトル', 'URL', 'ステータス', '公開日', '更新日',
            'カテゴリ数', 'タグ数', '文字数', 'アイキャッチ画像'
        ])

        # データ
        for post in posts:
            title = post.get('title', {}).get('rendered', '')
            content = post.get('content', {}).get('rendered', '')

            writer.writerow([
                post.get('id'),
                title.strip(),
                post.get('link'),
                post.get('status'),
                post.get('date', '').split('T')[0] if post.get('date') else '',
                post.get('modified', '').split('T')[0] if post.get('modified') else '',
                len(post.get('categories', [])),
                len(post.get('tags', [])),
                len(content),
                '✓' if post.get('featured_media') else '✗'
            ])

    print(f"✓ CSV backup saved: {filename}")
    return filename


def main():
    """メイン処理"""
    print("=" * 60)
    print("📦 WordPress 記事一覧バックアップ")
    print("=" * 60)

    # 記事取得
    posts = get_all_posts()

    if not posts:
        print("❌ 記事が取得できませんでした")
        return

    print(f"\n✓ {len(posts)}件の記事を取得しました")

    # タイムスタンプ生成
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # バックアップ保存
    print("\n💾 バックアップを保存中...")
    json_file = save_json_backup(posts, timestamp)
    csv_file = save_csv_backup(posts, timestamp)

    # 結果表示
    print("\n" + "=" * 60)
    print("✅ バックアップ完了！")
    print("=" * 60)
    print(f"  - JSON: {json_file}")
    print(f"  - CSV: {csv_file}")
    print(f"  - 記事数: {len(posts)}件")
    print(f"  - タイムスタンプ: {timestamp}")

    # 統計情報
    published = sum(1 for p in posts if p.get('status') == 'publish')
    draft = sum(1 for p in posts if p.get('status') == 'draft')
    with_featured = sum(1 for p in posts if p.get('featured_media'))

    print("\n📊 統計情報:")
    print(f"  - 公開記事: {published}件")
    print(f"  - 下書き: {draft}件")
    print(f"  - アイキャッチ画像設定済み: {with_featured}件 ({with_featured/len(posts)*100:.1f}%)")

    print("=" * 60)


if __name__ == '__main__':
    main()
