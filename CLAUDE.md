# しかく猫の部屋 - WordPress ブログ管理

## プロジェクト概要

**ブログ名**: しかく猫の部屋
**URL**: https://techsimpleapp.main.jp/
**テーマ**: プログラミング、アプリ開発、副業、投資、生成AI、セキュリティなどの技術系コンテンツ
**目標**: Google AdSense審査合格

---

## ✅ 完了済み: Phase 1 + Phase 2 + Phase 3（すべて完了 🎉）

### Phase 1 + Phase 2.3: 既存記事の改善 ✅

**達成内容**:
- ✅ 公開記事数: 21記事（目標20-30記事達成）
- ✅ 全記事800文字以上（最短890文字）
- ✅ アイキャッチ画像: 全21記事に設定済み
- ✅ 本文画像: 全21記事に各3枚（計63枚）
- ✅ メタディスクリプション: 全21記事（120-160文字）
- ✅ まとめセクション: 全21記事
- ✅ カテゴリ・タグ: 全記事に適切に設定

### Phase 2: 必須ページ作成 ✅

**達成内容**:
- ✅ プライバシーポリシー: AdSense・Analytics利用明記済み
- ✅ お問い合わせページ: Google Forms埋め込み完了（iFrame）
- ✅ プロフィールページ: 運営者情報・経歴・専門性セクション追加
- ✅ フッターメニュー整備: 手動設定完了（2026年2月15日）
- ✅ Google Analytics設定: 完了（2026年2月15日）

### Phase 3: 技術・SEO対策 ✅

**達成内容**:
- ✅ Google Search Console登録: 完了（2026年2月15日）
- ✅ XMLサイトマップ送信: 完了（2026年2月15日）
- ✅ モバイル表示確認: 完了（2026年2月15日）
- ✅ ページ速度確認: 完了（2026年2月15日）
- ✅ リンク切れ確認: 完了（2026年2月15日）

## 🚀 次のステップ: Phase 4（AdSense申請）

