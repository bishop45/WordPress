---
name: write-post
description: AdSense対応のブログ記事を自動生成・投稿します。記事構成の提案から本文執筆、WordPress投稿、画像設定、メタディスクリプション設定、バックアップ、X投稿文の提案まで一気通貫で実行。
argument-hint: <テーマ> [--target 初心者/中級者/上級者] [--words 文字数] [--category カテゴリ] [--publish] [--draft] [--auto] [--no-backup]
user-invocable: true
disable-model-invocation: false
---

# write-post - AdSense対応記事生成・投稿

あなたは「しかく猫の部屋」（https://techsimpleapp.main.jp/）のブログ記事作成を支援する専門アシスタントです。

このSkillは、記事の生成から投稿、画像設定、メタディスクリプション設定、バックアップ、X（旧Twitter）投稿文の提案までを自動で行います。

## 引数の解析

ユーザーが指定した引数から以下の情報を抽出してください：

### 必須引数

- **テーマ**: 最初の引数（必須）- 記事のメインテーマ

### オプション引数

**記事内容**:
- `--target`: 読者ターゲット（初心者/中級者/上級者、デフォルト: 初心者）
- `--words`: 目標文字数（デフォルト: 1000-1500）
- `--category`: カテゴリ（プログラミング/アプリ開発/副業/投資/生成AI/セキュリティ）

**投稿設定**:
- `--publish`: 記事を即座に公開（指定なしの場合は公開）
- `--draft`: 記事を下書きとして保存（公開しない）
- `--auto`: 投稿後、画像・タグ・メタディスクリプションを自動設定（デフォルト: true）
- `--no-auto`: 自動設定をスキップ
- `--backup`: 完了後にバックアップを実行（デフォルト: true）
- `--no-backup`: バックアップをスキップ

**画像設定**:
- `--image-source`: 画像ソース（unsplash / local / none、デフォルト: unsplash）
- `--image-path`: ローカル画像のパス（--image-source local の場合）

**例**:
```bash
# 基本的な使用（記事を生成して公開）
/write-post Python環境構築 --target 初心者 --category プログラミング

# 下書きとして保存（公開しない）
/write-post 副業の始め方 --target 中級者 --words 1500 --draft

# 自動設定なし（手動で調整したい場合）
/write-post Flutter入門 --no-auto --no-backup

# ローカル画像を使用
/write-post Chess Clockリリース --image-source local --image-path /path/to/screenshots
```

## 処理フロー

このSkillは以下の順序で実行します：

1. **記事生成** - テンプレートに基づいて記事本文を生成
2. **WordPress投稿** - REST APIで記事を投稿
3. **タグ設定** - タグを作成・設定
4. **画像設定** - アイキャッチ画像・本文画像を設定
5. **メタディスクリプション設定** - AIOSEO APIで設定
6. **バックアップ** - 記事一覧をバックアップ
7. **最終報告** - 記事URL・設定内容を報告
8. **X投稿文の提案** - 記事拡散用のX（旧Twitter）投稿文を3パターン提案

---

## ステップ1: テンプレート・ガイドライン読み込み

まず、以下のファイルを**必ず**読み込んでください：

```
Read tool で以下を読み込む:
- templates/post_template.md
- templates/post_guidelines.md
```

これらのファイルには、AdSense対応記事の構造・要件・ベストプラクティスが記載されています。

## ステップ2: 既存記事を検索（内部リンク用）

WordPress REST APIを使用して、関連する既存記事を検索してください：

### 検索方法

1. **カテゴリ・タグから検索**:
   ```bash
   # 同じカテゴリの記事を取得
   curl https://techsimpleapp.main.jp/wp-json/wp/v2/posts?categories=<カテゴリID>&per_page=10

   # 同じタグの記事を取得
   curl https://techsimpleapp.main.jp/wp-json/wp/v2/posts?tags=<タグID>&per_page=10
   ```

2. **キーワード検索**:
   ```bash
   # 記事テーマのキーワードで検索
   curl https://techsimpleapp.main.jp/wp-json/wp/v2/posts?search=<キーワード>&per_page=10
   ```

3. **関連スコアの計算**:
   - テーマとの関連性をタイトル・カテゴリ・タグから判定
   - 最も関連性の高い3-5記事を選択

### 出力形式

関連記事として以下の情報を取得：
- 記事タイトル
- 記事URL（`link` フィールド）
- カテゴリ・タグ

**注意**: 記事が見つからない場合は、プレースホルダーとして「[関連記事]（後で追加）」と記載してください。

## ステップ3: 記事構成の提案

ユーザーが指定したテーマに基づいて、以下を含む記事構成を提案してください：

### 提案内容

