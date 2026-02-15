# しかく猫の部屋 - WordPress ブログ管理ツール

**ブログURL**: https://techsimpleapp.main.jp/
**ステータス**: ✅ Phase 1-4 完了（AdSense申請準備完了）

## クイックスタート

### 環境セットアップ

```bash
# Python仮想環境の有効化
source venv/bin/activate

# 依存パッケージのインストール（初回のみ）
pip install -r requirements.txt
```

### 新規記事作成フロー（AdSense対応）

#### 🚀 Claude Code Skillを使用（推奨）

```bash
# write-post Skillで記事を自動生成
/write-post [テーマ] --target [初心者/中級者/上級者] --category [カテゴリ]

# 例
/write-post Python環境構築 --target 初心者 --category プログラミング
/write-post 副業の始め方 --target 中級者 --words 1500
```

生成された記事をWordPressに投稿後、自動最適化：

```bash
python scripts/active/add_featured_images.py
python scripts/active/apply_post_improvements.py --mode all
```

#### 📝 手動作成の場合

```bash
# 1. テンプレートを確認
cat templates/post_template.md
cat templates/post_guidelines.md

# 2. WordPress管理画面で記事を作成・公開

# 3. 自動最適化
python scripts/active/add_featured_images.py
python scripts/active/apply_post_improvements.py --mode all --dry-run
python scripts/active/apply_post_improvements.py --mode all
```

### サイト検証・チェック

```bash
# サイトの技術・SEO要件を確認
python scripts/active/verify_site.py

# AdSense申請前の最終チェック
python scripts/active/final_check.py

# 記事構造の分析
python scripts/active/improve_post_structure.py --mode analyze
```

## ファイル構成

```
WordPress/
├── README.md                     # このファイル（クイックスタート）
├── CLAUDE.md                     # 詳細ガイド
├── docs/                         # ドキュメント
│   ├── TODO_NEXT_STEPS.md       # 作業計画
│   ├── PHASE3_GUIDE.md          # Phase 3ガイド
│   └── PHASE4_GUIDE.md          # Phase 4ガイド
├── scripts/active/               # アクティブなスクリプト
│   ├── add_featured_images.py
│   ├── improve_post_structure.py
│   ├── apply_post_improvements.py
│   ├── update_pages.py
│   ├── verify_site.py
│   └── final_check.py
├── templates/                    # 記事作成テンプレート
└── reports/                      # 分析レポート
```

## AdSense審査要件（✅ 全達成）

### コンテンツ
- ✅ 記事数: 21記事
- ✅ 文字数: 全記事800文字以上
- ✅ 画像: アイキャッチ21枚 + 本文63枚
- ✅ メタディスクリプション: 全記事設定済み

### 必須ページ
- ✅ プライバシーポリシー
- ✅ お問い合わせページ
- ✅ 運営者情報（プロフィール）
- ✅ フッターメニュー

### 技術・SEO
- ✅ HTTPS対応
- ✅ Google Analytics
- ✅ Google Search Console
- ✅ XMLサイトマップ
- ✅ モバイルフレンドリー
- ✅ ページ速度最適化

## 主要スクリプト

### add_featured_images.py
- Unsplash APIから画像を取得してアイキャッチ画像を自動設定

### apply_post_improvements.py
- メタディスクリプション自動設定
- まとめセクション追加
- 内部リンク追加
- 本文画像追加（h2見出し後）

### improve_post_structure.py
- 記事構造の分析とCSVレポート出力
- 内部リンク提案生成

### verify_site.py
- XMLサイトマップ・robots.txt確認
- 必須ページの存在確認
- HTTPS対応確認

### final_check.py
- AdSense申請前の最終チェック
- Phase 1-4の全項目を自動検証

## 環境変数（.env）

```bash
# WordPress設定
WORDPRESS_URL=https://techsimpleapp.main.jp
WORDPRESS_USERNAME=ユーザー名
WORDPRESS_APPLICATION_PASSWORD=アプリケーションパスワード

# Unsplash API設定
UNSPLASH_APPLICATION_ID=アプリケーションID
UNSPLASH_ACCESS_KEY=アクセスキー
UNSPLASH_SECRET_KEY=シークレットキー
```

## 詳細ドキュメント

- **プロジェクト詳細**: [CLAUDE.md](CLAUDE.md)
- **Phase 3ガイド**: [docs/PHASE3_GUIDE.md](docs/PHASE3_GUIDE.md)
- **Phase 4ガイド**: [docs/PHASE4_GUIDE.md](docs/PHASE4_GUIDE.md)
- **作業履歴**: [docs/TODO_NEXT_STEPS.md](docs/TODO_NEXT_STEPS.md)

## 次のステップ

Phase 4（AdSense申請）の準備が完了しています。詳細は [docs/PHASE4_GUIDE.md](docs/PHASE4_GUIDE.md) を参照してください。

---

**最終更新**: 2026年2月15日
**作成者**: しかく猫の部屋 運営者
