#!/usr/bin/env python3
"""
Test script to verify all dashboard features are working.
Run this before launching the full app to diagnose issues.
"""

import sys
sys.path.insert(0, 'src')

import time
from datetime import datetime

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_header(text):
    print(f"\n{BOLD}{BLUE}{'=' * 60}{RESET}")
    print(f"{BOLD}{BLUE}{text:^60}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 60}{RESET}\n")


def print_test(name, passed, message=""):
    status = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
    print(f"{status} - {name}")
    if message:
        print(f"     {message}")


def test_imports():
    """Test that all imports work."""
    print_header("Testing Imports")

    tests = [
        ("Tkinter", lambda: __import__('tkinter')),
        ("yfinance", lambda: __import__('yfinance')),
        ("requests", lambda: __import__('requests')),
        ("pandas", lambda: __import__('pandas')),
        ("feedparser", lambda: __import__('feedparser')),
        ("Config module", lambda: __import__('config', fromlist=['INDICES'])),
        ("Utils module", lambda: __import__('utils', fromlist=['get_arrow_emoji'])),
        ("DataFetcher", lambda: __import__('data_fetcher', fromlist=['MarketDataFetcher'])),
        ("UI Components", lambda: __import__('ui_components', fromlist=['QuoteDisplay'])),
    ]

    passed = 0
    for name, test_func in tests:
        try:
            test_func()
            print_test(name, True)
            passed += 1
        except Exception as e:
            print_test(name, False, str(e))

    return passed == len(tests)


def test_data_fetching():
    """Test data fetching functionality."""
    print_header("Testing Data Fetching")

    from data_fetcher import MarketDataFetcher

    fetcher = MarketDataFetcher()
    passed = 0
    total = 5

    # Test 1: Single quote
    try:
        start = time.time()
        quote = fetcher.get_quote('SPY')
        elapsed = time.time() - start

        if quote and 'price' in quote:
            print_test("Fetch single quote (SPY)",True,
                      f"${quote['price']:.2f} | {elapsed:.2f}s")
            passed += 1
        else:
            print_test("Fetch single quote (SPY)", False, "No price data")
    except Exception as e:
        print_test("Fetch single quote (SPY)", False, str(e))

    # Test 2: Batch quotes
    try:
        start = time.time()
        quotes = fetcher.get_quotes_batch(['SPY', 'QQQ', '^VIX'])
        elapsed = time.time() - start

        if len(quotes) >= 2:
            print_test("Fetch batch quotes", True,
                      f"{len(quotes)} symbols | {elapsed:.2f}s")
            passed += 1
        else:
            print_test("Fetch batch quotes", False, f"Only got {len(quotes)} symbols")
    except Exception as e:
        print_test("Fetch batch quotes", False, str(e))

    # Test 3: IV data
    try:
        start = time.time()
        iv = fetcher.get_iv_data('AAPL')
        elapsed = time.time() - start

        if iv and 'current_iv' in iv:
            print_test("Fetch IV data (AAPL)", True,
                      f"IV {iv['current_iv']:.1f}% | {elapsed:.2f}s")
            passed += 1
        else:
            print_test("Fetch IV data (AAPL)", False, "No IV data")
    except Exception as e:
        print_test("Fetch IV data (AAPL)", False, str(e))

    # Test 4: Top movers
    try:
        start = time.time()
        gainers = fetcher.get_top_movers(direction='gainers', limit=5)
        elapsed = time.time() - start

        if len(gainers) > 0:
            top = gainers[0]
            print_test("Fetch top movers", True,
                      f"{len(gainers)} gainers | {top['symbol']} +{top['change_pct']:.2f}% | {elapsed:.2f}s")
            passed += 1
        else:
            print_test("Fetch top movers", False, "No movers found")
    except Exception as e:
        print_test("Fetch top movers", False, str(e))

    # Test 5: News
    try:
        start = time.time()
        news = fetcher.get_news_headlines(limit=5)
        elapsed = time.time() - start

        if len(news) > 0:
            headline = news[0]['title'][:50] + "..."
            print_test("Fetch news headlines", True,
                      f"{len(news)} articles | {elapsed:.2f}s")
            passed += 1
        else:
            print_test("Fetch news headlines", False, "No news found")
    except Exception as e:
        print_test("Fetch news headlines", False, str(e))

    return passed, total