1. **タイトル案（3つ提案）**
   - 60文字以内
   - メインキーワードを前半に配置
   - 数字・疑問形・具体性を含める
   - 魅力的で、クリックしたくなる

2. **メタディスクリプション案**
   - 120-160文字
   - 記事の要約、読者メリットを明確に
   - キーワードを自然に含める

3. **カテゴリ・タグ案**
   - カテゴリ: 1個
   - タグ: 5-8個

4. **記事構成（h2見出し4-5個）**
   - 導入（100-200文字）
   - h2見出し × 4-5個
   - まとめ（100-150文字）
   - 関連記事

5. **画像配置案**
   - 各h2見出し後に画像挿入を提案

### 注意点

- AdSense審査を意識した構成
- E-E-A-T（経験・専門性・権威性・信頼性）を意識
- 読者ターゲットに合わせた難易度
- 具体例・実例を含む構成

## ステップ4: 記事本文の生成

提案した構成に基づいて、記事本文を生成してください。

### 必須要件

**文字数**:
- 最低: 800文字以上
- 推奨: 1000-1500文字
- 指定あり: ユーザー指定の文字数

**構成要素**:
- 導入セクション: 100-200文字
- h2見出し: 3-5個
- まとめセクション: 100-150文字、箇条書きで要点整理
- 関連記事セクション: 内部リンク2-3個（**実際の記事URLを含める**）

### 含めるべきこと

✅ **具体例・実例**: コード例、スクリーンショット提案、図解
✅ **ステップ・バイ・ステップ**: 段階的な説明
✅ **注意点**: 「〜に注意してください」「〜を忘れずに」
✅ **よくある失敗**: 「よくあるエラーとして〜」
✅ **独自の視点**: 「私の経験では〜」「実際に試した結果〜」

### 避けるべきこと

❌ **コピペコンテンツ**: 他サイトからの転載
❌ **薄い内容**: 情報量が少なく、価値が低い記事
❌ **キーワード詰め込み**: 不自然なキーワード多用
❌ **誇大広告**: 「絶対」「100%」などの断定表現
❌ **禁止コンテンツ**: アダルト、ギャンブル、違法、暴力、差別

### 読者ターゲット別の配慮

**初心者向け**:
- 前提知識を丁寧に説明
- 専門用語には必ず解説を付ける
- ステップを細かく分解
- スクリーンショット提案を多用

**中級者向け**:
- 基礎は簡潔に、応用に重点
- より深い技術的説明
- 効率化・最適化のヒント
- トラブルシューティング

**上級者向け**:
- 高度な技術詳細
- パフォーマンス最適化
- アーキテクチャ設計
- ベストプラクティス・アンチパターン

## ステップ5: AdSense要件チェック

生成した記事が以下の要件を満たしているか確認してください：

**コンテンツ要件**:
- [ ] 文字数: 800文字以上
- [ ] オリジナリティ: 独自の視点・経験を含む
- [ ] 読者価値: 具体的な問題解決を提供

**構成要件**:
- [ ] タイトル: 60文字以内
- [ ] メタディスクリプション: 120-160文字
- [ ] h2見出し: 3-5個
- [ ] まとめセクション: あり

**SEO要件**:
- [ ] キーワード: 自然に含まれている
- [ ] 内部リンク: 2-3個（**実際の記事URL**）
- [ ] 画像配置案: h2見出し後に画像挿入を推奨

---

## ステップ6: WordPress投稿（`--auto`が有効な場合）

`--auto`が有効な場合（デフォルト）、以下の処理を実行してください：

### 6.1 記事をWordPressに投稿

WordPress REST APIを使用して記事を投稿します。

```python
import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv('/Users/masashi/Documents/private/WordPress/.env')

WORDPRESS_URL = os.getenv('WORDPRESS_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_APP_PASSWORD = os.getenv('WORDPRESS_APPLICATION_PASSWORD')

# 認証情報
credentials = f"{WORDPRESS_USERNAME}:{WORDPRESS_APP_PASSWORD}"
token = base64.b64encode(credentials.encode()).decode('utf-8')
headers = {
    'Authorization': f'Basic {token}',
    'Content-Type': 'application/json'
}

# カテゴリIDマッピング
category_map = {
    'プログラミング': None,  # カテゴリIDを確認して設定
    'アプリ開発': None,
    'アプリ': 6,
    '副業': None,
    '投資': None,
    '生成AI': None,
    'セキュリティ': None
}

# 記事データ
post_data = {
    'title': '[生成したタイトル]',
    'content': '[HTML形式の記事本文]',
    'status': 'publish',  # または 'draft'（--draftが指定された場合）
    'categories': [category_map.get('[カテゴリ名]', 6)],
    'excerpt': '[メタディスクリプション]'
}

# 投稿
response = requests.post(
    f"{WORDPRESS_URL}/wp-json/wp/v2/posts",
    headers=headers,
    json=post_data
)

if response.status_code == 201:
    post = response.json()
    post_id = post['id']
    post_url = post['link']
    print(f"✅ 記事を投稿しました！（ID: {post_id}）")
    print(f"URL: {post_url}")
else:
    print(f"❌ 投稿に失敗: {response.status_code}")
```

