#!/usr/bin/env python3
"""
サイト検証スクリプト - Phase 3用

WordPress サイトの技術・SEO要件をチェックします。
- XMLサイトマップの存在確認
- robots.txtの確認
- 必須ページの存在確認
- HTTPS確認
- レスポンスタイム測定

使用方法:
    python verify_site.py
"""

import os
import sys
import time
from typing import Dict, List, Tuple
import requests
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# 設定
SITE_URL = os.getenv("WORDPRESS_URL", "https://techsimpleapp.main.jp")

# チェック対象のサイトマップURL（複数パターン）
SITEMAP_URLS = [
    "/wp-sitemap.xml",          # WordPress標準（5.5以降）
    "/sitemap_index.xml",       # Yoast SEO、Rank Math
    "/sitemap.xml",             # All in One SEO
]

# チェック対象の必須ページ
REQUIRED_PAGES = [
    {"path": "/", "name": "トップページ"},
    {"path": "/profile/", "name": "プロフィール"},
    {"path": "/privacy-policy/", "name": "プライバシーポリシー"},
    {"path": "/お問い合わせ/", "name": "お問い合わせ"},
]

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
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


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
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def check_url_exists(url: str, timeout: int = 10) -> Tuple[bool, int, float]:
    """
    URLが存在するか確認し、ステータスコードとレスポンスタイムを返す

    Returns:
        (存在するか, ステータスコード, レスポンスタイム秒)
    """
    try:
        start_time = time.time()
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        response_time = time.time() - start_time

        return response.status_code == 200, response.status_code, response_time
    except requests.RequestException as e:
        return False, 0, 0.0


def check_xml_sitemap() -> Dict[str, any]:
    """XMLサイトマップの存在をチェック"""
    print_header("1. XMLサイトマップ確認")

    results = []
    found_sitemap = None

    for sitemap_path in SITEMAP_URLS:
        url = f"{SITE_URL}{sitemap_path}"
        exists, status_code, response_time = check_url_exists(url)

        results.append({
            "path": sitemap_path,
            "url": url,
            "exists": exists,
            "status_code": status_code,
            "response_time": response_time
        })

        if exists:
            print_success(f"{sitemap_path} が見つかりました")
            print_info(f"   URL: {url}")
            print_info(f"   レスポンスタイム: {response_time:.2f}秒")
            found_sitemap = url
        else:
            print_error(f"{sitemap_path} が見つかりません (Status: {status_code})")

    if found_sitemap:
        print_success(f"\n使用するサイトマップ: {found_sitemap}")
    else:
        print_error("\nXMLサイトマップが見つかりませんでした")
        print_warning("対処方法:")
        print_warning("  1. WordPressバージョンが5.5以上か確認")
        print_warning("  2. SEOプラグイン（Yoast SEO、All in One SEO）をインストール")
        print_warning("  3. プラグインでサイトマップ機能を有効化")

    return {
        "found": found_sitemap is not None,
        "sitemap_url": found_sitemap,
        "results": results
    }


def check_robots_txt() -> Dict[str, any]:
    """robots.txtの確認"""
    print_header("2. robots.txt確認")

    url = f"{SITE_URL}/robots.txt"
    exists, status_code, response_time = check_url_exists(url)

    if exists:
        print_success(f"robots.txt が見つかりました")
        print_info(f"   URL: {url}")
        print_info(f"   レスポンスタイム: {response_time:.2f}秒")

        # robots.txtの内容を取得して表示
        try:
            response = requests.get(url)
            print_info("\n--- robots.txt の内容 ---")
            print(response.text)
            print_info("--- robots.txt の内容ここまで ---\n")
        except:
            print_warning("robots.txtの内容を取得できませんでした")
    else:
        print_warning(f"robots.txt が見つかりません (Status: {status_code})")
        print_info("注意: robots.txtは必須ではありませんが、推奨されます")

    return {
        "found": exists,
        "url": url,
        "status_code": status_code,
        "response_time": response_time
    }


