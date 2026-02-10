# Getting Started with Daily Markets Dashboard

## Quick Start (5 minutes)

### 1. Run the App (Easiest Way)

**On macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

**On Windows:**
```bash
python src/main.py
```

**On Any Platform:**
```bash
python3 -m pip install -r requirements.txt
python3 src/main.py
```

That's it! The app will:
- Install dependencies (if needed)
- Launch the dashboard
- Start fetching market data
- Display all 6 panels within 5 seconds

### 2. Add API Keys (Optional)

For enhanced features, you can add free API keys:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys
# You can add one or all - the app works without any!
```

Optional API keys:
- **Alpha Vantage**: https://www.alphavantage.co/ (sign up for free key)
- **FRED**: https://fred.stlouisfed.org/docs/api/ (sign up for free key)
- **Polygon.io**: https://polygon.io/ (optional, free tier)
- **Finnhub**: https://finnhub.io/ (optional, free tier)

## What You'll See

When you launch the app, you'll see 6 panels:

### Panel 1: Market Overview (Top)
```
Indices        Volatility       Rates & Macro
SPY: $693 ...  VIX: 17.36 ...  10Y: 4.12% ...
QQQ: $614 ...  VIX9D: ...      2Y: 3.95% ...
DIA: $39k ...  VVIX: ...       Dollar: 103 ...
```

### Panel 2 & 3: Movers & Volatility (Middle Row)
```
Top Gainers          Top Losers           Volatility Heat Map
AMD: +3.6% ...       TSLA: -2.1% ...      AAPL: IV 25% (avg: 22) 🔥
MSFT: +3.1% ...      META: -1.5% ...      MSFT: IV 18% (avg: 19) 🟡
```

### Panel 4 & 5: News & Calendars (Bottom Row)
```
Market News                Economic Calendar
[8:42am] Fed Powell ...   8:30am - Jobless Claims
[7:15am] NVIDIA earnings  10:00am - Fed Chair Speech
```

## Common Tasks

### Change What Stocks to Track

Edit `src/config.py`:

```python
# Lines 22-27: Change indices
INDICES = {
    'SPY': 'S&P 500',
    'QQQ': 'Nasdaq',
    'DIA': 'Dow Jones',
    'IWM': 'Russell 2000',
    'VTI': 'Total Market',  # Add your own!
}

# Lines 46-51: Change IV stocks
IV_STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'NVIDIA', 'GRANDPA']
```

### Speed Up/Slow Down Refreshes

Edit `src/config.py`:

```python
MARKET_HOURS_INTERVAL = 60        # 1 minute (default)
MARKET_HOURS_INTERVAL = 30        # 30 seconds (faster)
MARKET_HOURS_INTERVAL = 300       # 5 minutes (slower)
```

### Change Colors (Dark to Light Theme)

Edit `src/config.py` COLORS section:

```python
COLORS = {
    'bg_primary': '#1e1e1e',      # Dark background (change to '#ffffff' for light)
    'text_primary': '#ffffff',     # White text (change to '#000000' for light)
    # etc...
}
```

## Troubleshooting

### Problem: "ModuleNotFoundError"
**Solution:** Make sure dependencies are installed:
```bash
python3 -m pip install -r requirements.txt
```

### Problem: Takes >5 seconds to load
**Solution:**
- Check your internet connection
- Reduce the number of stocks to track in `config.py`
- Wait a moment and try again (API might be slow)

### Problem: No data showing
**Solution:**
- Check internet connection
- Try clicking the "🔄 Refresh" button
- Check `app.log` for errors
- Verify symbols are valid (e.g., SPY not SP500)

### Problem: "Permission denied" on run.sh
**Solution:**
```bash
chmod +x run.sh
```

### Problem: "No module named 'tkinter'"
**Solution:**
```bash
# macOS
brew install python3
# Windows - reinstall Python and check "tcl/tk and IDLE"
# Linux
sudo apt-get install python3-tk
```

## Next Steps

1. **Launch the app**: `./run.sh` or `python3 src/main.py`
2. **Wait for data**: Watch the loading spinner - should complete in <5 seconds
3. **Explore**: Click through all 6 panels
4. **Customize**: Edit `src/config.py` to track different symbols
5. **Keep it open**: The app auto-refreshes every 1-5 minutes (depending on market hours)

## File Guide

| File | Purpose |
|------|---------|
| `run.sh` | Easy launcher script |
| `src/main.py` | Main application |
| `src/config.py` | Settings you can customize |
| `src/data_fetcher.py` | Gets market data from APIs |
| `src/panels/` | Individual dashboard panels |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
| `.env.example` | Template for API keys |

## Tips & Tricks

**Tip 1:** The app uses your computer's system time. Make sure your clock is correct.

**Tip 2:** Keep the app running in a window all day. It auto-refreshes with fresh data.

**Tip 3:** Click "🔄 Refresh" to manually update without waiting for auto-refresh.

**Tip 4:** If a data source is slow, it won't block other panels - they load independently.

**Tip 5:** Check `app.log` to see what's happening behind the scenes.

## Is This Real-Time Data?

- **Market Hours (9:30am-4pm ET)**: ~30 second delay (standard for free APIs)
- **Premarket (7am-9:30am)**: Varies by source
- **News Headlines**: 1-5 minutes delayed
- **Economic Calendar**: Real-time when available

For professional-grade real-time data, you'd need a paid Bloomberg Terminal or similar.

## Getting Help

1. Check this file first
2. Read `README.md` for detailed docs
3. Check `app.log` for error messages
4. Review `src/config.py` comments for customization options
5. Verify your API keys (if using them)

## Features Coming Soon

- ✅ All core features working!
- 🔜 Custom watchlists
- 🔜 Desktop notifications
- 🔜 Price charts
- 🔜 Export to CSV
- 🔜 Light theme
- 🔜 Mobile app

---

**Enjoy the Daily Markets Dashboard!** 📊

For detailed docs, see [README.md](README.md)