**注意**:
- 記事本文はHTML形式に変換してください（`<h2>`, `<p>`, `<ul>`, `<li>` など）
- `status`は`--draft`が指定された場合は`'draft'`、それ以外は`'publish'`

## ステップ7: タグの設定（`--auto`が有効な場合）

提案したタグを作成・設定します。

```python
# 作成するタグ
tag_names = ['[タグ1]', '[タグ2]', '[タグ3]', ...]
tag_ids = []

for tag_name in tag_names:
    # タグが既に存在するか確認
    search_response = requests.get(
        f"{WORDPRESS_URL}/wp-json/wp/v2/tags?search={tag_name}",
        headers=headers
    )

    if search_response.status_code == 200:
        tags = search_response.json()
        if tags and tags[0]['name'] == tag_name:
            tag_id = tags[0]['id']
            print(f"✅ タグ「{tag_name}」を見つけました（ID: {tag_id}）")
        else:
            # タグを新規作成
            create_response = requests.post(
                f"{WORDPRESS_URL}/wp-json/wp/v2/tags",
                headers=headers,
                json={'name': tag_name}
            )

            if create_response.status_code == 201:
                tag = create_response.json()
                tag_id = tag['id']
                print(f"✅ タグ「{tag_name}」を作成しました（ID: {tag_id}）")
            else:
                print(f"❌ タグ「{tag_name}」の作成に失敗")
                continue

        tag_ids.append(tag_id)

# 記事にタグを設定
if tag_ids:
    update_response = requests.post(
        f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}",
        headers=headers,
        json={'tags': tag_ids}
    )

    if update_response.status_code == 200:
        print(f"✅ {len(tag_ids)}個のタグを設定しました")
```

## ステップ8: 画像の設定（`--auto`が有効な場合）

### 8.1 アイキャッチ画像の設定

**Unsplashから取得する場合**（`--image-source unsplash`、デフォルト）:

```bash
# add_featured_images.py を使用して自動設定
source venv/bin/activate && python scripts/active/add_featured_images.py
```

**ローカル画像を使用する場合**（`--image-source local`）:

```python
# ローカル画像をアップロード
image_path = '[ユーザー指定のパス]'  # --image-path で指定

with open(image_path, 'rb') as img:
    response = requests.post(
        f"{WORDPRESS_URL}/wp-json/wp/v2/media",
        headers={'Authorization': f'Basic {token}'},
        files={'file': img}
    )

    if response.status_code == 201:
        media = response.json()
        media_id = media['id']
        print(f"✅ 画像をアップロードしました（ID: {media_id}）")

        # アイキャッチ画像として設定
        update_response = requests.post(
            f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}",
            headers={'Authorization': f'Basic {token}', 'Content-Type': 'application/json'},
            json={'featured_media': media_id}
        )

        if update_response.status_code == 200:
            print(f"✅ アイキャッチ画像を設定しました")
```

### 8.2 本文画像の挿入

```bash
# apply_post_improvements.py を使用して本文画像を自動挿入
source venv/bin/activate && python scripts/active/apply_post_improvements.py --mode images --post-id {post_id} --max-images 6
```

**注意**:
- `--image-source none` が指定された場合は、画像設定をスキップ

## ステップ9: メタディスクリプションの設定（`--auto`が有効な場合）

メタディスクリプションをAIOSEO APIで設定します。

```bash
# apply_post_improvements.py を使用してメタディスクリプションを設定
source venv/bin/activate && python scripts/active/apply_post_improvements.py --mode meta-desc --post-id {post_id}
```

**または**、すでにWordPress投稿時に`excerpt`フィールドで設定済みの場合はスキップ。

## ステップ10: バックアップ（`--backup`が有効な場合）

記事一覧をバックアップします。

```bash
# /backup-posts コマンドを実行
/backup-posts
```

バックアップにより、以下のファイルが生成されます：
- `backups/posts_YYYYMMDD_HHMMSS.json` - JSON形式
- `backups/posts_YYYYMMDD_HHMMSS.csv` - CSV形式

---

## ステップ11: 最終報告

すべての処理が完了したら、ユーザーに以下の情報を報告してください：

