"""
Utility functions for the Markets Dashboard.
"""

import logging
from datetime import datetime, time
import pytz
from config import LOG_FILE, LOG_LEVEL

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Eastern Time Zone
ET = pytz.timezone('US/Eastern')


def get_current_et_time():
    """Get current time in Eastern Time."""
    return datetime.now(ET)


def is_market_hours():
    """Check if current time is during market hours (9:30 AM - 4:00 PM ET)."""
    now = get_current_et_time()
    market_open = time(9, 30)
    market_close = time(16, 0)

    # Only during weekdays
    if now.weekday() >= 5:  # Saturday=5, Sunday=6
        return False

    return market_open <= now.time() < market_close


def is_premarket():
    """Check if current time is premarket (7:00 AM - 9:30 AM ET)."""
    now = get_current_et_time()
    premarket_start = time(7, 0)
    market_open = time(9, 30)

    # Only during weekdays
    if now.weekday() >= 5:
        return False

    return premarket_start <= now.time() < market_open


def is_after_hours():
    """Check if current time is after hours (4:00 PM - 8:00 PM ET)."""
    now = get_current_et_time()
    market_close = time(16, 0)
    after_hours_end = time(20, 0)

    # Only during weekdays
    if now.weekday() >= 5:
        return False

    return market_close <= now.time() < after_hours_end


def get_market_status():
    """Get current market status as string."""
    if is_market_hours():
        return "MARKET OPEN"
    elif is_premarket():
        return "PREMARKET"
    elif is_after_hours():
        return "AFTER HOURS"
    else:
        return "CLOSED"


def format_currency(value):
    """Format value as currency string."""
    if value is None:
        return "N/A"
    try:
        return f"${value:,.2f}"
    except (TypeError, ValueError):
        return "N/A"


def format_percentage(value, decimals=2):
    """Format value as percentage string."""
    if value is None:
        return "N/A"
    try:
        sign = "+" if value >= 0 else ""
        return f"{sign}{value:.{decimals}f}%"
    except (TypeError, ValueError):
        return "N/A"


def format_volume(volume):
    """Format volume as human-readable string."""
    if volume is None:
        return "N/A"
    try:
        volume = int(volume)
        if volume >= 1_000_000_000:
            return f"{volume / 1_000_000_000:.1f}B"
        elif volume >= 1_000_000:
            return f"{volume / 1_000_000:.1f}M"
        elif volume >= 1_000:
            return f"{volume / 1_000:.1f}K"
        else:
            return str(volume)
    except (TypeError, ValueError):
        return "N/A"


def get_arrow_emoji(change_percent):
    """Get directional arrow emoji based on change."""
    if change_percent is None:
        return ""
    try:
        if change_percent > 0:
            return "⬆️"
        elif change_percent < 0:
            return "⬇️"
        else:
            return "➡️"
    except (TypeError, ValueError):
        return ""


def get_market_data_type():
    """Determine what type of data to show based on market hours."""
    if is_market_hours():
        return "live"
    elif is_premarket() or is_after_hours():
        return "premarket"
    else:
        return "previous_close"


def format_time_et(dt):
    """Format datetime as ET time string."""
    if dt is None:
        return "N/A"
    try:
        if not isinstance(dt, datetime):
            return str(dt)

        # Convert to ET if needed
        if dt.tzinfo is None:
            dt = ET.localize(dt)
        else:
            dt = dt.astimezone(ET)

        return dt.strftime("%I:%M %p")
    except Exception as e:
        logger.error(f"Error formatting time: {e}")
        return "N/A"


def log_info(message):
    """Log info message."""
    logger.info(message)


def log_error(message, exception=None):
    """Log error message."""
    if exception:
        logger.error(f"{message}: {str(exception)}")
    else:
        logger.error(message)


def log_warning(message):
    """Log warning message."""
    logger.warning(message)


def safe_divide(numerator, denominator):
    """Safely divide two numbers, handling division by zero."""
    if denominator is None or denominator == 0:
        return None
    try:
        return numerator / denominator
    except (TypeError, ZeroDivisionError):
        return None


def get_iv_color_code(current_iv, avg_iv):
    """Get color code emoji for IV heat map based on comparison to average."""
    if current_iv is None or avg_iv is None or avg_iv == 0:
        return "⚪"  # White - neutral

    try:
        ratio = (current_iv - avg_iv) / avg_iv

        if ratio > 0.10:  # >10% above average
            return "🔥"  # Red
        elif ratio >= 0.05:  # 5-10% above
            return "🟡"  # Yellow
        elif ratio >= -0.05:  # Within ±5%
            return "⚪"  # White
        else:  # <5% below (and more)
            return "🔵"  # Blue
    except (TypeError, ZeroDivisionError):
        return "⚪"


def get_date_string(days_offset=0):
    """Get date string for specified offset from today."""
    from datetime import timedelta
    date = datetime.now(ET) + timedelta(days=days_offset)
    return date.strftime("%Y-%m-%d")


def is_trading_day():
    """Check if today is a trading day (weekday)."""
    return get_current_et_time().weekday() < 5


def minutes_until_market_open():
    """Get minutes until market opens."""
    now = get_current_et_time()
    if now.weekday() >= 5:  # Weekend
        # Next Monday 9:30 AM
        days_until_monday = 7 - now.weekday()
        next_open = now.replace(day=now.day + days_until_monday, hour=9, minute=30, second=0, microsecond=0)
    else:
        # Tomorrow or today at 9:30 AM
        if now.time() < time(9, 30):
            next_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        else:
            next_open = (now.replace(hour=9, minute=30, second=0, microsecond=0) +
                        __import__('datetime').timedelta(days=1))

    time_diff = next_open - now
    return int(time_diff.total_seconds() / 60)
