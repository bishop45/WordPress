"""
WordPress ブログ記事を一括で下書きに戻すスクリプト
AdSense 審査対策のため、質の低いコンテンツを非公開にします。
"""

import os
import sys
import csv

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


def unpublish_post(post_id, config, dry_run=False):
    """記事を下書きに戻す"""
    if dry_run:
        return True

    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/posts/{post_id}"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    data = {"status": "draft"}
    response = requests.post(url, json=data, auth=auth)

    if response.status_code != 200:
        print(f"  ❌ 失敗 (HTTP {response.status_code}): {response.text[:100]}")
        return False

    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="WordPress記事を一括で下書きに戻す")
    parser.add_argument(
        "--csv",
        required=True,
        help="CSVファイルパス（analyze_posts.py で生成したファイル）"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=5,
        help="削除スコアの閾値（この値以上の記事を下書きに戻す）"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="実際には実行せず、対象記事を表示するのみ"
    )
    parser.add_argument(
        "--ids",
        help="特定の記事IDのみ下書きに戻す（カンマ区切り）"
    )

    args = parser.parse_args()

    config = load_config()

    # CSVファイルを読み込む
    target_posts = []

    with open(args.csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            post_id = int(row['記事ID'])
            title = row['タイトル']
            word_count = int(row['文字数'])
            score = int(row['削除スコア'])

            # 特定のIDが指定されている場合
            if args.ids:
                if str(post_id) in args.ids.split(','):
                    target_posts.append((post_id, title, word_count, score))
            # 削除スコアで判定
            elif score >= args.threshold:
                target_posts.append((post_id, title, word_count, score))

    if not target_posts:
        print("下書きに戻す記事が見つかりませんでした。")
        return

    # 対象記事を表示
    print("="*100)
    if args.dry_run:
        print("【DRY RUN】 以下の記事を下書きに戻します（実際には実行されません）")
    else:
        print("【実行】 以下の記事を下書きに戻します")
    print("="*100)
    print(f"対象記事数: {len(target_posts)}記事")
    print(f"削除スコア閾値: {args.threshold}以上\n")

    for i, (post_id, title, word_count, score) in enumerate(target_posts, 1):
        print(f"{i}. [スコア{score}] {title[:60]}")
        print(f"   記事ID: {post_id}, 文字数: {word_count}文字")

    # 確認
    if not args.dry_run:
        print("\n" + "="*100)
        response = input(f"\n本当に {len(target_posts)} 記事を下書きに戻しますか？ (yes/no): ")
        if response.lower() != 'yes':
            print("キャンセルしました。")
            return

        print("\n処理を開始します...\n")

        success_count = 0
        fail_count = 0

        for i, (post_id, title, word_count, score) in enumerate(target_posts, 1):
            print(f"[{i}/{len(target_posts)}] {title[:50]}... ", end="", flush=True)

            if unpublish_post(post_id, config):
                print("✅ 完了")
                success_count += 1
            else:
                print("❌ 失敗")
                fail_count += 1

        # サマリー
        print("\n" + "="*100)
        print("処理完了！")
        print(f"  成功: {success_count}記事")
        print(f"  失敗: {fail_count}記事")
        print(f"  合計: {len(target_posts)}記事")
        print("="*100)
    else:
        print("\n" + "="*100)
        print("DRY RUN 完了。実際に実行するには --dry-run を外してください。")
        print("="*100)


if __name__ == "__main__":
    main()
