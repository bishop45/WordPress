---
name: backup-posts
description: WordPress記事一覧をバックアップします。記事作成・更新後に実行することで、記事データの履歴を保存できます。
disable-model-invocation: true
---

# 記事一覧バックアップ

WordPress REST APIを使用して、全記事のメタデータをバックアップします。

## 実行内容

### 1. 記事データ取得

WordPress REST APIで全記事を取得：

```bash
# 全記事を取得（ページネーション対応）
curl "https://techsimpleapp.main.jp/wp-json/wp/v2/posts?per_page=100&page=1"
```

### 2. バックアップファイル作成

`backups/` ディレクトリに以下の形式でバックアップを作成：

```
backups/
├── posts_backup_YYYYMMDD_HHMMSS.json    # 完全なJSON形式
└── posts_backup_YYYYMMDD_HHMMSS.csv     # 人間が読みやすいCSV形式
```

### 3. バックアップ内容

各記事について以下の情報を保存：

**JSON形式**（完全なデータ）:
- ID
- タイトル
- URL（link）
- ステータス（status）
- 公開日時（date）
- 更新日時（modified）
- 著者（author）
- カテゴリ（categories）
- タグ（tags）
- 抜粋（excerpt）
- 文字数（content length）
- アイキャッチ画像ID（featured_media）
- メタディスクリプション（yoast_head_json.description）

**CSV形式**（主要データのみ）:
- ID
- タイトル
- URL
- ステータス
- 公開日
- 更新日
- カテゴリ数
- タグ数
- 文字数
- アイキャッチ画像有無

## 実行方法

### Python スクリプト実行

`scripts/active/` に新しいスクリプトを作成して実行：

```python
#!/usr/bin/env python3
"""WordPress記事一覧バックアップスクリプト"""

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
    """全記事を取得"""
    posts = []
    page = 1
    per_page = 100

    while True:
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"
        params = {'per_page': per_page, 'page': page}

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        batch = response.json()
        if not batch:
            break

        posts.extend(batch)

        # 次のページがあるかチェック
        total_pages = int(response.headers.get('X-WP-TotalPages', 1))
        if page >= total_pages:
            break

        page += 1

    return posts

def save_json_backup(posts, timestamp):
    """JSON形式でバックアップ"""
    filename = BACKUP_DIR / f"posts_backup_{timestamp}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"✓ JSON backup saved: {filename}")
    return filename

def save_csv_backup(posts, timestamp):
    """CSV形式でバックアップ"""
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
                post.get('date', '').split('T')[0],
                post.get('modified', '').split('T')[0],
                len(post.get('categories', [])),
                len(post.get('tags', [])),
                len(content),
                '✓' if post.get('featured_media') else '✗'
            ])

    print(f"✓ CSV backup saved: {filename}")
    return filename

def main():
    print("🔄 記事一覧を取得中...")
    posts = get_all_posts()
    print(f"✓ {len(posts)}件の記事を取得しました")

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    print("\n💾 バックアップを保存中...")
    json_file = save_json_backup(posts, timestamp)
    csv_file = save_csv_backup(posts, timestamp)

    print(f"\n✅ バックアップ完了！")
    print(f"  - JSON: {json_file}")
    print(f"  - CSV: {csv_file}")
    print(f"  - 記事数: {len(posts)}件")

if __name__ == '__main__':
    main()
```

### 実行コマンド

```bash
# Python環境で実行
python scripts/active/backup_posts.py
```

## 出力例

```
🔄 記事一覧を取得中...
✓ 21件の記事を取得しました

💾 バックアップを保存中...
✓ JSON backup saved: backups/posts_backup_20260215_143022.json
✓ CSV backup saved: backups/posts_backup_20260215_143022.csv

✅ バックアップ完了！
  - JSON: backups/posts_backup_20260215_143022.json
  - CSV: backups/posts_backup_20260215_143022.csv
  - 記事数: 21件
```

## バックアップの活用

### 1. 記事数の推移を追跡

```bash
# CSV形式で確認
cat backups/posts_backup_20260215_143022.csv | wc -l
```

### 2. 差分比較

```bash
# 最新2つのバックアップを比較
diff backups/posts_backup_20260215_143022.csv backups/posts_backup_20260215_150000.csv
```

### 3. 記事分析

CSVファイルをExcel・Google Sheetsで開いて分析：
- 記事数の推移
- カテゴリ・タグの分布
- 文字数の統計
- アイキャッチ画像設定率

## 推奨運用

### バックアップタイミング

1. **記事作成後**: 必ず実行
2. **記事更新後**: できるだけ実行
3. **定期バックアップ**: 週1回程度

### バックアップ保存期間

- **最新3ヶ月**: すべて保持
- **3ヶ月〜1年**: 月1回のみ保持
- **1年以上**: 削除

## 注意事項

- バックアップは `backups/` ディレクトリに保存されます（`.gitignore` で除外済み）
- 大量の記事がある場合、APIリクエストに時間がかかることがあります
- WordPress REST APIの制限（通常100件/ページ）に注意してください
- JSON形式は完全なデータ、CSV形式は主要データのみです

## トラブルシューティング

### エラー: Connection timeout
- ネットワーク接続を確認
- WordPress サイトが正常に稼働しているか確認

### エラー: Permission denied
- `backups/` ディレクトリの書き込み権限を確認
- `mkdir -p backups` で作成

### エラー: API rate limit
- リクエスト間隔を調整（`time.sleep(1)` を追加）