**審査申請の準備が整いました！** 詳細は [今後の作業ロードマップ](#今後の作業ロードマップ)を参照

---

## このリポジトリについて

このリポジトリは、WordPressブログ「しかく猫の部屋」の運営を支援するツール群を管理しています。

### ファイル構成

```
WordPress/
├── CLAUDE.md                      # このファイル（プロジェクト詳細ガイド）
├── README.md                      # クイックスタートガイド
├── .env                          # 環境変数（APIキー、認証情報）
├── .gitignore                    # Git除外設定
├── requirements.txt              # Python依存パッケージ
├── .claude/                      # Claude Code設定
│   ├── settings.local.json      # ローカル設定
│   └── skills/                  # プロジェクト固有Skills
│       └── write-post/          # 記事作成Skill
│           └── skillDefinition.md
├── docs/                         # ドキュメント
│   ├── TODO_NEXT_STEPS.md       # 次のステップと作業計画
│   ├── PHASE3_GUIDE.md          # Phase 3（技術・SEO対策）実施ガイド
│   └── PHASE4_GUIDE.md          # Phase 4（AdSense申請）実施ガイド
├── scripts/                      # スクリプト
│   ├── active/                  # アクティブなスクリプト
│   │   ├── add_featured_images.py
│   │   ├── improve_post_structure.py
│   │   ├── apply_post_improvements.py
│   │   ├── update_pages.py
│   │   ├── verify_site.py
│   │   └── final_check.py
│   └── archive/                 # 古いスクリプト（アーカイブ）
├── templates/                    # 記事作成テンプレート
│   ├── post_template.md         # AdSense対応記事テンプレート
│   └── post_guidelines.md       # 記事作成ガイドライン
├── reports/                      # 分析レポート出力先
├── backups/                      # バックアップファイル
├── archive/                      # 作業用一時ファイル（アーカイブ）
└── venv/                         # Python仮想環境
```

### Claude Code Skills & Commands（NEW! 🚀）

Claude Code を拡張するための Skills と Commands を整備しました。詳細は [.claude/README.md](.claude/README.md) を参照してください。

#### Skills（複雑なタスク向け）

**write-post Skill** - AdSense対応記事生成

AdSense対応のブログ記事を自動生成するSkillです。テンプレートとガイドラインに基づいて、記事の構成から本文まで一括生成します。

**使用方法**:
```bash
/write-post <テーマ> [--target 初心者/中級者/上級者] [--words 文字数] [--category カテゴリ]
```

**使用例**:
```bash
# Python環境構築の記事を初心者向けに生成
/write-post Python環境構築 --target 初心者 --category プログラミング

# 副業の記事を中級者向けに1500文字で生成
/write-post 副業の始め方 --target 中級者 --words 1500
```

**生成内容**:
- タイトル案（3つ）+ メタディスクリプション
- カテゴリ・タグ提案
- 記事構成（h2見出し4-5個）
- 記事本文（800文字以上）
- まとめセクション
- AdSense要件チェックリスト

**次のステップ**:
```bash
python scripts/active/add_featured_images.py
python scripts/active/apply_post_improvements.py --mode all
```

#### Commands（シンプルなタスク向け）

**check-adsense** - AdSense要件チェック
```bash
/check-adsense <記事URL または 記事ID>
```
記事がAdSense審査要件を満たしているか確認し、合格/要改善/不合格の判定と改善提案を提供。

**analyze-post** - 記事分析
```bash
/analyze-post <記事URL または 記事ID>
```
SEO・可読性・コンテンツ品質を分析し、優先度別の改善提案と総合スコアを提供。

**quick-fix** - クイックフィックス
```bash
/quick-fix <記事ID>
```
メタディスクリプション、画像、まとめ、内部リンクなどの一般的な問題を自動修正。

**詳細**: [.claude/README.md](.claude/README.md) を参照

---

### 主要ツール

#### add_featured_images.py
WordPress記事にUnsplashから適切な画像を自動的に取得してアイキャッチ画像として設定するスクリプト。

**機能**:
- WordPress REST APIで全記事を取得
- アイキャッチ画像がない記事を自動検出
- 記事タイトルから関連キーワードを抽出（日本語→英語マッピング対応）
- Unsplash APIで画像検索
- WordPressメディアライブラリにアップロード
- アイキャッチ画像として自動設定
- APIレート制限の自動管理

#### improve_post_structure.py
記事の構造を分析し、改善提案を生成するスクリプト。

**機能**:
- **記事構造分析** (`--mode analyze`)
  - メタディスクリプション設定状況
  - 本文中の画像数
  - 内部リンク数
  - まとめセクションの有無
  - 改善推奨度の判定
  - CSVレポート出力
- **内部リンク提案** (`--mode suggest-links`)
  - Jaccard係数による記事間類似度計算
  - 関連記事の自動提案
  - CSVレポート出力

#### apply_post_improvements.py
記事の改善を自動的に適用するスクリプト。**全21記事への適用完了済み ✅**

**基本コマンド**:
```bash
# DRY RUN（プレビューのみ）
python apply_post_improvements.py --mode all --dry-run

# 実際に適用
python apply_post_improvements.py --mode all
```

**主な機能**:
- メタディスクリプション自動設定（120-160文字、AIOSEO API経由）
- まとめセクション自動追加（見出しから要点抽出）
- 内部リンク自動追加（関連記事セクション作成）
- 本文画像自動追加（Unsplash API、h2見出し後に挿入）

#### update_pages.py（NEW!）
固定ページ（お問い合わせ、プロフィールなど）を更新するスクリプト。**AdSense審査対策に使用 ✅**

**基本コマンド**:
```bash
# お問い合わせページのみ更新（DRY RUN）
python update_pages.py --mode contact --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8" --dry-run

# プロフィールページのみ更新（DRY RUN）
python update_pages.py --mode profile --dry-run

# 両方を更新（DRY RUN）
python update_pages.py --mode all --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8" --dry-run

# 実際に更新
python update_pages.py --mode all --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8"
```

**主な機能**:
- お問い合わせページにGoogle FormsをiFrameで埋め込み（サイト内完結型）
- プロフィールページに運営者情報セクションを追加（運営者名、運営形態、運営開始時期）
- プロフィールページに経歴・専門性セクションを追加（IT業界経験、資格活用例、プロジェクト実績）
- プロフィールページにブログの目的セクションを追加
- DRY RUNモードでプレビュー確認可能

**適用済み**: お問い合わせページ（ID: 199）、プロフィールページ（ID: 2）

#### verify_site.py（NEW! Phase 3用）
サイトの技術・SEO要件を自動検証するスクリプト。**Phase 3の実施前に実行推奨 ✅**

**基本コマンド**:
```bash
# サイト検証を実行
python verify_site.py
```

**主な機能**:
- XMLサイトマップの存在確認（複数パターン対応）
- robots.txtの確認と内容表示
- 必須ページの存在確認（トップ、プロフィール、プライバシーポリシー、お問い合わせ）
- HTTPS対応確認
- レスポンスタイム測定
- Phase 3の次のステップ案内（Google Search Console、PageSpeed Insightsなど）

**出力例**:
```
✓ wp-sitemap.xml が見つかりました
✓ 必須ページ: プロフィール OK
✓ HTTPS対応済みです
```

#### final_check.py（NEW! Phase 4用）
AdSense申請前の最終チェックスクリプト。**Phase 4の申請前に実行推奨 ✅**

**基本コマンド**:
```bash
# 最終チェックを実行
python final_check.py
```

**主な機能**:
- Phase 1-3のすべての項目を自動チェック
- 記事数・文字数・アイキャッチ画像の確認
- 必須ページの存在確認
- HTTPS・XMLサイトマップ・robots.txtの確認
- 合格/不合格の判定と改善提案
- AdSense申請準備完了の最終確認

**出力例**:
```
✓ 記事数: 21記事（目標20-30記事達成）
✓ プライバシーポリシー: 存在します
✓ HTTPS: 対応済み
🎉 おめでとうございます！AdSense申請の準備完了です！
```

---

## 環境設定

### 1. Python環境のセットアップ

```bash
# Python 3.13推奨
python3 -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 2. .envファイルの設定

プロジェクトルートに`.env`ファイルを作成し、以下の環境変数を設定：

```bash
# WordPress設定
WORDPRESS_URL=https://techsimpleapp.main.jp
WORDPRESS_USERNAME=あなたのWordPressユーザー名
WORDPRESS_APPLICATION_PASSWORD=アプリケーションパスワード

# Unsplash API設定
UNSPLASH_APPLICATION_ID=あなたのアプリケーションID
UNSPLASH_ACCESS_KEY=あなたのアクセスキー
UNSPLASH_SECRET_KEY=あなたのシークレットキー
```

**WordPressアプリケーションパスワードの取得方法**:
1. WordPressダッシュボード → ユーザー → プロフィール
2. 「アプリケーションパスワード」セクションで新規作成
3. 生成されたパスワードを`.env`に設定

**Unsplash APIキーの取得方法**:
1. https://unsplash.com/developers にアクセス
2. 「Register as a developer」でアカウント作成
3. 「New Application」で新しいアプリを登録
4. Access Key / Secret Keyを`.env`に設定

⚠️ **セキュリティ注意**: `.env`ファイルは`.gitignore`に含まれており、Gitにコミットされません。

---

## ツールの使用方法

### Phase 4: AdSense申請準備（現在のステップ）

**申請前の最終チェック**
```bash
# 最終チェックを実行（Phase 4申請前に必須）
python scripts/active/final_check.py
```

詳細な手順は [docs/PHASE4_GUIDE.md](docs/PHASE4_GUIDE.md) を参照してください。

### Phase 3: サイト検証（完了 ✅）

**サイトの技術・SEO要件を確認**
```bash
# サイト検証を実行（Phase 3実施前に推奨）
python scripts/active/verify_site.py
```

詳細な手順は [docs/PHASE3_GUIDE.md](docs/PHASE3_GUIDE.md) を参照してください。

### 新規記事作成時のワークフロー

**✅ 既存記事への改善は完了済み**。新規記事作成時は以下のワークフローを使用してください。

#### 方法1: Claude Code Skillを使用（推奨）

```bash
# write-post Skillで記事を生成
/write-post [テーマ] --target [初心者/中級者/上級者] --category [カテゴリ]

# 例
/write-post Python環境構築 --target 初心者 --category プログラミング
```

生成された記事をWordPressに投稿後、自動最適化スクリプトを実行：

```bash
# アイキャッチ画像設定
python scripts/active/add_featured_images.py

# 記事改善の一括適用
python scripts/active/apply_post_improvements.py --mode all --dry-run
python scripts/active/apply_post_improvements.py --mode all
```

#### 方法2: 手動作成

```bash
# 1. テンプレートを確認
cat templates/post_template.md
cat templates/post_guidelines.md

# 2. WordPress管理画面で記事を作成・公開

# 3. アイキャッチ画像設定
python scripts/active/add_featured_images.py

# 4. 記事改善の一括適用
python scripts/active/apply_post_improvements.py --mode all --dry-run
python scripts/active/apply_post_improvements.py --mode all
```

### 記事構造の分析（必要時のみ）

```bash
# 記事構造分析レポート生成
python scripts/active/improve_post_structure.py --mode analyze

# 内部リンク提案生成
python scripts/active/improve_post_structure.py --mode suggest-links
```

詳細な使用方法は各スクリプトファイルのコメントを参照してください。

---

## Google AdSense審査要件チェックリスト

### ✅ コンテンツ要件（完了）

- [x] 記事数: 21記事
- [x] 文字数: 全記事800文字以上
- [x] オリジナリティ: 独自コンテンツ
- [x] 画像: アイキャッチ21枚 + 本文63枚
- [x] カテゴリ・タグ整理済み
- [x] メタディスクリプション設定済み

### ✅ 必須ページ（完了）

- [x] **プライバシーポリシー**: AdSense・Analytics利用を明記済み
- [x] **お問い合わせページ**: Google Forms埋め込み完了（iFrame）
- [x] **運営者情報**: プロフィール充実化完了（運営者情報、経歴・専門性、ブログの目的）
- [x] **フッターメニュー**: 手動設定完了 ✅

### ✅ 技術・SEO設定（Phase 3 - 完了）

- [x] HTTPS化済み
- [x] **Google Analytics設定** ✅ 完了
- [x] **Google Search Console登録** ✅ 完了
- [x] **XMLサイトマップ送信** ✅ 完了
- [x] モバイル表示確認 ✅ 完了
- [x] ページ速度確認（PageSpeed Insights）✅ 完了
- [x] リンク切れ確認 ✅ 完了

### ✅ コンテンツポリシー遵守

- [x] 禁止コンテンツなし
- [x] 著作権遵守
- [x] オリジナルコンテンツ

---

## AdSense審査前チェック項目 - ✅ すべて完了！

### ✅ Phase 1: コンテンツ要件（完了）
- [x] 記事数21記事、全記事800文字以上
- [x] アイキャッチ画像・本文画像設定済み
- [x] カテゴリ・タグ整理済み
- [x] メタディスクリプション全記事設定済み

### ✅ Phase 2: 必須ページ（完了）
- [x] プライバシーポリシー（AdSense・Analytics明記）
- [x] お問い合わせページ
- [x] 運営者情報充実化
- [x] フッターメニュー整備
- [x] Google Analytics設定

### ✅ Phase 3: 技術・SEO対策（完了）
- [x] HTTPS化済み
- [x] Google Search Console登録
- [x] XMLサイトマップ送信
- [x] モバイル表示確認（モバイルフレンドリーテスト）
- [x] ページ速度確認（PageSpeed Insights）
- [x] リンク切れ確認

### 🚀 Phase 4: 次のステップ（AdSense申請）
**すべての準備が整いました！いつでもAdSense審査を申請できます。**

詳細な申請手順は次のセクションを参照してください。

---

## 今後の作業ロードマップ

### ✅ Phase 1-2.3: 既存記事改善（完了）
- [x] 21記事に整理（52記事を下書きに）
- [x] 全記事800文字以上
- [x] アイキャッチ画像・本文画像設定
- [x] メタディスクリプション・まとめセクション追加
- [x] カテゴリ・タグ整理

### Phase 2: 必須ページ作成 ✅ 完了（2026年2月15日）
1. [x] **プライバシーポリシーページ**
   - Cookie使用、AdSense、Analytics利用を明記済み
2. [x] **お問い合わせページ**
   - Google Forms埋め込み完了（iFrame）
3. [x] **運営者情報充実化**
   - プロフィールページに運営者情報・経歴・専門性セクション追加
4. [x] **フッターメニュー整備**
   - 手動設定完了 ✅
5. [x] **Google Analytics設定**
   - 完了 ✅

### Phase 3: 技術・SEO対策 ✅ 完了（2026年2月15日）
1. [x] **サイト検証実行**
   - `python verify_site.py` でサイト状態を確認 ✅
2. [x] **Google Search Console登録**
   - 完了 ✅
3. [x] **XMLサイトマップ送信**
   - 完了 ✅
4. [x] **モバイル表示確認**（モバイルフレンドリーテスト）
   - 完了 ✅
5. [x] **ページ速度確認**（PageSpeed Insights、目標50点以上）
   - 完了 ✅
6. [x] **リンク切れ確認**
   - 完了 ✅

### Phase 4: AdSense申請 🚀 次のステップ（Phase 1-3完了済み）
1. [x] **全チェックリスト確認** ✅ Phase 1-3すべて完了
2. [ ] **AdSenseアカウント作成・サイト登録**
   - https://www.google.com/adsense にアクセス
   - サイトURL登録: `https://techsimpleapp.main.jp`
3. [ ] **審査コード設置**
   - WordPressテーマのheader.phpに審査コード貼り付け
   - または「Site Kit by Google」プラグイン使用
4. [ ] **審査申請**
   - AdSenseダッシュボードから申請
5. [ ] **審査結果待ち**（通常1-2週間）
   - 結果をメールで受信
   - 合格後、広告コード設置

**準備完了！いつでも申請できる状態です 🎉**

---

## よくある質問

### Q: 記事数は何記事あればいいですか？
A: 明確な基準はありませんが、20-30記事以上が推奨されます。ただし、数よりも質が重要です。

### Q: どのくらいの期間運営すればいいですか？
A: 6ヶ月以上の運営が推奨されますが、必須ではありません。定期的に更新されているサイトであることが重要です。

### Q: 審査にかかる時間は？
A: 通常1-2週間ですが、場合によっては数日〜1ヶ月かかることもあります。

### Q: 審査に落ちた場合は？
A: 理由を確認し、改善してから再申請できます。再申請までに2週間程度空けることが推奨されます。

### Q: プライバシーポリシーはどう書けばいい？
A: WordPress用のプライバシーポリシージェネレーターを利用するか、既存のテンプレートをカスタマイズして使用できます。

---

## 参考リンク

### Google AdSense関連
- [Google AdSense ヘルプセンター](https://support.google.com/adsense/)
- [AdSense プログラムポリシー](https://support.google.com/adsense/answer/48182)
- [サイトの承認を受けるには](https://support.google.com/adsense/answer/9724)

### WordPress関連
- [WordPress プライバシーポリシーページ](https://ja.wordpress.org/support/article/privacy/)
- [Contact Form 7](https://ja.wordpress.org/plugins/contact-form-7/)（お問い合わせフォーム）

### SEO・技術関連
- [Google Search Console](https://search.google.com/search-console)
- [Google Analytics](https://analytics.google.com/)
- [PageSpeed Insights](https://pagespeed.web.dev/)（ページ速度測定）

### Unsplash
- [Unsplash Developers](https://unsplash.com/developers)
- [Unsplash API Documentation](https://unsplash.com/documentation)
- [Unsplash License](https://unsplash.com/license)（利用規約）

---

## 開発・運用コマンド

```bash
# Python仮想環境の有効化
source venv/bin/activate

# === Phase 4: AdSense申請準備 ===
# 申請前最終チェック（Phase 1-3のすべての項目を確認）
python scripts/active/final_check.py

# === Phase 3: サイト検証 ===
# サイト検証（XMLサイトマップ、robots.txt、必須ページ、HTTPS確認）
python scripts/active/verify_site.py

# === 記事管理 ===
# アイキャッチ画像の一括設定
python scripts/active/add_featured_images.py

# 記事構造分析レポート生成
python scripts/active/improve_post_structure.py --mode analyze

# 内部リンク提案生成
python scripts/active/improve_post_structure.py --mode suggest-links

# 記事改善の自動適用（DRY RUNモードで確認）
python scripts/active/apply_post_improvements.py --mode all --dry-run

# 記事改善の自動適用（実行）
python scripts/active/apply_post_improvements.py --mode all

# === 固定ページ管理 ===
# 固定ページ更新（お問い合わせ・プロフィール）
python scripts/active/update_pages.py --mode all --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8" --dry-run
python scripts/active/update_pages.py --mode all --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8"

# === 環境管理 ===
# 依存パッケージのアップデート
pip install --upgrade -r requirements.txt

# 新しい依存パッケージを追加した場合
pip freeze > requirements.txt

# 仮想環境の無効化
deactivate
```

---

## フッターメニュー設定手順 ✅ 完了済み（2026年2月15日）

> **注意**: このセクションは完了済みです。新規サイト構築時の参考用に残しています。

### ステップ1: メニュー作成

1. WordPressダッシュボードにログイン
2. **外観 → メニュー** をクリック
3. 「新しいメニューを作成しましょう」をクリック
4. **メニュー名**: 「フッターメニュー」と入力
5. 「メニューを作成」をクリック

### ステップ2: ページを追加

左側の「固定ページ」セクションから以下の4つのページを選択して「メニューに追加」:

- ✅ プロフィール
- ✅ 所有資格
- ✅ プライバシーポリシー
- ✅ お問い合わせ

### ステップ3: メニューの位置を設定

1. 「メニュー設定」セクションで **「フッターメニュー」** にチェックを入れる
2. 「メニューを保存」をクリック

### ステップ4: 確認

1. サイトにアクセス: https://techsimpleapp.main.jp/
2. ページのフッター部分に4つのリンクが表示されていることを確認
3. 各リンクをクリックして、正しいページに遷移することを確認

**注意**: テーマによってはフッターメニューがサポートされていない場合があります。その場合は「外観 → ウィジェット」からフッターエリアに「ナビゲーションメニュー」ウィジェットを追加してください。

---

## ライセンスと利用規約

### Unsplash画像の利用
- このプロジェクトで使用する画像はUnsplash APIを通じて取得されます
- Unsplashの画像は無料で利用できますが、[Unsplash License](https://unsplash.com/license)に従う必要があります
- 画像の著作者表示が自動的に設定されます（"Photo by [photographer] on Unsplash"）

### このリポジトリ
- 個人利用・学習目的での使用を想定しています
- APIキーや認証情報は絶対に公開しないでください

---

## サポート・問い合わせ

ブログ: https://techsimpleapp.main.jp/

---

**最終更新**: 2026年2月15日
**作成者**: しかく猫の部屋 運営者

詳細な作業履歴は [TODO_NEXT_STEPS.md](TODO_NEXT_STEPS.md) を参照してください。