def check_required_pages() -> Dict[str, any]:
    """必須ページの存在確認"""
    print_header("3. 必須ページ確認")

    results = []
    all_found = True

    for page in REQUIRED_PAGES:
        url = f"{SITE_URL}{page['path']}"
        exists, status_code, response_time = check_url_exists(url)

        results.append({
            "name": page['name'],
            "path": page['path'],
            "url": url,
            "exists": exists,
            "status_code": status_code,
            "response_time": response_time
        })

        if exists:
            print_success(f"{page['name']}: OK")
            print_info(f"   URL: {url}")
            print_info(f"   レスポンスタイム: {response_time:.2f}秒")
        else:
            print_error(f"{page['name']}: 見つかりません (Status: {status_code})")
            all_found = False

    if all_found:
        print_success("\nすべての必須ページが存在します")
    else:
        print_error("\n一部の必須ページが見つかりませんでした")
        print_warning("AdSense審査前に必ず作成してください")

    return {
        "all_found": all_found,
        "results": results
    }


def check_https() -> Dict[str, any]:
    """HTTPS対応確認"""
    print_header("4. HTTPS確認")

    if SITE_URL.startswith("https://"):
        print_success("HTTPS対応済みです")

        # HTTPからのリダイレクトを確認
        http_url = SITE_URL.replace("https://", "http://")
        try:
            response = requests.get(http_url, allow_redirects=False, timeout=10)
            if response.status_code in [301, 302]:
                print_success("HTTP→HTTPSのリダイレクト設定済み")
            else:
                print_warning("HTTP→HTTPSのリダイレクトが設定されていません")
                print_warning("セキュリティ向上のため、リダイレクト設定を推奨します")
        except:
            print_warning("HTTPアクセスの確認に失敗しました")

        return {"https_enabled": True}
    else:
        print_error("HTTPSが有効ではありません")
        print_error("AdSense審査の必須要件です。至急HTTPS化してください")
        return {"https_enabled": False}


def print_summary_and_next_steps(
    sitemap_result: Dict,
    robots_result: Dict,
    pages_result: Dict,
    https_result: Dict
):
    """サマリーと次のステップを出力"""
    print_header("5. サマリーと次のステップ")

    # 合格/不合格判定
    passed_checks = []
    failed_checks = []

    if https_result["https_enabled"]:
        passed_checks.append("HTTPS対応")
    else:
        failed_checks.append("HTTPS対応")

    if sitemap_result["found"]:
        passed_checks.append("XMLサイトマップ")
    else:
        failed_checks.append("XMLサイトマップ")

    if pages_result["all_found"]:
        passed_checks.append("必須ページ")
    else:
        failed_checks.append("必須ページ")

    # robots.txtは任意
    if robots_result["found"]:
        passed_checks.append("robots.txt")

    print_success(f"合格項目 ({len(passed_checks)}):")
    for check in passed_checks:
        print(f"  ✓ {check}")

    if failed_checks:
        print_error(f"\n改善必要項目 ({len(failed_checks)}):")
        for check in failed_checks:
            print(f"  ✗ {check}")
    else:
        print_success("\nすべての必須項目をクリアしています！")

    # Phase 3の次のステップ
    print_header("次のステップ")

    print_info("1. Google Search Console登録")
    print(f"   https://search.google.com/search-console")
    print(f"   サイトURL: {SITE_URL}")

    if sitemap_result["found"]:
        print_info(f"\n2. XMLサイトマップ送信")
        print(f"   Google Search Console → サイトマップ")
        print(f"   サイトマップURL: {sitemap_result['sitemap_url']}")
    else:
        print_warning(f"\n2. XMLサイトマップ作成（未完了）")
        print(f"   PHASE3_GUIDE.md の手順を参照してください")

    print_info("\n3. モバイルフレンドリーテスト")
    print(f"   https://search.google.com/test/mobile-friendly?url={SITE_URL}")

    print_info("\n4. PageSpeed Insights")
    print(f"   https://pagespeed.web.dev/?url={SITE_URL}")

    print_info("\n5. リンク切れ確認")
    print(f"   https://www.brokenlinkcheck.com/")
    print(f"   または WordPress プラグイン「Broken Link Checker」を使用")

    print_info("\n詳細な手順は PHASE3_GUIDE.md を参照してください")


def main():
    """メイン処理"""
    print_header(f"WordPress サイト検証 - Phase 3")
    print_info(f"対象サイト: {SITE_URL}")
    print_info(f"実行日時: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 各種チェック実行
    sitemap_result = check_xml_sitemap()
    robots_result = check_robots_txt()
    pages_result = check_required_pages()
    https_result = check_https()

    # サマリーと次のステップ
    print_summary_and_next_steps(
        sitemap_result,
        robots_result,
        pages_result,
        https_result
    )

    print("\n" + "="*60)
    print_success("サイト検証が完了しました")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
