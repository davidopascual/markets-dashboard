"""
Daily Markets Dashboard - Main Application
Desktop app displaying essential market data every morning.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
import threading
from datetime import datetime
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, THEME, COLORS, FONTS,
    MARKET_HOURS_INTERVAL, PREMARKET_INTERVAL, AFTERHOURS_INTERVAL, OVERNIGHT_INTERVAL
)
from data_fetcher import MarketDataFetcher
from ui_components import RefreshButton, StatusBar, LoadingSpinner
from panels.market_overview import MarketOverviewPanel
from panels.movers import MoversPanel
from panels.volatility_heatmap import VolatilityHeatMapPanel
from panels.news import NewsPanel
from panels.economic_calendar import EconomicCalendarPanel
from panels.earnings_calendar import EarningsCalendarPanel
from panels.charts import ChartsPanel
from utils import (
    log_info, log_error, is_market_hours, is_premarket, is_after_hours,
    get_market_status, get_current_et_time, format_time_et
)


class MarketsDashboard(tk.Tk):
    """Main dashboard application."""

    def __init__(self):
        super().__init__()

        # Configure window
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(bg=COLORS['bg_primary'])

        # Initialize data fetcher
        self.data_fetcher = MarketDataFetcher()

        # State
        self.is_loading = False
        self.refresh_timer = None
        self.panels = {}

        # Create UI
        self.create_layout()

        # Load initial data
        self.load_initial_data()

        log_info(f"Application started. Window size: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    def create_layout(self):
        """Create the main layout."""
        # Top bar with refresh button and status
        top_bar = tk.Frame(self, bg=COLORS['bg_primary'])
        top_bar.pack(fill=tk.X, padx=5, pady=5)

        # Title
        title_label = tk.Label(
            top_bar,
            text="Daily Markets Dashboard",
            font=('Helvetica', 14, 'bold'),
            fg=COLORS['text_primary'],
            bg=COLORS['bg_primary']
        )
        title_label.pack(side=tk.LEFT)

        # Refresh button
        self.refresh_btn = RefreshButton(top_bar, command=self.manual_refresh)
        self.refresh_btn.pack(side=tk.RIGHT, padx=10)

        # Status bar
        self.status_bar = StatusBar(self)
        self.status_bar.pack(fill=tk.X)

        # Separator
        separator = tk.Frame(self, bg=COLORS['text_secondary'], height=1)
        separator.pack(fill=tk.X)

        # Loading spinner (hidden initially, shows itself when started)
        self.loading_spinner = LoadingSpinner(self)

        # Main content area
        self.content_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Market Overview (full width, top)
        overview = MarketOverviewPanel(self.content_frame, self.data_fetcher)
        overview.pack(fill=tk.X, pady=5)
        self.panels['overview'] = overview

        # Charts panel (full width, below overview)
        charts = ChartsPanel(self.content_frame, self.data_fetcher)
        charts.pack(fill=tk.X, pady=5)
        self.panels['charts'] = charts

        # Middle row: Movers and Volatility (side by side)
        middle_frame = tk.Frame(self.content_frame, bg=COLORS['bg_primary'])
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        movers = MoversPanel(middle_frame, self.data_fetcher)
        movers.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        self.panels['movers'] = movers

        volatility = VolatilityHeatMapPanel(middle_frame, self.data_fetcher)
        volatility.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        self.panels['volatility'] = volatility

        # Bottom row: News (left) and Calendars (right, stacked)
        bottom_frame = tk.Frame(self.content_frame, bg=COLORS['bg_primary'])
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        news = NewsPanel(bottom_frame, self.data_fetcher)
        news.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        self.panels['news'] = news

        # Right column: calendars
        calendar_frame = tk.Frame(bottom_frame, bg=COLORS['bg_primary'])
        calendar_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)

        econ_calendar = EconomicCalendarPanel(calendar_frame, self.data_fetcher)
        econ_calendar.pack(fill=tk.BOTH, expand=True, pady=2)
        self.panels['econ_calendar'] = econ_calendar

        earnings = EarningsCalendarPanel(calendar_frame, self.data_fetcher)
        earnings.pack(fill=tk.BOTH, expand=True, pady=2)
        self.panels['earnings'] = earnings

    def load_initial_data(self):
        """Load initial data in a separate thread."""
        if self.is_loading:
            return

        self.is_loading = True
        self.loading_spinner.start()
        self.refresh_btn.config(state='disabled')
        self.status_bar.update_status("Loading market data...")

        # Fetch data in background thread
        thread = threading.Thread(target=self._load_data_thread, daemon=True)
        thread.start()

    def _load_data_thread(self):
        """Load data in background thread."""
        try:
            # Fetch data for all panels in parallel
            threads = []

            def fetch_overview():
                if 'overview' in self.panels:
                    self.panels['overview'].update_data()

            def fetch_movers():
                if 'movers' in self.panels:
                    self.panels['movers'].update_data()

            def fetch_volatility():
                if 'volatility' in self.panels:
                    self.panels['volatility'].update_data()

            def fetch_news():
                if 'news' in self.panels:
                    self.panels['news'].update_data()

            def fetch_econ():
                if 'econ_calendar' in self.panels:
                    self.panels['econ_calendar'].update_data()

            def fetch_earnings():
                if 'earnings' in self.panels:
                    self.panels['earnings'].update_data()

            def fetch_charts():
                if 'charts' in self.panels:
                    self.panels['charts'].update_data()

            threads.append(threading.Thread(target=fetch_overview, daemon=True))
            threads.append(threading.Thread(target=fetch_movers, daemon=True))
            threads.append(threading.Thread(target=fetch_volatility, daemon=True))
            threads.append(threading.Thread(target=fetch_news, daemon=True))
            threads.append(threading.Thread(target=fetch_econ, daemon=True))
            threads.append(threading.Thread(target=fetch_earnings, daemon=True))
            threads.append(threading.Thread(target=fetch_charts, daemon=True))

            # Start all threads
            for t in threads:
                t.start()

            # Wait for all to complete
            for t in threads:
                t.join(timeout=30)

            # Update UI on main thread
            self.after(0, self._finish_loading)

        except Exception as e:
            log_error("Error loading data", e)
            self.after(0, self._finish_loading)

    def _finish_loading(self):
        """Finish loading and update UI."""
        self.is_loading = False
        self.loading_spinner.stop()
        self.refresh_btn.config(state='normal')

        # Update status
        market_status = get_market_status()
        current_time = format_time_et(get_current_et_time())
        self.status_bar.update_status(f"Status: {market_status}")
        self.status_bar.update_time(current_time)

        log_info("Data loading completed")

        # Schedule next refresh
        self.schedule_refresh()

    def schedule_refresh(self):
        """Schedule the next auto-refresh based on market hours."""
        # Cancel existing timer
        if self.refresh_timer:
            self.after_cancel(self.refresh_timer)

        # Determine refresh interval
        if is_market_hours():
            interval = MARKET_HOURS_INTERVAL
        elif is_premarket():
            interval = PREMARKET_INTERVAL
        elif is_after_hours():
            interval = AFTERHOURS_INTERVAL
        else:
            interval = OVERNIGHT_INTERVAL

        # Schedule next refresh
        interval_ms = interval * 1000
        self.refresh_timer = self.after(interval_ms, self.auto_refresh)
        log_info(f"Next refresh scheduled in {interval} seconds")

    def auto_refresh(self):
        """Auto-refresh data."""
        if not self.is_loading:
            self.load_initial_data()

    def manual_refresh(self):
        """Manual refresh triggered by user."""
        log_info("Manual refresh triggered")
        self.data_fetcher.clear_cache()
        self.load_initial_data()

    def on_closing(self):
        """Handle window closing."""
        log_info("Application closing")
        if self.refresh_timer:
            self.after_cancel(self.refresh_timer)
        self.destroy()


def main():
    """Main entry point."""
    try:
        app = MarketsDashboard()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as e:
        log_error("Fatal error in main", e)
        raise


if __name__ == "__main__":
    main()
