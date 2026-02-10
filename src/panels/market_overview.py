"""
Market Overview Panel - displays indices, volatility, and rates/macro data.
"""

import tkinter as tk
from config import INDICES, VOLATILITY, RATES_MACRO, COLORS, FONTS
from ui_components import QuoteDisplay, LabeledFrame
from utils import get_arrow_emoji, log_error


class MarketOverviewPanel(LabeledFrame):
    """Display market indices, volatility, and rates."""

    def __init__(self, parent, data_fetcher, **kwargs):
        super().__init__(parent, title="Market Overview", **kwargs)

        self.data_fetcher = data_fetcher
        self.quote_widgets = {}

        # Create three-column layout
        columns_frame = tk.Frame(self, bg=COLORS['bg_secondary'])
        columns_frame.pack(fill=tk.BOTH, expand=True)

        # Column 1: Indices
        self.indices_frame = tk.Frame(columns_frame, bg=COLORS['bg_primary'], bd=1, relief=tk.GROOVE)
        self.indices_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=2)
        tk.Label(self.indices_frame, text="Indices", font=FONTS['header'],
                 fg=COLORS['text_primary'], bg=COLORS['bg_primary']).pack(anchor=tk.W, padx=5, pady=2)

        # Column 2: Volatility
        self.volatility_frame = tk.Frame(columns_frame, bg=COLORS['bg_primary'], bd=1, relief=tk.GROOVE)
        self.volatility_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=2)
        tk.Label(self.volatility_frame, text="Volatility", font=FONTS['header'],
                 fg=COLORS['text_primary'], bg=COLORS['bg_primary']).pack(anchor=tk.W, padx=5, pady=2)

        # Column 3: Rates/Macro
        self.rates_frame = tk.Frame(columns_frame, bg=COLORS['bg_primary'], bd=1, relief=tk.GROOVE)
        self.rates_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=2)
        tk.Label(self.rates_frame, text="Rates & Macro", font=FONTS['header'],
                 fg=COLORS['text_primary'], bg=COLORS['bg_primary']).pack(anchor=tk.W, padx=5, pady=2)

        # Create widgets for each symbol
        for symbol, label in INDICES.items():
            widget = QuoteDisplay(self.indices_frame, symbol, 0, 0, "")
            widget.pack(fill=tk.X)
            self.quote_widgets[symbol] = widget

        for symbol, label in VOLATILITY.items():
            widget = QuoteDisplay(self.volatility_frame, symbol, 0, 0, "")
            widget.pack(fill=tk.X)
            self.quote_widgets[symbol] = widget

        for symbol, label in RATES_MACRO.items():
            widget = QuoteDisplay(self.rates_frame, symbol, 0, 0, "")
            widget.pack(fill=tk.X)
            self.quote_widgets[symbol] = widget

    def update_data(self):
        """Fetch data (thread-safe) and schedule UI update on main thread."""
        try:
            # Collect all symbols
            all_symbols = list(INDICES.keys()) + list(VOLATILITY.keys()) + list(RATES_MACRO.keys())

            # Fetch quotes in batch (thread-safe)
            quotes = self.data_fetcher.get_quotes_batch(all_symbols)

            # Schedule UI update on main thread
            self.after(0, lambda q=quotes: self._render(q))

        except Exception as e:
            log_error("Error updating market overview", e)

    def _render(self, quotes):
        """Update widgets on the main thread."""
        try:
            for symbol, quote in quotes.items():
                if symbol in self.quote_widgets:
                    price = quote.get('price', 0) or 0
                    change_pct = quote.get('change_pct', 0) or 0
                    arrow = get_arrow_emoji(change_pct)
                    self.quote_widgets[symbol].update_quote(price, change_pct, arrow)
        except Exception as e:
            log_error("Error rendering market overview", e)

    def clear(self):
        """Clear all data."""
        for widget in self.quote_widgets.values():
            widget.update_quote(0, 0, "")
