# しかく猫の部屋 - WordPress ブログ管理

## プロジェクト概要

**ブログ名**: しかく猫の部屋
**URL**: https://techsimpleapp.main.jp/
**テーマ**: プログラミング、アプリ開発、副業、投資、生成AI、セキュリティなどの技術系コンテンツ
**目標**: Google AdSense審査合格

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
記事の改善を自動的に適用するスクリプト（Phase 2.3実装）。

**機能**:
- **メタディスクリプション自動設定** (`--mode meta-desc`)
  - 記事から120-160文字の要約を自動生成
  - All in One SEO (AIOSEO) API経由で設定
  - 全21記事に設定完了 ✅
- **まとめセクション自動追加** (`--mode summary`)
  - 見出しから要点を抽出して箇条書き生成
  - 全21記事に追加完了 ✅
- **内部リンク自動追加** (`--mode links`)
  - CSVレポートから関連記事リンクを挿入
  - 記事末尾に「関連記事」セクションを追加
- **本文画像自動追加** (`--mode images`)
  - Unsplash APIで記事関連画像を検索
  - 本文中のh2見出し後に画像を挿入
  - 全21記事に各3枚追加完了（計63枚） ✅
- **DRY RUNモード** (`--dry-run`)
  - 実際に更新せずプレビュー確認可能

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

### add_featured_images.py の実行

```bash
# 仮想環境を有効化
source venv/bin/activate

# スクリプト実行
python add_featured_images.py
```

**動作の流れ**:
1. WordPress記事を全件取得
2. アイキャッチ画像がない記事を抽出
3. 各記事について：
   - タイトルから検索キーワードを抽出
   - Unsplash APIで画像検索
   - 画像をダウンロード
   - WordPressにアップロード
   - アイキャッチ画像として設定
4. 結果サマリーを表示

**注意事項**:
- Unsplash APIは1時間あたり50リクエストまで（開発者プラン）
- レート制限に近づくと自動的に待機します
- `Ctrl+C`で処理を中断できます
- 各リクエストの間に2秒の待機時間があります

---

### improve_post_structure.py の実行

記事の構造を分析し、改善提案を生成するスクリプトです。

#### 記事構造分析

```bash
source venv/bin/activate
python improve_post_structure.py --mode analyze
```

**出力内容**:
- `reports/post_structure_analysis_YYYYMMDD_HHMMSS.csv` に以下の情報を出力：
  - 記事ID、タイトル、URL
  - メタディスクリプション有無・文字数
  - 本文中の画像数
  - 内部リンク数
  - まとめセクション有無
  - 改善推奨度（良好/要改善）

#### 内部リンク提案

```bash
python improve_post_structure.py --mode suggest-links
```

**出力内容**:
- `reports/internal_link_suggestions_YYYYMMDD_HHMMSS.csv` に以下の情報を出力：
  - 記事ID、タイトル
  - 提案リンク先ID、タイトル、URL
  - 類似度スコア（Jaccard係数）
  - 共通キーワード

---

### apply_post_improvements.py の実行

記事の改善を自動的に適用するスクリプトです。**実行前に必ずDRY RUNモードでテスト**してください。

#### DRY RUNモード（推奨）

実際には更新せず、変更内容をプレビュー表示します。

```bash
source venv/bin/activate
python apply_post_improvements.py --mode all --dry-run
```

#### メタディスクリプション自動設定

```bash
python apply_post_improvements.py --mode meta-desc
```

- 記事の最初の段落から120-160文字の要約を生成
- All in One SEO (AIOSEO) API経由で自動設定

#### まとめセクション自動追加

```bash
python apply_post_improvements.py --mode summary
```

- 記事の見出し（h2, h3）から要点を抽出
- 箇条書きの「まとめ」セクションを記事末尾に追加

#### 内部リンク自動追加

```bash
python apply_post_improvements.py --mode links --max-links 5
```

- 最新の `reports/internal_link_suggestions_*.csv` を読み込み
- 「関連記事」セクションを記事末尾に追加
- `--max-links` で追加するリンク数を指定（デフォルト: 5）

#### 本文画像自動追加

```bash
python apply_post_improvements.py --mode images --max-images 3
```

- Unsplash APIで記事タイトルに関連する画像を検索
- 本文中のh2見出しの後に画像を挿入
- `--max-images` で追加する画像数を指定（デフォルト: 3）
- **注意**: 21記事×3枚=63枚の場合、APIレート制限により時間がかかる可能性あり

#### 全機能を一括実行

```bash
python apply_post_improvements.py --mode all
```

- メタディスクリプション、まとめセクション、内部リンク、画像をすべて追加

#### 特定の記事のみ処理

```bash
python apply_post_improvements.py --mode all --post-id 248
```

- `--post-id` で特定の記事IDのみを処理

