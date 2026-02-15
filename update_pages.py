#!/usr/bin/env python3
"""
WordPress固定ページ更新スクリプト
AdSense審査対策: お問い合わせページ・プロフィールページの改善

使用方法:
  python update_pages.py --mode all --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8" --dry-run
  python update_pages.py --mode contact --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8"
  python update_pages.py --mode profile
"""

import os
import sys
import argparse
import requests
import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# =============================================================================
# 設定読み込み
# =============================================================================

def load_config():
    """環境変数から設定を読み込む"""
    load_dotenv()

    required_vars = [
        "WORDPRESS_URL",
        "WORDPRESS_USERNAME",
        "WORDPRESS_APPLICATION_PASSWORD",
    ]
    config = {}
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            print(f"エラー: 環境変数 {var} が設定されていません。")
            print("  .envファイルを確認してください。")
            sys.exit(1)
        config[var] = value

    return config


# =============================================================================
# WordPress REST API関数
# =============================================================================

def get_page_by_id(page_id, config):
    """固定ページをIDで取得"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/pages/{page_id}"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    response = requests.get(url, params={'context': 'edit'}, auth=auth)

    if response.status_code != 200:
        print(f"エラー: ページID {page_id} の取得に失敗しました (HTTP {response.status_code})")
        print(f"レスポンス: {response.text[:200]}")
        sys.exit(1)

    return response.json()


def update_page_content(page_id, new_content, config):
    """固定ページのコンテンツを更新"""
    url = f"{config['WORDPRESS_URL']}/wp-json/wp/v2/pages/{page_id}"
    auth = (config["WORDPRESS_USERNAME"], config["WORDPRESS_APPLICATION_PASSWORD"])

    payload = {
        "content": new_content
    }

    response = requests.post(url, json=payload, auth=auth)

    if response.status_code != 200:
        raise Exception(f"ページ更新失敗 (HTTP {response.status_code}): {response.text[:200]}")

    return response.json()


# =============================================================================
# Google Forms iFrame変換
# =============================================================================

def convert_google_form_url_to_iframe(form_url):
    """Google FormsのURLをiFrame埋め込みコードに変換

    Args:
        form_url: Google FormsのURL
            - https://forms.gle/xxxxx
            - https://docs.google.com/forms/d/e/xxxxx/viewform

    Returns:
        iFrameの埋め込みコード（HTML）
    """
    # forms.gle の短縮URLを展開
    if "forms.gle" in form_url:
        try:
            response = requests.head(form_url, allow_redirects=True, timeout=10)
            form_url = response.url
        except Exception as e:
            print(f"警告: Google Forms URLの展開に失敗しました: {e}")
            print(f"  元のURLを使用します: {form_url}")

    # /viewform を /viewform?embedded=true に変換
    if "viewform" in form_url:
        if "embedded=true" not in form_url:
            if "?" in form_url:
                form_url += "&embedded=true"
            else:
                form_url += "?embedded=true"
    else:
        # /viewform がない場合は追加
        if "?" in form_url:
            form_url += "&viewform&embedded=true"
        else:
            form_url += "/viewform?embedded=true"

    # iFrame生成
    iframe_html = f'''<iframe src="{form_url}"
        width="640"
        height="800"
        frameborder="0"
        marginheight="0"
        marginwidth="0">
  読み込んでいます…
</iframe>'''

    return iframe_html


# =============================================================================
# お問い合わせページ更新
# =============================================================================

def update_contact_page(google_form_url, config, dry_run=False):
    """お問い合わせページを更新

    Args:
        google_form_url: Google FormsのURL
        config: 設定情報
        dry_run: True の場合、実際には更新しない

    Returns:
        (success: bool, message: str)
    """
    page_id = 199

    print(f"📄 お問い合わせページ（ID: {page_id}）を更新します...")

    # 既存ページ取得
    page = get_page_by_id(page_id, config)
    print(f"  現在のタイトル: {page['title']['rendered']}")

    # Google Forms iFrame生成
    iframe_html = convert_google_form_url_to_iframe(google_form_url)

    # 新しいコンテンツ作成
    new_content = f'''<!-- wp:heading -->
<h2 class="wp-block-heading">お問い合わせ</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>「しかく猫の部屋」へのお問い合わせは、以下のフォームからお願いいたします。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{iframe_html}
<!-- /wp:html -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">【営業・勧誘目的のお問い合わせについて】</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>当サイトでは、商品・サービスの営業、広告掲載の売り込み、SEO対策・システム開発等の勧誘を目的としたお問い合わせはお受けしておりません。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>これらの内容につきましては、送信いただいてもご返信いたしかねますので、あらかじめご了承ください。</p>
<!-- /wp:paragraph -->
'''

    if dry_run:
        print("\n" + "=" * 80)
        print("【DRY RUN】お問い合わせページプレビュー")
        print("=" * 80)
        print(new_content)
        print("=" * 80)
        return True, "DRY RUN完了"

    # 実際に更新
    try:
        update_page_content(page_id, new_content, config)
        return True, "✅ お問い合わせページ更新完了"
    except Exception as e:
        return False, f"❌ お問い合わせページ更新失敗: {e}"


# =============================================================================
# プロフィールページ更新
# =============================================================================

def update_profile_page(config, dry_run=False):
    """プロフィールページを更新（運営者情報・経歴セクション追加）

    Args:
        config: 設定情報
        dry_run: True の場合、実際には更新しない

    Returns:
        (success: bool, message: str)
    """
    page_id = 2

    print(f"📄 プロフィールページ（ID: {page_id}）を更新します...")

    # 既存ページ取得
    page = get_page_by_id(page_id, config)
    print(f"  現在のタイトル: {page['title']['rendered']}")

    # 既存のHTMLを取得
    current_content = page['content']['raw']

    # BeautifulSoupで解析
    soup = BeautifulSoup(current_content, 'html.parser')

    # 既に運営者情報セクションが存在するかチェック
    existing_operator_section = soup.find('h2', string=lambda t: t and '運営者情報' in t)
    if existing_operator_section:
        print("  ⚠️ 運営者情報セクションは既に存在します。スキップします。")
        return True, "⚠️ プロフィールページは既に更新済み"

    # 運営者情報セクションのHTML
    operator_section_html = '''
<!-- 運営者情報セクション -->
<section class="section">
<h2 class="section-title">運営者情報</h2>
<div class="info-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
  <div class="info-item" style="padding: 1rem; background: #f5f5f5; border-radius: 8px;">
    <strong>運営者:</strong> しかく猫（ペンネーム）
  </div>
  <div class="info-item" style="padding: 1rem; background: #f5f5f5; border-radius: 8px;">
    <strong>運営形態:</strong> 個人運営
  </div>
  <div class="info-item" style="padding: 1rem; background: #f5f5f5; border-radius: 8px;">
    <strong>運営開始:</strong> 2024年
  </div>
  <div class="info-item" style="padding: 1rem; background: #f5f5f5; border-radius: 8px;">
    <strong>お問い合わせ:</strong> <a href="https://techsimpleapp.main.jp/お問い合わせ/">お問い合わせフォーム</a>
  </div>
</div>
</section>
'''

    # 経歴・専門性セクションのHTML
    career_section_html = '''
<!-- 経歴・専門性セクション -->
<section class="section">
<h2 class="section-title">経歴・専門性</h2>
<div class="bio-text" style="line-height: 1.8;">
  <p><strong>IT業界での経験:</strong> 15年以上のIT業界経験を持ち、プロジェクトマネージャー、システムアーキテクトとして大規模システム開発プロジェクトに従事してきました。</p>

  <p><strong>専門分野:</strong></p>
  <ul style="margin-left: 1.5rem; line-height: 1.8;">
    <li>プロジェクトマネジメント（PMP、情報処理技術者試験 プロジェクトマネージャ）</li>
    <li>システムアーキテクチャ設計（システムアーキテクト、ネットワークスペシャリスト、データベーススペシャリスト）</li>
    <li>クラウドインフラストラクチャ（AWS SAA、AWS DVA）</li>
    <li>アジャイル開発（CSM、CSPO、A-CSM）</li>
    <li>情報セキュリティ（情報処理安全確保支援士）</li>
    <li>生成AI活用（Claude、ChatGPT等の実践的活用）</li>
  </ul>

  <p><strong>プロジェクト実績:</strong></p>
  <ul style="margin-left: 1.5rem; line-height: 1.8;">
    <li>大規模Webシステムの設計・開発・運用</li>
    <li>クラウド移行プロジェクトのリード</li>
    <li>アジャイル開発チームの立ち上げ・育成</li>
    <li>セキュリティ監査・改善プロジェクト</li>
  </ul>

  <p>これらの経験を通じて得た知識と実践的なノウハウを、このブログを通じて共有しています。</p>
</div>
</section>
'''

    # ブログの目的セクションのHTML
    purpose_section_html = '''
<!-- ブログの目的セクション -->
<section class="section">
<h2 class="section-title">このブログについて</h2>
<p class="bio-text" style="line-height: 1.8;">
「しかく猫の部屋」は、技術者としての経験と学びを共有し、読者の皆様のスキルアップや問題解決に貢献することを目的としています。
複雑な技術概念を分かりやすく解説し、実践的な活用方法をお伝えすることを心がけています。
</p>

<p class="bio-text" style="line-height: 1.8;">
<strong>コンテンツの方針:</strong>
</p>
<ul style="margin-left: 1.5rem; line-height: 1.8;">
  <li>生成AI技術の最新ニュースと実践的な活用方法</li>
  <li>プログラミング・アプリ開発のチュートリアル</li>
  <li>セキュリティ、クラウド、データベース等の技術解説</li>
  <li>副業・投資に関する実体験と考察</li>
  <li>資格取得の体験記と活用方法</li>
</ul>

<p class="bio-text" style="line-height: 1.8;">
技術の進化に伴い、常に学び続け、その知見を皆様と共有していきます。
</p>
</section>
'''

    # 現在のコンテンツに追加
    # content-sectionの終わり（</div>）の直前に挿入
    content_section_div = soup.find('div', class_='content-section')

    if content_section_div:
        # 新しいセクションをBeautifulSoupのタグとして追加
        operator_soup = BeautifulSoup(operator_section_html, 'html.parser')
        career_soup = BeautifulSoup(career_section_html, 'html.parser')
        purpose_soup = BeautifulSoup(purpose_section_html, 'html.parser')

        # content-sectionの最後に追加
        content_section_div.append(operator_soup)
        content_section_div.append(career_soup)
        content_section_div.append(purpose_soup)

        new_content = str(soup)
    else:
        # content-sectionが見つからない場合は、既存のコンテンツの最後に追加
        new_content = current_content + operator_section_html + career_section_html + purpose_section_html

    if dry_run:
        print("\n" + "=" * 80)
        print("【DRY RUN】プロフィールページプレビュー（最後の1000文字）")
        print("=" * 80)
        print(new_content[-1000:])
        print("=" * 80)
        return True, "DRY RUN完了"

    # 実際に更新
    try:
        update_page_content(page_id, new_content, config)
        return True, "✅ プロフィールページ更新完了"
    except Exception as e:
        return False, f"❌ プロフィールページ更新失敗: {e}"


# =============================================================================
# メイン処理
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='WordPress固定ページ更新スクリプト（AdSense審査対策）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用例:
  # お問い合わせページのみ更新（DRY RUN）
  python update_pages.py --mode contact --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8" --dry-run

  # プロフィールページのみ更新（DRY RUN）
  python update_pages.py --mode profile --dry-run

  # 両方を更新（DRY RUN）
  python update_pages.py --mode all --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8" --dry-run

  # 実際に更新
  python update_pages.py --mode all --google-form-url "https://forms.gle/smgXvkrLdsu9m4rZ8"
        '''
    )

    parser.add_argument(
        '--mode',
        choices=['contact', 'profile', 'all'],
        default='all',
        help='更新モード: contact（お問い合わせページ）, profile（プロフィールページ）, all（両方）'
    )
    parser.add_argument(
        '--google-form-url',
        type=str,
        help='Google FormsのURL (--mode contact または all の場合は必須)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='実際には更新せず、プレビューのみ表示'
    )

    args = parser.parse_args()

    # 設定読み込み
    config = load_config()

    print("=" * 80)
    print("WordPress固定ページ更新スクリプト")
    print("=" * 80)
    print()

    if args.dry_run:
        print("【DRY RUNモード】実際には更新しません\n")

    # お問い合わせページ更新
    if args.mode in ['contact', 'all']:
        if not args.google_form_url:
            print("エラー: --google-form-url が必要です（--mode contact または all の場合）")
            sys.exit(1)

        success, message = update_contact_page(args.google_form_url, config, args.dry_run)
        print(f"\n{message}\n")

        if not success and not args.dry_run:
            sys.exit(1)

    # プロフィールページ更新
    if args.mode in ['profile', 'all']:
        success, message = update_profile_page(config, args.dry_run)
        print(f"\n{message}\n")

        if not success and not args.dry_run:
            sys.exit(1)

    # 完了メッセージ
    print("=" * 80)
    if args.dry_run:
        print("DRY RUN完了")
        print("問題なければ、--dry-run を外して実行してください。")
    else:
        print("✅ すべてのページ更新が完了しました")
        print("\n次のステップ:")
        print("  1. お問い合わせページ確認: https://techsimpleapp.main.jp/お問い合わせ/")
        print("  2. プロフィールページ確認: https://techsimpleapp.main.jp/profile/")
        print("  3. フッターメニュー設定（手動）:")
        print("     - WordPressダッシュボード → 外観 → メニュー")
        print("     - 新しいメニュー作成: 「フッターメニュー」")
        print("     - 4つの固定ページを追加（プロフィール、保有資格、プライバシーポリシー、お問い合わせ）")
        print("     - メニューの位置 → フッターメニューを選択")
    print("=" * 80)


if __name__ == "__main__":
    main()
