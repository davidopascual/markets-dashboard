"""
Configuration and constants for the Markets Dashboard.
"""

# Window Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Daily Markets Dashboard"
THEME = "darkblue"  # ttk theme

# Market Hours (ET)
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 30
MARKET_CLOSE_HOUR = 16
MARKET_CLOSE_MINUTE = 0
PREMARKET_START_HOUR = 7
PREMARKET_START_MINUTE = 0
AFTERHOURS_END_HOUR = 20
AFTERHOURS_END_MINUTE = 0

# Refresh Intervals (seconds)
MARKET_HOURS_INTERVAL = 60  # 1 minute during market hours
PREMARKET_INTERVAL = 300  # 5 minutes before market open
AFTERHOURS_INTERVAL = 1800  # 30 minutes after market close
OVERNIGHT_INTERVAL = 3600  # 1 hour overnight

# Cache Settings (seconds)
QUOTE_CACHE_TTL = 30
NEWS_CACHE_TTL = 300
ECONOMIC_CALENDAR_CACHE_TTL = 3600
IV_CACHE_TTL = 60

# API Rate Limits (calls per minute)
ALPHA_VANTAGE_RATE_LIMIT = 5
FRED_RATE_LIMIT = 120
POLYGON_RATE_LIMIT = 5
FINNHUB_RATE_LIMIT = 60

# Symbols to Track

# Indices
INDICES = {
    'SPY': 'S&P 500',
    'QQQ': 'Nasdaq',
    'DIA': 'Dow Jones',
    'IWM': 'Russell 2000',
}

# Volatility
VOLATILITY = {
    '^VIX': 'VIX',
    '^VIX9D': 'VIX 9D',
    '^VVIX': 'VVIX',
}

# Rates & Macro
RATES_MACRO = {
    '^TNX': '10Y Treasury',
    '^IRX': '2Y Treasury',
    'DX-Y.NYB': 'Dollar Index',
    'GLD': 'Gold',
    'USO': 'Crude Oil',
}

# Stocks for IV Heat Map
IV_STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'JPM', 'XOM', 'SPY']

# Top Movers Criteria
MIN_MARKET_CAP_BILLIONS = 5  # Only track stocks > $5B market cap
TOP_MOVERS_COUNT = 5  # Show top 5 gainers and losers
MIN_VOLUME_RATIO = 1.0  # Minimum volume compared to average

# News Sources (RSS feeds)
NEWS_SOURCES = {
    'Bloomberg': 'https://feeds.bloomberg.com/markets/news.rss',
    'Reuters': 'http://feeds.reuters.com/reuters/businessNews',
    'CNBC': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
    'WSJ': 'https://feeds.wsj.com/xml/rss/3_7085.xml',
}
NEWS_LIMIT = 10

# Volatility Heat Map Color Coding
IV_COLOR_THRESHOLDS = {
    'red': 0.10,      # > 10% above average: RED
    'yellow': 0.05,   # 5-10% above: YELLOW
    'white': 0.05,    # Within ±5%: WHITE
    'blue': -0.10,    # < -10% below: BLUE
}

# Notification Settings
ENABLE_NOTIFICATIONS = True
VIX_ALERT_THRESHOLD = 0.05  # Alert if VIX moves >5%
STOCK_ALERT_THRESHOLD = 0.10  # Alert if stock moves >10%

# UI Colors (for dark theme)
COLORS = {
    'bg_primary': '#1e1e1e',
    'bg_secondary': '#2d2d2d',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0b0',
    'positive': '#00ff00',
    'negative': '#ff4444',
    'neutral': '#ffff00',
    'red': '#ff4444',
    'yellow': '#ffff00',
    'blue': '#4488ff',
}

# Font Settings
FONTS = {
    'title': ('Helvetica', 12, 'bold'),
    'header': ('Helvetica', 11, 'bold'),
    'body': ('Helvetica', 10),
    'mono': ('Courier', 9),
}

# API Endpoints
API_ENDPOINTS = {
    'alpha_vantage': 'https://www.alphavantage.co/query',
    'fred': 'https://api.stlouisfed.org/fred/series/observations',
    'polygon': 'https://api.polygon.io/v1',
    'finnhub': 'https://finnhub.io/api/v1',
}

# Economic Calendar Events (fallback/hardcoded)
MAJOR_ECONOMIC_EVENTS = [
    'Initial Jobless Claims',
    'Unemployment Rate',
    'Non-Farm Payroll',
    'CPI Release',
    'Core CPI',
    'PPI Release',
    'Fed Meeting',
    'FOMC Minutes',
    'GDP Release',
    'Durable Goods',
    'ISM Manufacturing',
    'ISM Services',
    'Consumer Confidence',
    'Housing Starts',
    'Existing Home Sales',
]

# Logging
LOG_FILE = 'app.log'
LOG_LEVEL = 'INFO'

# Startup Settings
SHOW_SPLASH_SCREEN = True
AUTO_REFRESH_ENABLED = True
LOAD_DATA_IN_PARALLEL = True
TARGET_LOAD_TIME_SECONDS = 5
