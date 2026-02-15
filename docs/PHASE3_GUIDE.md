# Phase 3: 技術・SEO対策 実施ガイド

**目的**: Google AdSense審査合格に向けた技術・SEO設定の完了
**対象サイト**: https://techsimpleapp.main.jp/
**作成日**: 2026年2月15日

---

## 📋 Phase 3 タスク一覧

### ✅ 完了済み
- [x] Google Analytics設定

### ⚠️ 未完了（これから実施）
- [ ] Google Search Console登録
- [ ] XMLサイトマップ送信
- [ ] モバイル表示確認
- [ ] ページ速度確認（PageSpeed Insights）
- [ ] リンク切れ確認

---

## 1. Google Search Console登録

### 目的
- Googleにサイトを認識させる
- 検索パフォーマンスを監視
- XMLサイトマップを送信
- インデックス状況を確認

### 手順

#### ステップ1: Google Search Consoleにアクセス
1. https://search.google.com/search-console にアクセス
2. Googleアカウントでログイン（Google Analyticsと同じアカウント推奨）

#### ステップ2: プロパティを追加
1. 左上の「プロパティを検索」→「プロパティを追加」をクリック
2. プロパティタイプを選択：
   - **URLプレフィックス**を選択（推奨）
   - URL: `https://techsimpleapp.main.jp` を入力
3. 「続行」をクリック

#### ステップ3: 所有権の確認
複数の確認方法がありますが、**HTMLタグ方式**が最も簡単です。

**方法1: HTMLタグ（推奨）**
1. Google Search Consoleで「HTMLタグ」を選択
2. メタタグをコピー（例: `<meta name="google-site-verification" content="......">`）
3. WordPressダッシュボード → **外観 → テーマエディター** → **header.php**
4. `</head>` の直前にメタタグを貼り付け
5. 「ファイルを更新」をクリック
6. Google Search Consoleに戻り「確認」をクリック

**方法2: Google Analytics（GAが設定済みの場合）**
1. Google Search Consoleで「Google Analytics」を選択
2. 「確認」をクリック（既にGAが設定されていれば自動認証）

**方法3: HTMLファイル（サーバーアクセスが必要）**
1. 指定されたHTMLファイルをダウンロード
2. WordPressの公開ディレクトリ（ルート）にアップロード
3. ブラウザで `https://techsimpleapp.main.jp/google[ID].html` にアクセスして確認
4. Google Search Consoleに戻り「確認」をクリック

#### ステップ4: 確認完了
「所有権を確認しました」と表示されれば成功です。

---

## 2. XMLサイトマップ作成・送信

### 目的
- Googleにサイト構造を伝える
- 新しいページを早くインデックスさせる
- SEO効果を高める

### 2-1. XMLサイトマップの存在確認

WordPressでは多くのSEOプラグイン（Yoast SEO、All in One SEOなど）が自動的にサイトマップを生成します。

#### 確認方法
以下のURLをブラウザで開いて、XMLサイトマップが存在するか確認してください：

1. **標準のWordPressサイトマップ**（WordPress 5.5以降はデフォルトで生成）
   ```
   https://techsimpleapp.main.jp/wp-sitemap.xml
   ```

2. **Yoast SEOを使用している場合**
   ```
   https://techsimpleapp.main.jp/sitemap_index.xml
   ```

3. **All in One SEO (AIOSEO)を使用している場合**
   ```
   https://techsimpleapp.main.jp/sitemap.xml
   ```

4. **Rank Mathを使用している場合**
   ```
   https://techsimpleapp.main.jp/sitemap_index.xml
   ```

#### XMLサイトマップの例
正常なサイトマップは以下のようなXML形式で表示されます：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://techsimpleapp.main.jp/</loc>
    <lastmod>2026-02-15</lastmod>
    <priority>1.0</priority>
  </url>
  ...
</urlset>
```

### 2-2. サイトマップが見つからない場合

#### WordPressデフォルトのサイトマップを有効化
1. WordPressダッシュボード → **設定 → 表示設定**
2. 「検索エンジンがサイトをインデックスしないようにする」のチェックが**外れている**ことを確認
3. `https://techsimpleapp.main.jp/wp-sitemap.xml` にアクセスして確認

