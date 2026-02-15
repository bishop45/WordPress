# Claude Code 拡張機能

このディレクトリには、Claude Code を拡張する Skills と Commands が含まれています。

## 📁 ディレクトリ構造

```
.claude/
├── README.md                  # このファイル
├── settings.local.json        # ローカル設定
├── skills/                    # Skills（複雑なタスク）
│   └── write-post/
│       └── SKILL.md          # 記事生成スキル
└── commands/                  # Commands（シンプルなタスク）
    ├── check-adsense.md      # AdSense要件チェック
    ├── analyze-post.md       # 記事分析
    └── quick-fix.md          # クイックフィックス
```

## 🎯 Skills vs Commands

### Skills（推奨）

**特徴**:
- 複雑なタスクに適している
- ディレクトリ構造でサポートファイルを含められる
- Claude が自動的に呼び出すことができる（`disable-model-invocation: false` の場合）
- `/skill-name` で手動呼び出しも可能

**使用例**:
```bash
# テーマを指定して記事を生成（自動実行される場合もある）
/write-post Python環境構築 --target 初心者 --category プログラミング

# オプション付き
/write-post 副業の始め方 --target 中級者 --words 1500
```

### Commands（シンプルなタスク向け）

**特徴**:
- シンプルなタスクに適している
- 単一ファイル（フラットファイル）
- 主に手動呼び出し（`disable-model-invocation: true` が一般的）
- `/command-name` で呼び出し

**使用例**:
```bash
# AdSense要件をチェック
/check-adsense https://techsimpleapp.main.jp/post-url

# 記事を分析
/analyze-post 123

# クイックフィックスを実行
/quick-fix 123
```

## 📚 利用可能な Skills

### `/write-post` - AdSense対応記事生成

**説明**: AdSense審査に合格する記事を自動生成します。

**使い方**:
```bash
/write-post <テーマ> [--target 初心者/中級者/上級者] [--words 文字数] [--category カテゴリ]
```

**例**:
```bash
/write-post Python環境構築 --target 初心者 --category プログラミング
/write-post 副業の始め方 --target 中級者 --words 1500
/write-post セキュリティ対策 --category セキュリティ
```

**生成内容**:
1. タイトル案（3つ）
2. メタディスクリプション案
3. カテゴリ・タグ案
4. 記事構成（h2見出し4-5個）
5. 記事本文（800文字以上）
6. まとめセクション
7. AdSense要件チェックリスト

**次のステップ**:
生成された記事をWordPressに投稿後、自動化スクリプトで最適化：
```bash
python scripts/active/add_featured_images.py
python scripts/active/apply_post_improvements.py --mode all
```

## 📋 利用可能な Commands

### `/check-adsense` - AdSense要件チェック

**説明**: 記事がGoogle AdSense審査要件を満たしているか確認します。

**使い方**:
```bash
/check-adsense <記事URL または 記事ID>
```

**例**:
```bash
/check-adsense https://techsimpleapp.main.jp/python-setup/
/check-adsense 123
```

**チェック項目**:
- コンテンツ要件（文字数、オリジナリティ、読者価値）
- 構成要件（タイトル、メタディスクリプション、見出し、まとめ）
- 画像要件（アイキャッチ、本文画像、altテキスト）
- SEO要件（カテゴリ、タグ、内部リンク）
- 禁止コンテンツチェック

**出力**: 合格/要改善/不合格の判定と具体的な改善提案

---

### `/analyze-post` - 記事分析

**説明**: WordPress記事を詳細に分析し、SEO・可読性・構造の改善提案を行います。

**使い方**:
```bash
/analyze-post <記事URL または 記事ID>
```

**例**:
```bash
/analyze-post https://techsimpleapp.main.jp/python-setup/
/analyze-post 123
```

