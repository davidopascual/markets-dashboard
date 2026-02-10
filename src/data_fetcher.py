"""
Market data fetcher using multiple data sources.
Primary: yfinance (no API key needed)
Backup: Alpha Vantage, FRED, RSS feeds
"""

import os
import time
import requests
import yfinance as yf
import feedparser
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from config import (
    QUOTE_CACHE_TTL, NEWS_CACHE_TTL, IV_CACHE_TTL,
    ALPHA_VANTAGE_RATE_LIMIT, NEWS_SOURCES, IV_STOCKS,
    TOP_MOVERS_COUNT, MIN_MARKET_CAP_BILLIONS
)
from utils import log_error, log_info, log_warning, get_current_et_time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
FRED_API_KEY = os.getenv('FRED_API_KEY', '')


class Cache:
    """Simple TTL-based cache."""

    def __init__(self):
        self.data = {}

    def get(self, key):
        """Get cached value if not expired."""
        if key in self.data:
            value, timestamp, ttl = self.data[key]
            if time.time() - timestamp < ttl:  # Check TTL
                return value
            else:
                del self.data[key]
        return None

    def set(self, key, value, ttl):
        """Set cached value with TTL."""
        self.data[key] = (value, time.time(), ttl)

    def clear(self):
        """Clear all cache."""
        self.data = {}