#### SEOプラグインでサイトマップを生成
**Yoast SEO（推奨）**を使用する場合：
1. WordPressダッシュボード → **プラグイン → 新規追加**
2. 「Yoast SEO」を検索してインストール・有効化
3. **SEO → 一般 → 機能** → 「XMLサイトマップ」を有効化
4. `https://techsimpleapp.main.jp/sitemap_index.xml` にアクセスして確認

### 2-3. Google Search ConsoleにサイトマップURLを送信

1. Google Search Console → **サイトマップ**（左メニュー）
2. 「新しいサイトマップの追加」に以下のいずれかを入力：
   - `wp-sitemap.xml`（WordPress標準）
   - `sitemap_index.xml`（Yoast SEO、Rank Math）
   - `sitemap.xml`（AIOSEO）
3. 「送信」をクリック
4. ステータスが「成功しました」になることを確認

---

## 3. モバイル表示確認

### 目的
- スマートフォンで正しく表示されるか確認
- レスポンシブデザインの動作確認
- AdSense審査の必須要件（モバイルフレンドリー）

### 3-1. Googleモバイルフレンドリーテスト

1. https://search.google.com/test/mobile-friendly にアクセス
2. URL欄に `https://techsimpleapp.main.jp` を入力
3. 「URLをテスト」をクリック
4. 結果を確認：
   - ✅ **「ページはモバイルフレンドリーです」** → 合格
   - ❌ **問題が検出される** → 改善が必要

#### よくある問題と対処法
- **テキストが小さすぎる**: テーマのフォントサイズを調整
- **タップ要素同士が近すぎる**: ボタン・リンクの間隔を広げる
- **ビューポートが設定されていない**: テーマのheader.phpに以下を追加
  ```html
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  ```

### 3-2. 実機・ブラウザでの確認

#### Chromeデベロッパーツール（PC）
1. Chromeでサイトを開く: https://techsimpleapp.main.jp
2. `F12`（または右クリック → 検証）でデベロッパーツールを開く
3. ツールバーの「デバイスツールバー」アイコン（📱）をクリック
4. 以下のデバイスで表示を確認：
   - iPhone 12 Pro（390x844）
   - iPhone SE（375x667）
   - iPad（768x1024）
   - Galaxy S20（412x915）

#### 確認ポイント
- [ ] ヘッダーメニューが正しく表示される
- [ ] 画像が画面からはみ出ない
- [ ] テキストが読みやすいサイズ
- [ ] ボタン・リンクがタップしやすい
- [ ] フッターメニューが表示される
- [ ] お問い合わせフォームが動作する

---

## 4. ページ速度確認（PageSpeed Insights）

### 目的
- ページ読み込み速度を測定
- ユーザー体験（UX）の向上
- SEOランキング向上
- AdSense審査の評価要素

### 手順

#### ステップ1: PageSpeed Insightsで測定
1. https://pagespeed.web.dev/ にアクセス
2. URL欄に以下を入力して測定（複数ページ推奨）：
   - トップページ: `https://techsimpleapp.main.jp`
   - 記事ページ: 主要な記事のURL
   - 固定ページ: プロフィール、お問い合わせ
3. 「Analyze」をクリック

#### ステップ2: スコアを確認
PageSpeed Insightsは0〜100点でスコアを表示します：
- **90-100点**: 優秀（緑）
- **50-89点**: 改善が必要（オレンジ）
- **0-49点**: 不良（赤）

**目標**: モバイル・デスクトップともに **50点以上**（できれば70点以上）

#### ステップ3: 主要指標を確認
- **FCP (First Contentful Paint)**: 最初のコンテンツ表示時間 → 1.8秒以下
- **LCP (Largest Contentful Paint)**: 最大コンテンツ表示時間 → 2.5秒以下
- **CLS (Cumulative Layout Shift)**: レイアウトのずれ → 0.1以下

### よくある改善方法

#### 1. 画像の最適化
- 画像を圧縮（JPEG: 80-85%品質、WebP形式推奨）
- プラグイン「EWWW Image Optimizer」または「Smush」を使用
- アイキャッチ画像のサイズを適切に設定（推奨: 1200x630px）

