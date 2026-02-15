#!/usr/bin/env python3
"""
improve_all_posts.py - 記事改善管理スクリプト

posts_to_improve/内の記事を管理し、改善状況を追跡します。
実際の改善処理は、Claude Codeのサブエージェントが行います。

このスクリプトは：
1. 改善が必要な記事をリストアップ
2. 改善済み記事を確認
3. 改善状況のサマリーを表示
"""

import os
import glob


def list_posts_to_improve():
    """改善が必要な記事をリストアップ"""
    md_files = sorted(glob.glob('posts_to_improve/post_*.md'))

    posts = []
    for md_file in md_files:
        post_id = os.path.basename(md_file).replace('post_', '').replace('.md', '')

        # 対応する改善済みファイルが存在するか確認
        improved_file = f'posts_improved/post_{post_id}.html'
        is_improved = os.path.exists(improved_file)

        posts.append({
            'id': post_id,
            'md_file': md_file,
            'improved_file': improved_file,
            'is_improved': is_improved
        })

    return posts


def print_status(posts):
    """改善状況を表示"""
    total = len(posts)
    improved = sum(1 for p in posts if p['is_improved'])
    remaining = total - improved

    print("=" * 60)
    print("記事改善状況サマリー")
    print("=" * 60)
    print(f"合計記事数: {total}")
    print(f"改善済み:   {improved}")
    print(f"未改善:     {remaining}")
    print()

    if remaining > 0:
        print("未改善の記事:")
        print("-" * 60)
        for post in posts:
            if not post['is_improved']:
                print(f"  ❌ 記事ID {post['id']:>3}: {post['md_file']}")
        print()

    if improved > 0:
        print("改善済みの記事:")
        print("-" * 60)
        for post in posts:
            if post['is_improved']:
                file_size = os.path.getsize(post['improved_file']) / 1024
                print(f"  ✅ 記事ID {post['id']:>3}: {post['improved_file']} ({file_size:.1f} KB)")
        print()

    return total, improved, remaining


def main():
    """メイン処理"""
    print()
    posts = list_posts_to_improve()
    total, improved, remaining = print_status(posts)

    if remaining > 0:
        print("=" * 60)
        print("次のステップ:")
        print("=" * 60)
        print()
        print("Claude Codeで以下のコマンドを実行して、記事を改善してください：")
        print()
        print("【方法1】一括改善（推奨）")
        print("  Task toolを使って、複数の記事を並列処理します。")
        print()
        print("【方法2】個別改善")
        print("  各記事を個別に改善します：")
        print()
        for idx, post in enumerate(posts[:5], 1):  # 最初の5記事を表示
            if not post['is_improved']:
                print(f"  {idx}. 記事ID {post['id']}:")
                print(f"     - {post['md_file']} を読む")
                print(f"     - 改善指示に従って記事を改善")
                print(f"     - {post['improved_file']} に保存")
                print()

        if remaining > 5:
            print(f"  ... 他 {remaining - 5} 記事")
            print()

        print("=" * 60)
    else:
        print("=" * 60)
        print("✨ すべての記事の改善が完了しました！")
        print("=" * 60)
        print()
        print("次のステップ:")
        print("  apply_improved_content.py を実行して、改善後の記事をWordPressに適用してください")
        print()

    return 0


if __name__ == "__main__":
    exit(main())