**分析項目**:
1. **SEO分析**: タイトル、メタディスクリプション、見出し構造、内部リンク
2. **可読性分析**: 段落構成、文章の読みやすさ、視覚的要素
3. **コンテンツ品質分析**: 文字数、オリジナリティ、E-E-A-T
4. **AdSense要件チェック**: 全項目の適合状況

**出力**: 優先度別の改善提案と総合評価（スコア）

---

### `/quick-fix` - クイックフィックス

**説明**: 記事の一般的な問題を素早く自動修正します。

**使い方**:
```bash
/quick-fix <記事URL または 記事ID>
```

**例**:
```bash
/quick-fix 123
```

**自動修正内容**:
1. メタディスクリプション未設定 → 自動生成
2. アイキャッチ画像未設定 → Unsplashから取得・設定
3. 本文画像不足（3枚未満） → h2見出し後に自動挿入
4. まとめセクション未設定 → 見出しから要点抽出・生成
5. 内部リンク不足（2個未満） → 関連記事セクション追加

**実行方法**:
```bash
# DRY RUNで確認（推奨）
python scripts/active/apply_post_improvements.py --mode all --post-id <ID> --dry-run

# 実際に修正
python scripts/active/apply_post_improvements.py --mode all --post-id <ID>
```

## 🚀 ワークフロー例

### 新規記事作成のワークフロー

1. **記事生成**:
   ```bash
   /write-post Python環境構築 --target 初心者 --category プログラミング
   ```

2. **WordPress投稿**:
   - 生成された記事をWordPress管理画面にコピー
   - カテゴリ・タグを設定
   - 公開

3. **自動最適化**:
   ```bash
   python scripts/active/add_featured_images.py
   python scripts/active/apply_post_improvements.py --mode all
   ```

4. **確認**:
   ```bash
   /check-adsense 123
   ```

### 既存記事改善のワークフロー

1. **記事分析**:
   ```bash
   /analyze-post 123
   ```

2. **問題箇所を確認**:
   - 分析レポートで改善提案を確認

3. **クイックフィックス**:
   ```bash
   /quick-fix 123
   ```

4. **再確認**:
   ```bash
   /check-adsense 123
   ```

## 📖 参考リソース

- **公式ドキュメント**: https://code.claude.com/docs/ja/skills
- **プロジェクトドキュメント**: [../CLAUDE.md](../CLAUDE.md)
- **記事テンプレート**: [../templates/post_template.md](../templates/post_template.md)
- **記事作成ガイドライン**: [../templates/post_guidelines.md](../templates/post_guidelines.md)

## 🔧 カスタマイズ

### 新しいSkillを追加する

1. `.claude/skills/` 内に新しいディレクトリを作成
2. `SKILL.md` ファイルを作成（YAMLフロントマター + マークダウンコンテンツ）
3. 必要に応じてサポートファイルを追加（`examples.md`、`scripts/` など）

**例**:
```
.claude/skills/my-skill/
├── SKILL.md          # メイン定義
├── examples.md       # 使用例
└── scripts/
    └── helper.py     # ヘルパースクリプト
```

### 新しいCommandを追加する

1. `.claude/commands/` 内に新しいMarkdownファイルを作成
2. YAMLフロントマター + マークダウンコンテンツを記述

**例**:
```markdown
---
name: my-command
description: My command description
disable-model-invocation: true
---

# My Command

[コマンドの指示内容]
```

## ⚠️ 注意事項

- **Skills は自動実行される場合がある**: `disable-model-invocation: false` の場合、Claude が自動的に呼び出すことがあります
- **Commands は手動実行が基本**: 通常は `/command-name` で手動呼び出しします
- **DRY RUN推奨**: 自動修正系のコマンドは必ず `--dry-run` で確認してから実行してください
- **人間の確認が必要**: 自動生成・自動修正は完璧ではありません。必ず内容を確認してください

## 📝 更新履歴

- **2026-02-15**: 初版作成
  - write-post Skill 追加
  - check-adsense、analyze-post、quick-fix Commands 追加
