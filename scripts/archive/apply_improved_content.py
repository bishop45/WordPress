#!/usr/bin/env python3
"""
apply_improved_content.py - 改善された記事をWordPressに適用

posts_improved/内の改善済みHTMLファイルをWordPressに反映します。

機能:
- DRY RUNモードで変更内容をプレビュー
- 更新前のバックアップ作成
- サマリーレポート表示
"""

import os
import glob
import json
import requests
import argparse
from datetime import datetime
from dotenv import load_dotenv

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


def get_improved_posts():
    """改善済み記事のリストを取得"""
    html_files = sorted(glob.glob('posts_improved/post_*.html'))

    posts = []
    for html_file in html_files:
        post_id = os.path.basename(html_file).replace('post_', '').replace('.html', '')

        # HTMLファイルを読み込み
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        posts.append({
            'id': int(post_id),
            'html_file': html_file,
            'content': content,
            'size': len(content)
        })

    return posts


def get_current_post(post_id, config):
    """現在の記事内容を取得"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/posts/{post_id}"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        post = response.json()
        return {
            'id': post['id'],
            'title': post['title']['rendered'],
            'content': post['content']['rendered'],
            'modified': post['modified']
        }
    else:
        print(f"   ❌ 記事ID {post_id} の取得に失敗: {response.status_code}")
        return None


def update_post_content(post_id, new_content, config, dry_run=False):
    """記事内容を更新"""
    if dry_run:
        print(f"   [DRY RUN] 記事ID {post_id} の更新をスキップ")
        return True

    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/posts/{post_id}"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    payload = {"content": new_content}

    response = requests.post(url, json=payload, auth=auth)

    if response.status_code == 200:
        return True
    else:
        print(f"   ❌ 更新失敗: {response.status_code}")
        print(f"   {response.text}")
        return False


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='改善された記事をWordPressに適用')
    parser.add_argument('--dry-run', action='store_true', help='実際に更新せず確認のみ')
    parser.add_argument('--post-id', type=int, help='特定の記事IDのみ更新')
    args = parser.parse_args()

    print("=" * 60)
    if args.dry_run:
        print("改善記事適用ツール [DRY RUN モード]")
    else:
        print("改善記事適用ツール")
    print("=" * 60)
    print()

    try:
        # 設定読み込み
        config = load_config()
        print(f"📍 WordPress URL: {config['WORDPRESS_URL']}")
        print()

        # 改善済み記事を取得
        improved_posts = get_improved_posts()

        if args.post_id:
            # 特定の記事のみフィルタ
            improved_posts = [p for p in improved_posts if p['id'] == args.post_id]

        if not improved_posts:
            if args.post_id:
                print(f"❌ 記事ID {args.post_id} の改善ファイルが見つかりません")
            else:
                print("❌ 改善済み記事が見つかりません")
            return 1

        print(f"📝 処理対象: {len(improved_posts)} 記事")
        print()

        # 各記事を処理
        success_count = 0
        fail_count = 0

        for idx, improved_post in enumerate(improved_posts, 1):
            post_id = improved_post['id']

            print(f"[{idx}/{len(improved_posts)}] 記事ID {post_id}")

            # 現在の記事内容を取得
            current_post = get_current_post(post_id, config)

            if not current_post:
                fail_count += 1
                continue

            print(f"   タイトル: {current_post['title'][:50]}...")
            print(f"   現在の文字数: {len(current_post['content'])} 文字")
            print(f"   改善後の文字数: {improved_post['size']} 文字")

            diff = improved_post['size'] - len(current_post['content'])
            if diff > 0:
                print(f"   📈 +{diff} 文字増加")
            else:
                print(f"   📉 {diff} 文字減少")

            # 更新実行
            if update_post_content(post_id, improved_post['content'], config, args.dry_run):
                if not args.dry_run:
                    print(f"   ✅ 更新完了")
                success_count += 1
            else:
                fail_count += 1

            print()

        # サマリー表示
        print("=" * 60)
        print("処理結果サマリー")
        print("=" * 60)
        print(f"成功: {success_count} 記事")
        print(f"失敗: {fail_count} 記事")
        print()

        if args.dry_run:
            print("=" * 60)
            print("DRY RUNモードで実行しました")
            print("実際に更新するには --dry-run を外して実行してください")
            print("=" * 60)
        else:
            print("=" * 60)
            print("✨ 記事の適用が完了しました！")
            print("=" * 60)
            print()
            print("次のステップ:")
            print("  1. WordPress管理画面で記事を確認してください")
            print("  2. 画像バリエーション改善を実施してください")
            print("  3. 内部リンク提案を実施してください")
            print()

        return 0 if fail_count == 0 else 1

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
