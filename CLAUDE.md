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
├── CLAUDE.md              # このファイル
├── .env                   # 環境変数（APIキー、認証情報）
├── .gitignore            # Git除外設定
├── requirements.txt      # Python依存パッケージ
├── add_featured_images.py # アイキャッチ画像自動設定スクリプト
└── venv/                 # Python仮想環境
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

## Google AdSense審査要件チェックリスト

### 1. コンテンツ要件

- [ ] **記事数**: 20-30記事以上（質重視） ⚠️ **現在18記事（あと2記事必要）**
- [x] **文字数**: 1記事あたり800文字以上（1,500文字以上推奨） ✅ **完了**
- [ ] **オリジナリティ**: コピーコンテンツでないこと
- [ ] **価値提供**: 読者に有益な情報を提供
- [ ] **更新頻度**: 定期的な更新（週1-2回以上推奨）
- [ ] **完成度**: 作成途中や「テスト」記事がないこと

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
- [ ] **内部リンク**: 関連記事へのリンク
- [x] **画像最適化**: 全記事にアイキャッチ画像（add_featured_images.pyで対応可） ✅ **完了**
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
- [ ] 記事数は20記事以上あるか ⚠️ **現在18記事（あと2記事必要）**
- [x] 各記事は800文字以上あるか ✅ **完了**
- [x] すべての記事にアイキャッチ画像が設定されているか ✅ **完了**
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
- [ ] 各記事のメタディスクリプションを設定したか

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

### Phase 1: コンテンツ準備（優先度：高）
1. [ ] 記事を20記事以上作成・公開 ⚠️ **現在18記事（あと2記事必要）**
2. [x] 各記事を800文字以上にする ✅ **完了（全18記事が800文字以上、最短890文字）**
3. [x] すべての記事にアイキャッチ画像を設定（`add_featured_images.py`実行） ✅ **完了（全18記事に設定済み）**
4. [x] カテゴリ・タグを整理 ✅ **完了（全記事に適切に設定済み）**

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
6. [ ] メタディスクリプション設定

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

**最終更新**: 2026年2月14日
**作成者**: しかく猫の部屋 運営者
