#!/usr/bin/env python3
"""
AdSense申請前 最終チェックスクリプト

Phase 1-3の全項目を再確認し、AdSense申請の準備が整っているか確認します。

使用方法:
    python final_check.py
"""

import os
import sys
from dotenv import load_dotenv
import requests
from typing import Dict, List

# .envファイルから環境変数を読み込み
load_dotenv()

# 設定
SITE_URL = os.getenv("WORDPRESS_URL", "https://techsimpleapp.main.jp")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_APP_PASSWORD = os.getenv("WORDPRESS_APPLICATION_PASSWORD")

# 色付き出力用のANSIエスケープコード
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str):
    """セクションヘッダーを出力"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")


def print_success(text: str):
    """成功メッセージを出力"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text: str):
    """エラーメッセージを出力"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text: str):
    """警告メッセージを出力"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def print_info(text: str):
    """情報メッセージを出力"""
    print(f"  {text}")


def get_wordpress_posts() -> List[Dict]:
    """WordPressの公開記事を取得"""
    try:
        url = f"{SITE_URL}/wp-json/wp/v2/posts"
        params = {
            "per_page": 100,
            "status": "publish"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print_error(f"記事の取得に失敗: {e}")
        return []


def check_phase1_content() -> Dict[str, bool]:
    """Phase 1: コンテンツ要件をチェック"""
    print_header("Phase 1: コンテンツ要件")

    results = {}

    # 記事取得
    posts = get_wordpress_posts()

    # 1. 記事数チェック
    post_count = len(posts)
    if post_count >= 20:
        print_success(f"記事数: {post_count}記事（目標20-30記事達成）")
        results["post_count"] = True
    else:
        print_error(f"記事数: {post_count}記事（目標20記事未満）")
        results["post_count"] = False

    # 2. 文字数チェック
    if posts:
        word_counts = []
        for post in posts:
            # HTMLタグを除いた文字数をカウント
            content = post.get("content", {}).get("rendered", "")
            # 簡易的な文字数カウント（HTMLタグ除外）
            import re
            text = re.sub(r'<[^>]+>', '', content)
            word_count = len(text.strip())
            word_counts.append(word_count)

        min_words = min(word_counts) if word_counts else 0
        if min_words >= 800:
            print_success(f"最短記事: {min_words}文字（目標800文字以上達成）")
            results["word_count"] = True
        else:
            print_error(f"最短記事: {min_words}文字（800文字未満の記事あり）")
            results["word_count"] = False
    else:
        results["word_count"] = False

    # 3. アイキャッチ画像チェック
    if posts:
        posts_with_featured = sum(1 for post in posts if post.get("featured_media", 0) > 0)
        if posts_with_featured == post_count:
            print_success(f"アイキャッチ画像: 全{post_count}記事に設定済み")
            results["featured_images"] = True
        else:
            print_warning(f"アイキャッチ画像: {posts_with_featured}/{post_count}記事（未設定: {post_count - posts_with_featured}記事）")
            results["featured_images"] = False
    else:
        results["featured_images"] = False

    # その他の項目（手動確認）
    print_info("\n以下の項目は手動で確認してください:")
    print_info("  □ カテゴリ・タグ整理済み")
    print_info("  □ メタディスクリプション全記事設定済み")
    print_info("  □ オリジナルコンテンツ（コピペなし）")
    print_info("  □ 禁止コンテンツなし")

    return results


def check_phase2_pages() -> Dict[str, bool]:
    """Phase 2: 必須ページをチェック"""
    print_header("Phase 2: 必須ページ")

    results = {}

    required_pages = [
        {"path": "/privacy-policy/", "name": "プライバシーポリシー"},
        {"path": "/お問い合わせ/", "name": "お問い合わせ"},
        {"path": "/profile/", "name": "プロフィール"},
    ]

    for page in required_pages:
        url = f"{SITE_URL}{page['path']}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print_success(f"{page['name']}: 存在します")
                results[page['name']] = True
            else:
                print_error(f"{page['name']}: 見つかりません (Status: {response.status_code})")
                results[page['name']] = False
        except Exception as e:
            print_error(f"{page['name']}: 確認失敗 ({e})")
            results[page['name']] = False

    print_info("\n以下の項目は手動で確認してください:")
    print_info("  □ プライバシーポリシーにAdSense利用を明記")
    print_info("  □ お問い合わせページにGoogle Forms埋め込み")
    print_info("  □ プロフィールページに運営者情報・経歴記載")
    print_info("  □ フッターメニュー整備")

    return results


def check_phase3_technical() -> Dict[str, bool]:
    """Phase 3: 技術・SEO要件をチェック"""
    print_header("Phase 3: 技術・SEO要件")

    results = {}

    # 1. HTTPS確認
    if SITE_URL.startswith("https://"):
        print_success("HTTPS: 対応済み")
        results["https"] = True
    else:
        print_error("HTTPS: 未対応（必須）")
        results["https"] = False

    # 2. XMLサイトマップ確認
    sitemap_urls = [
        "/sitemap.xml",
        "/wp-sitemap.xml",
        "/sitemap_index.xml",
    ]

    sitemap_found = False
    for sitemap in sitemap_urls:
        url = f"{SITE_URL}{sitemap}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print_success(f"XMLサイトマップ: {sitemap} が見つかりました")
                sitemap_found = True
                break
        except:
            pass

    if not sitemap_found:
        print_error("XMLサイトマップ: 見つかりません")

    results["sitemap"] = sitemap_found

    # 3. robots.txt確認
    try:
        response = requests.get(f"{SITE_URL}/robots.txt", timeout=10)
        if response.status_code == 200:
            print_success("robots.txt: 存在します")
            results["robots_txt"] = True
        else:
            print_warning("robots.txt: 見つかりません（推奨）")
            results["robots_txt"] = False
    except:
        results["robots_txt"] = False

    print_info("\n以下の項目は手動で確認してください:")
    print_info("  □ Google Analytics設定済み")
    print_info("  □ Google Search Console登録済み")
    print_info("  □ XMLサイトマップ送信済み")
    print_info("  □ モバイルフレンドリーテスト合格")
    print_info("  □ PageSpeed Insights 50点以上")
    print_info("  □ リンク切れ確認済み")

    return results


def print_summary(phase1: Dict, phase2: Dict, phase3: Dict):
    """サマリーと次のステップを出力"""
    print_header("最終チェック結果サマリー")

    # 合格項目数をカウント
    total_checks = len(phase1) + len(phase2) + len(phase3)
    passed_checks = sum([
        sum(phase1.values()),
        sum(phase2.values()),
        sum(phase3.values())
    ])

    print(f"\n自動チェック項目: {passed_checks}/{total_checks} 合格\n")

    # Phase別サマリー
    print(f"{Colors.BOLD}Phase 1: コンテンツ要件{Colors.END}")
    for key, value in phase1.items():
        status = f"{Colors.GREEN}✓{Colors.END}" if value else f"{Colors.RED}✗{Colors.END}"
        print(f"  {status} {key}")

    print(f"\n{Colors.BOLD}Phase 2: 必須ページ{Colors.END}")
    for key, value in phase2.items():
        status = f"{Colors.GREEN}✓{Colors.END}" if value else f"{Colors.RED}✗{Colors.END}"
        print(f"  {status} {key}")

    print(f"\n{Colors.BOLD}Phase 3: 技術・SEO要件{Colors.END}")
    for key, value in phase3.items():
        status = f"{Colors.GREEN}✓{Colors.END}" if value else f"{Colors.RED}✗{Colors.END}"
        print(f"  {status} {key}")

    # 最終判定
    print_header("AdSense申請の準備状況")

    if passed_checks == total_checks:
        print_success("✅ すべての自動チェック項目をクリアしています！")
        print_success("✅ AdSense審査を申請できる準備が整っています。")
        print("\n" + "="*70)
        print(f"{Colors.BOLD}{Colors.GREEN}🎉 おめでとうございます！AdSense申請の準備完了です！{Colors.END}")
        print("="*70 + "\n")
        print_info("次のステップ:")
        print_info("  1. PHASE4_GUIDE.md を参照してAdSense申請手順を確認")
        print_info("  2. https://www.google.com/adsense にアクセス")
        print_info("  3. AdSenseアカウント作成・サイト登録")
        print_info("  4. 審査コード設置")
        print_info("  5. 審査申請")
    else:
        print_warning(f"⚠ {total_checks - passed_checks}個の項目で改善が必要です。")
        print_info("\n改善後、再度このスクリプトを実行してください:")
        print_info("  python final_check.py")


def main():
    """メイン処理"""
    print_header("🎯 AdSense申請前 最終チェック 🎯")
    print_info(f"対象サイト: {SITE_URL}")
    print_info("実行日時: " + __import__('time').strftime('%Y-%m-%d %H:%M:%S'))

    # 各Phaseのチェック実行
    phase1_results = check_phase1_content()
    phase2_results = check_phase2_pages()
    phase3_results = check_phase3_technical()

    # サマリー出力
    print_summary(phase1_results, phase2_results, phase3_results)

    print("\n" + "="*70)
    print_info("詳細な申請手順は PHASE4_GUIDE.md を参照してください")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