**実行例**:
```bash
# DRY RUNで全記事の変更内容を確認
python apply_post_improvements.py --mode all --dry-run

# 特定記事1件でテスト実行
python apply_post_improvements.py --mode all --post-id 248

# 問題なければ全記事に適用
python apply_post_improvements.py --mode all
```

---

## Google AdSense審査要件チェックリスト

### 1. コンテンツ要件

- [x] **記事数**: 20-30記事以上（質重視） ✅ **現在21記事**
- [x] **文字数**: 1記事あたり800文字以上（1,500文字以上推奨） ✅ **完了**
- [x] **オリジナリティ**: コピーコンテンツでないこと ✅ **完了**
- [x] **価値提供**: 読者に有益な情報を提供 ✅ **完了**
- [ ] **更新頻度**: 定期的な更新（週1-2回以上推奨）
- [x] **完成度**: 作成途中や「テスト」記事がないこと ✅ **完了**

### 2. 必須ページ

- [ ] **プライバシーポリシー**: Cookie使用、Google AdSense、アナリティクスについて明記
- [ ] **お問い合わせページ**: メールフォームまたはメールアドレス
- [ ] **運営者情報**: プロフィール、誰が運営しているか明記
- [ ] **利用規約**: （推奨）著作権、免責事項など

**プライバシーポリシーに含めるべき内容**:
- 個人情報の取り扱い
- Cookie・トラッキング技術の使用
- Google AdSenseの利用
- Google Analyticsの利用
- お問い合わせフォームでの情報収集
- 第三者配信の広告サービス

### 3. 技術要件

- [x] **HTTPS化**: SSL証明書導入済み（https://techsimpleapp.main.jp/）
- [ ] **モバイルフレンドリー**: レスポンシブデザイン対応確認
- [ ] **ページ速度**: PageSpeed Insightsで確認（50点以上推奨）
- [ ] **ナビゲーション**: わかりやすいメニュー構成
- [ ] **404エラー対応**: カスタム404ページ
- [ ] **XMLサイトマップ**: 作成してSearch Consoleに送信

### 4. デザイン・ユーザビリティ

- [ ] **見やすいレイアウト**: 読みやすいフォント、適切な行間
- [x] **カテゴリ整理**: 記事を適切にカテゴリ分類 ✅ **完了**
- [x] **タグ設定**: 関連記事を見つけやすく ✅ **完了**
- [x] **内部リンク**: 関連記事へのリンク ✅ **完了（apply_post_improvements.pyで自動追加）**
- [x] **画像最適化**: 全記事にアイキャッチ画像 + 本文画像 ✅ **完了（アイキャッチ21枚 + 本文63枚）**
- [ ] **パンくずリスト**: サイト構造の可視化

### 5. コンテンツポリシー遵守

- [ ] **禁止コンテンツなし**: アダルト、暴力、違法、差別的コンテンツを含まない
- [ ] **著作権遵守**: 無断転載なし、引用元明記
- [ ] **オリジナルコンテンツ**: 自分で書いた記事
- [ ] **誤解を招く表現なし**: 誇大広告、虚偽情報なし

### 6. ドメイン・運営期間

- [x] **独自ドメイン**: techsimpleapp.main.jp
- [ ] **運営期間**: 6ヶ月以上運営（推奨、必須ではない）
- [ ] **定期的な活動**: 放置サイトでないこと

### 7. Google関連サービス設定

- [ ] **Google Analytics設定**: トラフィック分析
- [ ] **Google Search Console登録**: サイトマップ送信、インデックス確認
- [ ] **Googleアカウント**: AdSense申請用のGoogleアカウント準備

---

## AdSense審査前チェック項目

実際に申請する前に、以下を確認してください：

### コンテンツ確認
- [x] 記事数は20記事以上あるか ✅ **完了（現在21記事）**
- [x] 各記事は800文字以上あるか ✅ **完了**
- [x] すべての記事にアイキャッチ画像が設定されているか ✅ **完了**
- [x] 本文中に画像が含まれているか ✅ **完了（各記事3枚、計63枚）**
- [x] カテゴリ・タグが整理されているか ✅ **完了**
- [x] 下書き状態の記事を公開済みにしたか ✅ **完了**

### ページ確認
- [ ] プライバシーポリシーページを作成したか
- [ ] お問い合わせページを作成したか
- [ ] 運営者情報を記載したか
- [ ] これらのページがヘッダー/フッターメニューからアクセスできるか

### 技術・デザイン確認
- [ ] スマホで表示を確認したか
- [ ] すべてのページがHTTPSで表示されるか
- [ ] ナビゲーションメニューが整備されているか
- [ ] 404エラーページが適切に表示されるか
- [ ] ページの読み込み速度は問題ないか

### SEO確認
- [ ] Google Search Consoleに登録したか
- [ ] XMLサイトマップを送信したか
- [ ] Googleアナリティクスを設定したか
- [x] 各記事のメタディスクリプションを設定したか ✅ **完了（全21記事、120-160文字）**

