#!/usr/bin/env python3
"""
prepare_posts_for_improvement.py - 記事改善の準備スクリプト

バックアップJSONから各記事をMarkdown形式に変換し、
改善指示を含めてposts_to_improve/ディレクトリに保存します。
"""

import os
import json
import glob
from bs4 import BeautifulSoup
import re


def html_to_markdown(html):
    """簡易的なHTML→Markdown変換"""
    if not html:
        return ''

    soup = BeautifulSoup(html, 'html.parser')

    # 改行を保持するため、各要素を処理
    markdown = []

    for element in soup.find_all(recursive=False):
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(element.name[1])
            markdown.append(f"\n{'#' * level} {element.get_text().strip()}\n")
        elif element.name == 'p':
            text = element.get_text().strip()
            if text:
                markdown.append(f"{text}\n")
        elif element.name == 'ul':
            for li in element.find_all('li', recursive=False):
                markdown.append(f"- {li.get_text().strip()}")
            markdown.append('')
        elif element.name == 'ol':
            for idx, li in enumerate(element.find_all('li', recursive=False), 1):
                markdown.append(f"{idx}. {li.get_text().strip()}")
            markdown.append('')
        elif element.name == 'blockquote':
            text = element.get_text().strip()
            markdown.append(f"> {text}\n")
        elif element.name == 'pre':
            code = element.get_text()
            markdown.append(f"```\n{code}\n```\n")
        elif element.name == 'a':
            text = element.get_text().strip()
            href = element.get('href', '')
            markdown.append(f"[{text}]({href})")
        else:
            # その他の要素はテキストのみ抽出
            text = element.get_text().strip()
            if text:
                markdown.append(f"{text}\n")

    return '\n'.join(markdown)


def find_latest_backup():
    """最新のバックアップファイルを見つける"""
    backup_files = glob.glob('backups/posts_backup_*.json')

    if not backup_files:
        raise FileNotFoundError("バックアップファイルが見つかりません。先にbackup_posts.pyを実行してください。")

    # 最新のファイルを取得（ファイル名のタイムスタンプでソート）
    latest_backup = sorted(backup_files)[-1]
    return latest_backup


def create_improvement_prompt(post):
    """記事改善のためのプロンプトを生成"""
    current_length = post['content_length']
    target_length = max(1500, current_length)

    prompt = f"""# 改善指示

この記事を**Google AdSense審査突破**のために以下の観点で改善してください：

## 改善の目標

### 1. オリジナリティの強化
- 他サイトの情報を単純にまとめただけでなく、**独自の視点や分析**を追加してください
- 実例や具体的な数字を含めて説得力を高めてください
- 読者が「このサイトでしか読めない情報」と感じる要素を追加してください

### 2. 専門性の向上
- 技術的な正確性を保ちつつ、**より深い洞察**を追加してください
- 背景や原因、影響を詳しく説明してください
- 初心者でも理解できるように、専門用語には説明を加えてください

### 3. 読みやすさの改善
- 段落構成を見直し、**論理的な流れ**を作ってください
- 見出しを効果的に使って、記事の構造を明確にしてください
- 具体例や比喩を使って、理解しやすくしてください

### 4. 価値提供の明確化
- 読者が**実際に行動できる具体的な情報**を含めてください
- 「どうすればいいか」「何をすべきか」を明示してください
- 読み終わった後、読者が得られるメリットを明確にしてください

### 5. 文字数の目安
- **現在の文字数**: {current_length}文字
- **目標文字数**: {target_length}文字以上（1,500文字以上が望ましい）
- 単に文字数を増やすのではなく、**有益な情報を追加**してください

## 改善の制約

- 元の記事の主題やテーマは変えないでください
- 技術的な内容の正確性を保ってください
- HTMLタグの構造は維持してください（h2, h3, p, ul, li など）
- 画像タグ（<img>）が含まれている場合は、そのまま残してください

## 出力形式

改善後の記事を**HTML形式**で出力してください。以下の構造を守ってください：

```html
<h2>見出し1</h2>
<p>段落1...</p>

<h2>見出し2</h2>
<p>段落2...</p>

<h3>小見出し</h3>
<p>段落3...</p>

<h2>まとめ</h2>
<ul>
<li>ポイント1</li>
<li>ポイント2</li>
<li>ポイント3</li>
</ul>
```

**重要**: 出力は改善後のHTML本文のみとし、説明文や前書きは含めないでください。
"""

    return prompt


def prepare_posts():
    """バックアップJSONから記事を準備"""
    print("=" * 60)
    print("記事改善準備ツール")
    print("=" * 60)
    print()

    # 最新のバックアップファイルを見つける
    backup_file = find_latest_backup()
    print(f"📂 バックアップファイル: {backup_file}")

    # JSONを読み込む
    with open(backup_file, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)

    posts = backup_data['posts']
    print(f"📝 記事数: {len(posts)}")
    print()

    # 各記事をMarkdown形式に変換
    print("📄 記事をMarkdown形式に変換中...")
    print()

    for idx, post in enumerate(posts, 1):
        post_id = post['id']
        title = post['title']

        print(f"   [{idx}/{len(posts)}] 記事ID {post_id}: {title[:50]}...")

        # カテゴリとタグの文字列化
        categories_str = ', '.join([cat['name'] for cat in post['categories']])
        tags_str = ', '.join([tag['name'] for tag in post['tags']])

        # 本文をMarkdown形式に変換
        content_markdown = html_to_markdown(post['content_html'])

        # メタディスクリプションの表示
        meta_desc = post.get('meta_description', '')
        meta_desc_display = f"{meta_desc[:100]}..." if len(meta_desc) > 100 else meta_desc

        # Markdownファイルの内容を作成
        markdown_content = f"""# [{post_id}] {title}

**URL**: {post['url']}
**カテゴリ**: {categories_str or '未分類'}
**タグ**: {tags_str or 'なし'}
**現在の文字数**: {post['content_length']}文字
**メタディスクリプション**: {meta_desc_display}

---

## 本文

{content_markdown}

---

{create_improvement_prompt(post)}
"""

        # ファイルに保存
        output_file = f"posts_to_improve/post_{post_id}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

    print()
    print("✅ すべての記事をMarkdown形式に変換しました")
    print(f"   保存先: posts_to_improve/")
    print()
    print("=" * 60)
    print("次のステップ:")
    print("  improve_all_posts.py を実行して記事を自動改善してください")
    print("=" * 60)


def main():
    """メイン処理"""
    try:
        prepare_posts()
        return 0
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