def test_utils():
    """Test utility functions."""
    print_header("Testing Utility Functions")

    from utils import (
        get_arrow_emoji, format_currency, format_percentage,
        get_market_status, is_market_hours
    )

    tests_passed = 0
    tests_total = 5

    # Test arrow emoji
    try:
        up = get_arrow_emoji(1.5)
        down = get_arrow_emoji(-1.5)
        neutral = get_arrow_emoji(0)
        if up == "⬆️" and down == "⬇️" and neutral == "➡️":
            print_test("Arrow emoji formatting", True)
            tests_passed += 1
        else:
            print_test("Arrow emoji formatting", False,
                      f"Got: {up}, {down}, {neutral}")
    except Exception as e:
        print_test("Arrow emoji formatting", False, str(e))

    # Test currency formatting
    try:
        formatted = format_currency(1234.56)
        if "$1,234.56" in formatted:
            print_test("Currency formatting", True, formatted)
            tests_passed += 1
        else:
            print_test("Currency formatting", False, f"Got: {formatted}")
    except Exception as e:
        print_test("Currency formatting", False, str(e))

    # Test percentage formatting
    try:
        formatted = format_percentage(1.5)
        if "1.50%" in formatted or "+1.50" in formatted:
            print_test("Percentage formatting", True, formatted)
            tests_passed += 1
        else:
            print_test("Percentage formatting", False, f"Got: {formatted}")
    except Exception as e:
        print_test("Percentage formatting", False, str(e))

    # Test market status
    try:
        status = get_market_status()
        if status in ["MARKET OPEN", "PREMARKET", "AFTER HOURS", "CLOSED"]:
            print_test("Market status", True, f"Status: {status}")
            tests_passed += 1
        else:
            print_test("Market status", False, f"Unknown status: {status}")
    except Exception as e:
        print_test("Market status", False, str(e))

    # Test market hours check
    try:
        market_hours = is_market_hours()
        print_test("Market hours check", True, f"In market hours: {market_hours}")
        tests_passed += 1
    except Exception as e:
        print_test("Market hours check", False, str(e))

    return tests_passed, tests_total


def test_configuration():
    """Test configuration values."""
    print_header("Testing Configuration")

    from config import (
        INDICES, VOLATILITY, RATES_MACRO, IV_STOCKS,
        WINDOW_WIDTH, WINDOW_HEIGHT, NEWS_SOURCES
    )

    tests_passed = 0
    tests_total = 5

    # Test indices
    try:
        if 'SPY' in INDICES and len(INDICES) > 0:
            print_test("Indices configured", True, f"{len(INDICES)} indices")
            tests_passed += 1
        else:
            print_test("Indices configured", False)
    except Exception as e:
        print_test("Indices configured", False, str(e))

    # Test volatility
    try:
        if '^VIX' in VOLATILITY and len(VOLATILITY) > 0:
            print_test("Volatility configured", True, f"{len(VOLATILITY)} symbols")
            tests_passed += 1
        else:
            print_test("Volatility configured", False)
    except Exception as e:
        print_test("Volatility configured", False, str(e))

    # Test IV stocks
    try:
        if 'AAPL' in IV_STOCKS and len(IV_STOCKS) == 10:
            print_test("IV stocks configured", True, f"{len(IV_STOCKS)} stocks")
            tests_passed += 1
        else:
            print_test("IV stocks configured", False, f"Expected 10, got {len(IV_STOCKS)}")
    except Exception as e:
        print_test("IV stocks configured", False, str(e))

    # Test window dimensions
    try:
        if WINDOW_WIDTH == 1200 and WINDOW_HEIGHT == 800:
            print_test("Window dimensions", True, f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
            tests_passed += 1
        else:
            print_test("Window dimensions", False,
                      f"Expected 1200x800, got {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    except Exception as e:
        print_test("Window dimensions", False, str(e))

    # Test news sources
    try:
        if len(NEWS_SOURCES) >= 3:
            sources = ", ".join(NEWS_SOURCES.keys())
            print_test("News sources configured", True, f"{len(NEWS_SOURCES)} sources")
            tests_passed += 1
        else:
            print_test("News sources configured", False, f"Only {len(NEWS_SOURCES)} sources")
    except Exception as e:
        print_test("News sources configured", False, str(e))

    return tests_passed, tests_total


def main():
    """Run all tests."""
    print(f"\n{BOLD}{BLUE}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║   Daily Markets Dashboard - Feature Test Suite          ║")
    print("║   Testing all components and data sources                ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

    start_time = time.time()

    # Run all tests
    imports_ok = test_imports()

    data_passed, data_total = test_data_fetching()
    utils_passed, utils_total = test_utils()
    config_passed, config_total = test_configuration()

    # Summary
    total_passed = (imports_ok and 1 or 0) + data_passed + utils_passed + config_passed
    total_tests = 9 + data_total + utils_total + config_total

    elapsed = time.time() - start_time

    print_header(f"Test Summary - {elapsed:.2f}s")

    print(f"{BOLD}Results:{RESET}")
    print(f"  Imports:       {1 if imports_ok else 0}/1")
    print(f"  Data Fetching: {data_passed}/{data_total}")
    print(f"  Utils:         {utils_passed}/{utils_total}")
    print(f"  Configuration: {config_passed}/{config_total}")
    print(f"\n  {BOLD}Total:         {total_passed}/{total_tests}{RESET}")

    if total_passed == total_tests:
        print(f"\n{GREEN}{BOLD}✓ All tests passed! The dashboard is ready to run.{RESET}")
        print(f"\nStart the dashboard with:")
        print(f"  {BOLD}./run.sh{RESET} (on macOS/Linux)")
        print(f"  {BOLD}python3 src/main.py{RESET} (on any platform)\n")
        return 0
    else:
        print(f"\n{RED}{BOLD}✗ Some tests failed. Check the output above.{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