#### 2. キャッシュプラグインの導入
- **WP Rocket**（有料、高性能）
- **W3 Total Cache**（無料）
- **WP Super Cache**（無料、シンプル）

#### 3. 不要なプラグインを無効化
- 使っていないプラグインを削除
- 軽量なプラグインに置き換え

#### 4. CDN（コンテンツ配信ネットワーク）の利用
- **Cloudflare**（無料プラン利用可能）
- 静的ファイル（画像、CSS、JS）を高速配信

---

## 5. リンク切れ確認

### 目的
- 404エラーページの削減
- ユーザー体験の向上
- SEO評価の向上

### 5-1. プラグインで確認（推奨）

#### Broken Link Checkerプラグイン
1. WordPressダッシュボード → **プラグイン → 新規追加**
2. 「Broken Link Checker」を検索してインストール・有効化
3. **ツール → リンクエラー** でリンク切れを確認
4. 検出されたリンク切れを修正または削除

### 5-2. オンラインツールで確認

#### Online Broken Link Checker
1. https://www.brokenlinkcheck.com/ にアクセス
2. URL: `https://techsimpleapp.main.jp` を入力
3. 「Find broken links」をクリック
4. 結果を確認して、リンク切れを修正

---

## 📊 Phase 3 完了チェックリスト

### Google関連サービス
- [ ] Google Search Console登録完了
- [ ] XMLサイトマップ送信完了
- [x] Google Analytics設定完了 ✅

### サイト最適化
- [ ] モバイルフレンドリーテスト合格
- [ ] PageSpeed Insights: モバイル50点以上
- [ ] PageSpeed Insights: デスクトップ50点以上
- [ ] リンク切れ0件

---

## 🎯 Phase 3 完了後の次のステップ

Phase 3の全タスクが完了したら、**Phase 4: AdSense申請**に進みます。

### Phase 4の準備
1. すべてのチェックリスト項目を確認
2. サイトを最終チェック（誤字脱字、画像の表示、リンクの動作）
3. Google AdSenseアカウントを作成
4. サイトを登録・審査申請

詳細は `TODO_NEXT_STEPS.md` の Phase 4セクションを参照してください。

---

## 🔧 トラブルシューティング

### Q: Google Search Consoleで所有権確認ができない
A:
- HTMLタグが正しく貼り付けられているか確認
- キャッシュをクリア（ブラウザ＋WordPressプラグイン）
- Google Analytics方式を試す

### Q: XMLサイトマップが見つからない
A:
- WordPressバージョンを確認（5.5以降は `/wp-sitemap.xml` が標準）
- SEOプラグインをインストール（Yoast SEO推奨）
- プラグインの設定でサイトマップが有効になっているか確認

### Q: PageSpeed Insightsのスコアが低い
A:
- 画像圧縮プラグインを導入（EWWW Image Optimizer）
- キャッシュプラグインを導入（W3 Total Cache）
- 不要なプラグインを削除
- テーマを軽量なものに変更（検討）

### Q: モバイルフレンドリーテストで問題が出る
A:
- テーマがレスポンシブ対応か確認
- `<meta name="viewport">` タグがheader.phpにあるか確認
- CSSで `max-width: 100%` を画像に適用

---

## 📚 参考リンク

### Google公式ツール
- [Google Search Console](https://search.google.com/search-console)
- [モバイルフレンドリーテスト](https://search.google.com/test/mobile-friendly)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Google Analytics](https://analytics.google.com/)

### WordPress公式
- [WordPress サイトマップ](https://ja.wordpress.org/support/article/wordpress-sitemap/)
- [Yoast SEO](https://ja.wordpress.org/plugins/wordpress-seo/)
- [EWWW Image Optimizer](https://ja.wordpress.org/plugins/ewww-image-optimizer/)

### その他
- [Broken Link Check](https://www.brokenlinkcheck.com/)
- [Cloudflare](https://www.cloudflare.com/ja-jp/)

---

**最終更新**: 2026年2月15日
**作成者**: しかく猫の部屋 運営者

Phase 3の各タスクを順番に進めて、AdSense審査に備えましょう！
