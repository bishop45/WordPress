# しかく猫の部屋 - WordPress ブログ管理

## プロジェクト概要

**ブログ名**: しかく猫の部屋
**URL**: https://techsimpleapp.main.jp/
**テーマ**: プログラミング、アプリ開発、副業、投資、生成AI、セキュリティなどの技術系コンテンツ
**目標**: Google AdSense審査合格

---

## ✅ 完了済み: Phase 1 + Phase 2（ほぼ完了）

### Phase 1 + Phase 2.3: 既存記事の改善

**現在の状態**:
- ✅ 公開記事数: 21記事（目標20-30記事達成）
- ✅ 全記事800文字以上（最短890文字）
- ✅ アイキャッチ画像: 全21記事に設定済み
- ✅ 本文画像: 全21記事に各3枚（計63枚）
- ✅ メタディスクリプション: 全21記事（120-160文字）
- ✅ まとめセクション: 全21記事
- ✅ カテゴリ・タグ: 全記事に適切に設定

### Phase 2: 必須ページ作成（ほぼ完了）

**達成済み**:
- ✅ プライバシーポリシー: AdSense・Analytics利用明記済み
- ✅ お問い合わせページ: Google Forms埋め込み完了（iFrame）
- ✅ プロフィールページ: 運営者情報・経歴・専門性セクション追加
- ⚠️ フッターメニュー整備: 手動設定が必要（[設定手順](#フッターメニュー設定手順)参照）

**次のステップ**: [今後の作業ロードマップ](#今後の作業ロードマップ)を参照

---

## このリポジトリについて

このリポジトリは、WordPressブログ「しかく猫の部屋」の運営を支援するツール群を管理しています。

### ファイル構成

```
WordPress/
├── CLAUDE.md                      # このファイル
├── TODO_NEXT_STEPS.md            # 次のステップと作業計画
├── .env                          # 環境変数（APIキー、認証情報）
├── .gitignore                    # Git除外設定
├── requirements.txt              # Python依存パッケージ
├── add_featured_images.py        # アイキャッチ画像自動設定スクリプト
├── improve_post_structure.py     # 記事構造分析・内部リンク提案スクリプト
├── apply_post_improvements.py    # 記事改善自動適用スクリプト
├── update_pages.py               # 固定ページ更新スクリプト（NEW!）
├── reports/                      # 分析レポート出力先
└── venv/                         # Python仮想環境
```

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

**✅ 既存記事への改善は完了済み**。新規記事作成時のみ以下のツールを使用してください。

### 新規記事作成時のワークフロー

```bash
# 1. アイキャッチ画像設定（画像がない記事のみ）
python add_featured_images.py

# 2. 記事改善の一括適用（DRY RUNで確認）
python apply_post_improvements.py --mode all --dry-run

# 3. 問題なければ実行
python apply_post_improvements.py --mode all
```

### 記事構造の分析（必要時のみ）

```bash
# 記事構造分析レポート生成
python improve_post_structure.py --mode analyze

# 内部リンク提案生成
python improve_post_structure.py --mode suggest-links
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

### ✅ 必須ページ（ほぼ完了）

- [x] **プライバシーポリシー**: AdSense・Analytics利用を明記済み
- [x] **お問い合わせページ**: Google Forms埋め込み完了（iFrame）
- [x] **運営者情報**: プロフィール充実化完了（運営者情報、経歴・専門性、ブログの目的）
- [ ] **フッターメニュー**: 手動設定が必要（[設定手順](#フッターメニュー設定手順)参照）

### ⚠️ 技術・SEO設定（次のステップ）

- [x] HTTPS化済み
- [ ] **Google Search Console登録**
- [ ] **XMLサイトマップ送信**
- [ ] **Google Analytics設定**
- [ ] モバイル表示確認
- [ ] ページ速度確認（PageSpeed Insights）

### ✅ コンテンツポリシー遵守

- [x] 禁止コンテンツなし
- [x] 著作権遵守
- [x] オリジナルコンテンツ

---

## AdSense審査前チェック項目

### ✅ 完了項目
- [x] 記事数21記事、全記事800文字以上
- [x] アイキャッチ画像・本文画像設定済み
- [x] カテゴリ・タグ整理済み
- [x] メタディスクリプション全記事設定済み
- [x] HTTPS化済み

### ⚠️ 残りのタスク（優先順）
1. **必須ページ作成**
   - [ ] プライバシーポリシー（AdSense・Analytics明記）
   - [ ] お問い合わせページ
   - [ ] 運営者情報充実化
   - [ ] フッターメニューに追加

2. **Google関連サービス設定**
   - [ ] Google Search Console登録
   - [ ] XMLサイトマップ送信
   - [ ] Google Analytics設定

3. **最終確認**
   - [ ] モバイル表示確認
   - [ ] ページ速度確認（PageSpeed Insights）
   - [ ] ナビゲーション確認
   - [ ] リンク切れ確認

---

## 今後の作業ロードマップ

### ✅ Phase 1-2.3: 既存記事改善（完了）
- [x] 21記事に整理（52記事を下書きに）
- [x] 全記事800文字以上
- [x] アイキャッチ画像・本文画像設定
- [x] メタディスクリプション・まとめセクション追加
- [x] カテゴリ・タグ整理

### Phase 2: 必須ページ作成 ✅ ほぼ完了（フッターメニューのみ残）
1. [x] **プライバシーポリシーページ**
   - Cookie使用、AdSense、Analytics利用を明記済み
2. [x] **お問い合わせページ**
   - Google Forms埋め込み完了（iFrame）
3. [x] **運営者情報充実化**
   - プロフィールページに運営者情報・経歴・専門性セクション追加
4. [ ] **フッターメニュー整備**
   - 手動設定が必要（[設定手順](#フッターメニュー設定手順)参照）

### Phase 3: 技術・SEO対策（優先度：高）
1. [ ] **Google Search Console登録**
2. [ ] **XMLサイトマップ送信**
3. [ ] **Google Analytics設定**
4. [ ] **モバイル表示確認**
5. [ ] **ページ速度確認**（PageSpeed Insights）

### Phase 4: AdSense申請（Phase 2-3完了後）
1. [ ] 全チェックリスト確認
2. [ ] AdSenseアカウント作成・サイト登録
3. [ ] 審査コード設置
4. [ ] 審査申請
5. [ ] 審査結果待ち（1-2週間）

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

# アイキャッチ画像の一括設定
python add_featured_images.py

# 記事構造分析レポート生成
python improve_post_structure.py --mode analyze

# 内部リンク提案生成
python improve_post_structure.py --mode suggest-links

# 記事改善の自動適用（DRY RUNモードで確認）
python apply_post_improvements.py --mode all --dry-run

# 記事改善の自動適用（実行）
python apply_post_improvements.py --mode all

# 固定ページ更新（お問い合わせ・プロフィール）
python update_pages.py --mode all --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8" --dry-run
python update_pages.py --mode all --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8"

# 依存パッケージのアップデート
pip install --upgrade -r requirements.txt

# 新しい依存パッケージを追加した場合
pip freeze > requirements.txt

# 仮想環境の無効化
deactivate
```

---

## フッターメニュー設定手順（手動作業 約15分）

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