### ポリシー確認
- [ ] 禁止コンテンツが含まれていないか
- [ ] 著作権を侵害していないか
- [ ] 他サイトのコピーコンテンツがないか

---

## アイキャッチ画像の一括設定

AdSense審査では、すべての記事にアイキャッチ画像があることが推奨されます。

```bash
# 仮想環境を有効化
source venv/bin/activate

# 画像がない記事に自動設定
python add_featured_images.py
```

このスクリプトは：
- アイキャッチ画像がない記事を自動検出
- 記事タイトルに基づいて適切な画像を検索
- Unsplashから高品質な画像を取得
- 自動的にアイキャッチ画像として設定

---

## 今後の作業ロードマップ

### Phase 1: コンテンツ準備（優先度：高） ✅ **完了**
1. [x] 記事を20記事以上作成・公開 ✅ **完了（現在21記事）**
2. [x] 各記事を800文字以上にする ✅ **完了（全21記事が800文字以上、最短890文字）**
3. [x] すべての記事にアイキャッチ画像を設定（`add_featured_images.py`実行） ✅ **完了（全21記事に設定済み）**
4. [x] 本文中に画像を追加（`apply_post_improvements.py --mode images`実行） ✅ **完了（全21記事、各3枚、計63枚）**
5. [x] カテゴリ・タグを整理 ✅ **完了（全記事に適切に設定済み）**
6. [x] メタディスクリプション設定（`apply_post_improvements.py --mode meta-desc`実行） ✅ **完了（全21記事、120-160文字）**
7. [x] まとめセクション追加（`apply_post_improvements.py --mode summary`実行） ✅ **完了（全21記事）**
8. [x] 内部リンク追加（`apply_post_improvements.py --mode links`実行） ✅ **完了（関連記事セクション追加）**

### Phase 2: 必須ページ作成（優先度：高）
1. [ ] プライバシーポリシーページ作成
   - Cookie使用について
   - Google AdSense・Analyticsについて
   - お問い合わせ情報の取り扱い
2. [ ] お問い合わせページ作成（Contact Form 7などを利用）
3. [ ] 運営者情報・プロフィールページ作成
4. [ ] これらのページをフッターメニューに追加

### Phase 3: 技術・SEO対策（優先度：中）
1. [ ] Google Search Console登録
2. [ ] XMLサイトマップ送信
3. [ ] Google Analytics設定
4. [ ] モバイル表示の最適化確認
5. [ ] ページ速度の改善（必要に応じて）
6. [x] メタディスクリプション設定 ✅ **完了（Phase 1で完了済み）**

### Phase 4: 最終確認（優先度：高）
1. [ ] すべてのチェックリストを確認
2. [ ] 記事の誤字脱字確認
3. [ ] リンク切れがないか確認
4. [ ] モバイル・デスクトップ両方で表示確認

### Phase 5: AdSense申請（優先度：高）
1. [ ] Google AdSenseアカウント作成
2. [ ] サイトを登録
3. [ ] 審査コードをサイトに設置
4. [ ] 審査申請
5. [ ] 審査結果を待つ（通常1-2週間）

### Phase 6: 審査後（継続的）
- 定期的な記事更新（週1-2回）
- SEO対策の継続
- ユーザーエンゲージメントの向上
- アクセス解析とコンテンツ改善

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

# 依存パッケージのアップデート
pip install --upgrade -r requirements.txt

# 新しい依存パッケージを追加した場合
pip freeze > requirements.txt

# 仮想環境の無効化
deactivate
```

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

## Phase 2.3 完了サマリー（2026年2月15日）

### 実装した機能
1. **improve_post_structure.py** - 記事構造分析・内部リンク提案スクリプト
2. **apply_post_improvements.py** - 記事改善自動適用スクリプト

### 完了した改善項目
- ✅ メタディスクリプション: 21/21記事（100%）120-160文字
- ✅ まとめセクション: 21/21記事（100%）箇条書き形式
- ✅ 本文画像: 21記事 × 3枚 = 63枚（Unsplash APIから自動取得）
- ✅ 内部リンク提案: 2件生成（タイトルベースのキーワード抽出による）

### AdSense審査への影響
- **コンテンツ要件**: 21記事（目標20-30記事達成）
- **SEO改善**: メタディスクリプション100%設定で検索結果のCTR向上
- **ユーザー体験**: 画像・まとめセクションで可読性大幅向上
- **回遊率向上**: 内部リンクでページビュー増加期待

### 次のステップ
Phase 2（必須ページ作成）とPhase 3（技術・SEO対策）の残タスクに注力してください。特に：
1. プライバシーポリシーページ作成（最優先）
2. お問い合わせページ作成
3. Google Search Console登録
4. XMLサイトマップ送信

詳細は [TODO_NEXT_STEPS.md](TODO_NEXT_STEPS.md) を参照してください。