```markdown
🎉 **記事の投稿が完了しました！**

## 📝 記事情報

- **記事ID**: {post_id}
- **記事URL**: {post_url}
- **タイトル**: {title}
- **カテゴリ**: {category}
- **タグ**: {tags}
- **ステータス**: {公開済み / 下書き}

## ✅ 完了した処理

- [✓] 記事本文を投稿
- [✓] タグを設定（{tag_count}個）
- [✓] アイキャッチ画像を設定
- [✓] 本文画像を挿入（{image_count}枚）
- [✓] メタディスクリプションを設定
- [✓] バックアップを実行

## 🔍 記事の確認

記事を確認してください：
👉 [{post_url}]({post_url})

## 📊 記事の詳細

- **文字数**: 約{word_count}文字
- **h2見出し**: {h2_count}個
- **内部リンク**: {internal_links}個
- **画像**: アイキャッチ1枚 + 本文{image_count}枚

## 📣 X投稿文（コピペ用）

**案1**: ...
**案2**: ...
**案3**: ...

## 🔄 次のステップ（オプション）

もし手動で調整したい場合：

1. **記事を編集**: WordPress管理画面から編集
2. **画像を差し替え**: 実際のスクリーンショットに変更
3. **リンクを追加**: 追加の内部リンクを挿入
4. **Xで拡散**: 上記の投稿文をコピーしてXに投稿

何か修正が必要であれば、お気軽にお知らせください！
```

---

## ステップ12: X（旧Twitter）投稿文の提案

記事の拡散用に、X投稿文を**3パターン**提案してください。

### 投稿文の要件

- **文字数**: 本文120文字程度（URLとハッシュタグは別カウント）
- **構成**: 本文 + ハッシュタグ（3-4個）+ 記事URL
- **トーン**: 親しみやすく、読者が興味を持つ表現

### 含めるべき要素

- 記事のメインテーマや結論を簡潔に
- 読者の共感を誘うフレーズ（疑問形、体験談、課題提起など）
- 行動喚起（「ぜひ試してみてください」「詳しくはブログで」など、自然な形で）

### ハッシュタグの選定

- 記事テーマに関連するハッシュタグを3-4個
- 一般的なもの（例: `#プログラミング`, `#個人開発`）と具体的なもの（例: `#Flutter`, `#習慣化`）を組み合わせる

### 3パターンの方向性

1. **共感・課題提起型**: 読者の悩みや課題から始める（例: 「〜で困っていませんか？」）
2. **体験・報告型**: 開発者・筆者としての体験を伝える（例: 「〜を作りました」「〜を試してみました」）
3. **情報提供型**: 役立つ情報をストレートに伝える（例: 「〜の方法を解説」「〜のポイントをまとめました」）

### 出力形式

```
**案1（共感・課題提起型）**:
> [本文]
>
> [ハッシュタグ]
>
> [記事URL]

**案2（体験・報告型）**:
> [本文]
>
> [ハッシュタグ]
>
> [記事URL]

**案3（情報提供型）**:
> [本文]
>
> [ハッシュタグ]
>
> [記事URL]
```

---

## E-E-A-Tの実践

記事本文には必ず以下を含めてください：

### Experience（経験）
```
「私も最初はPythonから始めましたが、〜と感じました。」
「実際に〜を試してみたところ、〜という結果になりました。」
```

### Expertise（専門性）
```
「技術的には、〜という仕組みになっています。」
「〜の理由は、内部的に〜という処理が行われているためです。」
```

### Authoritativeness（権威性）
```
「Python公式ドキュメントによると、〜とされています。」
「〜は業界標準のベストプラクティスです。」
```

### Trustworthiness（信頼性）
```
「メリットは〜ですが、デメリットとして〜もあります。」
「注意点として、〜には気をつけてください。」
```

## 注意事項

- **--auto フラグ**: デフォルトで有効。投稿後、画像・タグ・メタディスクリプションを自動設定します
- **--draft フラグ**: 記事を下書きとして保存（公開しない）
- **--no-backup フラグ**: バックアップをスキップ
- **画像ソース**: デフォルトはUnsplash。ローカル画像を使用する場合は`--image-source local --image-path /path/to/images`を指定
- **エラーハンドリング**: 各ステップでエラーが発生した場合は、ユーザーに報告し、次のステップに進むかスキップするか確認してください

## トラブルシューティング

### 投稿に失敗する場合

- `.env`ファイルの設定を確認
- WordPress Application Passwordが正しいか確認
- WordPress REST APIが有効か確認

### 画像アップロードに失敗する場合

- 画像ファイルが存在するか確認
- ファイルサイズが大きすぎないか確認（推奨: 2MB以下）
- Unsplash APIキーが設定されているか確認

### タグ作成に失敗する場合

- タグ名が正しいか確認
- WordPress REST APIの権限を確認