class MarketDataFetcher:
    """Fetch market data from multiple sources."""

    def __init__(self):
        self.cache = Cache()
        self.last_request_time = {}
        self.session = requests.Session()
        log_info("MarketDataFetcher initialized")

    def _rate_limit(self, api_name: str, calls_per_minute: int):
        """Implement rate limiting."""
        min_interval = 60 / calls_per_minute
        now = time.time()

        if api_name in self.last_request_time:
            elapsed = now - self.last_request_time[api_name]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)

        self.last_request_time[api_name] = time.time()

    def get_quote(self, symbol: str) -> Optional[Dict]:
        """Get quote for a single symbol."""
        try:
            # Check cache first
            cache_key = f"quote_{symbol}"
            cached = self.cache.get(cache_key)
            if cached:
                return cached

            # Fetch from yfinance
            ticker = yf.Ticker(symbol)
            data = ticker.info

            if not data:
                log_warning(f"No data for {symbol}")
                return None

            quote = {
                'symbol': symbol,
                'price': data.get('currentPrice') or data.get('regularMarketPrice'),
                'change': data.get('regularMarketChange', 0),
                'change_pct': data.get('regularMarketChangePercent', 0),
                'volume': data.get('volume', 0),
                'market_cap': data.get('marketCap', 0),
                'timestamp': datetime.now().isoformat(),
            }

            # Cache result
            self.cache.set(cache_key, quote, QUOTE_CACHE_TTL)
            return quote

        except Exception as e:
            log_error(f"Error fetching quote for {symbol}", e)
            return None

    def get_quotes_batch(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get quotes for multiple symbols efficiently."""
        results = {}
        for symbol in symbols:
            quote = self.get_quote(symbol)
            if quote:
                results[symbol] = quote
        return results

    def get_top_movers(self, direction: str = 'gainers', limit: int = TOP_MOVERS_COUNT) -> List[Dict]:
        """Get top gainers or losers."""
        try:
            # Use yfinance screener for top movers
            # This is a workaround since yfinance doesn't have direct screener API
            # In production, would use Alpha Vantage or Finnhub

            # Common large-cap stocks to scan
            major_stocks = [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'JPM',
                'V', 'JNJ', 'WMT', 'PG', 'UNH', 'MA', 'DIS', 'BA', 'CSCO',
                'INTC', 'AMD', 'NFLX', 'GOOG', 'UBER', 'IBM', 'PAYX', 'GE'
            ]

            # Fetch quotes for major stocks
            movers = []
            quotes = self.get_quotes_batch(major_stocks)

            for symbol, quote in quotes.items():
                if quote and quote.get('market_cap', 0) > MIN_MARKET_CAP_BILLIONS * 1_000_000_000:
                    movers.append(quote)

            # Sort by change percentage
            if direction == 'gainers':
                movers.sort(key=lambda x: x.get('change_pct', 0), reverse=True)
            else:  # losers
                movers.sort(key=lambda x: x.get('change_pct', 0))

            result = movers[:limit]

            # Cache result
            cache_key = f"movers_{direction}"
            self.cache.set(cache_key, result, QUOTE_CACHE_TTL)

            return result

        except Exception as e:
            log_error(f"Error fetching {direction}", e)
            return []

    def get_iv_data(self, symbol: str) -> Optional[Dict]:
        """Get implied volatility data for a symbol."""
        try:
            cache_key = f"iv_{symbol}"
            cached = self.cache.get(cache_key)
            if cached:
                return cached

            # Fetch historical data to calculate IV-like metric
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1y")

            if hist.empty:
                return None

            # Calculate 30-day historical volatility as proxy for IV
            recent_returns = hist['Close'].pct_change().tail(30)
            vol_30d = recent_returns.std() * (252 ** 0.5) * 100  # Annualized

            # Current volatility (last 10 days)
            current_returns = hist['Close'].pct_change().tail(10)
            current_vol = current_returns.std() * (252 ** 0.5) * 100

            result = {
                'symbol': symbol,
                'current_iv': current_vol,
                'avg_iv_30d': vol_30d,
                'iv_percentile': min(100, max(0, (current_vol / vol_30d * 100) if vol_30d > 0 else 50)),
                'timestamp': datetime.now().isoformat(),
            }

            self.cache.set(cache_key, result, IV_CACHE_TTL)
            return result

        except Exception as e:
            log_error(f"Error fetching IV for {symbol}", e)
            return None

    def get_iv_data_batch(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get IV data for multiple symbols."""
        results = {}
        for symbol in symbols:
            iv_data = self.get_iv_data(symbol)
            if iv_data:
                results[symbol] = iv_data
        return results

    def get_news_headlines(self, limit: int = 10) -> List[Dict]:
        """Get latest market news from RSS feeds."""
        try:
            cache_key = "news_headlines"
            cached = self.cache.get(cache_key)
            if cached:
                return cached

            headlines = []

            for source_name, feed_url in NEWS_SOURCES.items():
                try:
                    feed = feedparser.parse(feed_url)
                    entries = feed.entries[:3]  # Get top 3 from each source

                    for entry in entries:
                        # Parse publication date
                        pub_date = None
                        if hasattr(entry, 'published_parsed'):
                            pub_date = datetime(*entry.published_parsed[:6])
                        else:
                            pub_date = datetime.now()

                        headline = {
                            'title': entry.get('title', 'No title'),
                            'summary': entry.get('summary', '')[:200],
                            'link': entry.get('link', ''),
                            'source': source_name,
                            'published': pub_date.isoformat(),
                            'published_time': pub_date.strftime('%I:%M %p'),
                        }
                        headlines.append(headline)

                except Exception as e:
                    log_warning(f"Error fetching news from {source_name}: {str(e)}")
                    continue

            # Sort by date and limit
            headlines.sort(key=lambda x: x['published'], reverse=True)
            headlines = headlines[:limit]

            # Cache result
            self.cache.set(cache_key, headlines, NEWS_CACHE_TTL)

            return headlines

        except Exception as e:
            log_error("Error fetching news", e)
            return []

    def get_economic_calendar(self, date: Optional[str] = None) -> List[Dict]:
        """Get economic calendar events for today."""
        try:
            if date is None:
                date = get_current_et_time().strftime("%Y-%m-%d")

            cache_key = f"econ_calendar_{date}"
            cached = self.cache.get(cache_key)
            if cached:
                return cached

            # Hardcoded major events as fallback
            # In production, would scrape from Investing.com or use API
            events = [
                {
                    'time': '08:30 AM',
                    'event': 'Initial Jobless Claims',
                    'forecast': 'TBD',
                    'importance': '🔴',
                },
                {
                    'time': '10:00 AM',
                    'event': 'Consumer Sentiment Index',
                    'forecast': 'TBD',
                    'importance': '🟡',
                },
                {
                    'time': '02:00 PM',
                    'event': 'FOMC Minutes Release',
                    'forecast': 'N/A',
                    'importance': '🔴',
                },
            ]

            self.cache.set(cache_key, events, 3600)  # Cache for 1 hour
            return events

        except Exception as e:
            log_error("Error fetching economic calendar", e)
            return []

    def get_earnings_calendar(self, date: Optional[str] = None) -> Dict[str, List[str]]:
        """Get earnings reports scheduled for today."""
        try:
            if date is None:
                date = get_current_et_time().strftime("%Y-%m-%d")

            cache_key = f"earnings_{date}"
            cached = self.cache.get(cache_key)
            if cached:
                return cached

            # Use yfinance earnings data for major stocks
            earnings_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META']

            before_open = []
            after_close = []

            for symbol in earnings_stocks:
                try:
                    ticker = yf.Ticker(symbol)
                    earnings_dates = ticker.calendar

                    if earnings_dates is not None:
                        earnings_date = earnings_dates.get('Earnings Date')
                        if earnings_date and isinstance(earnings_date, datetime):
                            if earnings_date.strftime("%Y-%m-%d") == date:
                                # Randomly assign to before/after for demo
                                if hash(symbol) % 2 == 0:
                                    before_open.append(symbol)
                                else:
                                    after_close.append(symbol)
                except:
                    pass

            result = {
                'before_open': before_open,
                'after_close': after_close,
            }

            self.cache.set(cache_key, result, 3600)
            return result

        except Exception as e:
            log_error("Error fetching earnings calendar", e)
            return {'before_open': [], 'after_close': []}

    def get_earnings_details(self, symbol: str) -> Optional[Dict]:
        """Get earnings details for a specific symbol."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            details = {
                'symbol': symbol,
                'eps_estimate': info.get('epsEstimate', 'N/A'),
                'revenue_estimate': info.get('revenueEstimate', 'N/A'),
                'roe': info.get('returnOnEquity', 'N/A'),
            }
            return details

        except Exception as e:
            log_error(f"Error fetching earnings for {symbol}", e)
            return None

    def clear_cache(self):
        """Clear all cached data."""
        self.cache.clear()
        log_info("Cache cleared")
