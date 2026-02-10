"""
Biggest Movers Panel - displays top gainers and losers.
"""

import tkinter as tk
from config import TOP_MOVERS_COUNT, COLORS, FONTS
from ui_components import StockRow, LabeledFrame
from utils import get_arrow_emoji, format_volume, log_error


class MoversPanel(LabeledFrame):
    """Display top gainers and losers."""

    def __init__(self, parent, data_fetcher, **kwargs):
        super().__init__(parent, title="Biggest Movers", **kwargs)

        self.data_fetcher = data_fetcher
        self.mover_widgets = {'gainers': [], 'losers': []}

        # Create two-column layout
        columns_frame = tk.Frame(self, bg=COLORS['bg_secondary'])
        columns_frame.pack(fill=tk.BOTH, expand=True)

        # Column 1: Gainers
        self.gainers_frame = tk.Frame(columns_frame, bg=COLORS['bg_primary'], bd=1, relief=tk.GROOVE)
        self.gainers_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=2)
        tk.Label(self.gainers_frame, text="Top Gainers", font=FONTS['header'],
                 fg=COLORS['positive'], bg=COLORS['bg_primary']).pack(anchor=tk.W, padx=5, pady=2)

        # Column 2: Losers
        self.losers_frame = tk.Frame(columns_frame, bg=COLORS['bg_primary'], bd=1, relief=tk.GROOVE)
        self.losers_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=2)
        tk.Label(self.losers_frame, text="Top Losers", font=FONTS['header'],
                 fg=COLORS['negative'], bg=COLORS['bg_primary']).pack(anchor=tk.W, padx=5, pady=2)

        # Create placeholder widgets for gainers and losers
        for i in range(TOP_MOVERS_COUNT):
            widget = StockRow(self.gainers_frame, "---", 0, 0, 0, "")
            widget.pack(fill=tk.X)
            self.mover_widgets['gainers'].append(widget)

        for i in range(TOP_MOVERS_COUNT):
            widget = StockRow(self.losers_frame, "---", 0, 0, 0, "")
            widget.pack(fill=tk.X)
            self.mover_widgets['losers'].append(widget)

    def update_data(self):
        """Fetch data (thread-safe) and schedule UI update on main thread."""
        try:
            gainers = self.data_fetcher.get_top_movers(direction='gainers', limit=TOP_MOVERS_COUNT)
            losers = self.data_fetcher.get_top_movers(direction='losers', limit=TOP_MOVERS_COUNT)

            self.after(0, lambda g=gainers, l=losers: self._render(g, l))

        except Exception as e:
            log_error("Error updating movers", e)

    def _render(self, gainers, losers):
        """Update widgets on the main thread."""
        try:
            for i, mover in enumerate(gainers):
                if i < len(self.mover_widgets['gainers']):
                    price = mover.get('price', 0) or 0
                    change_pct = mover.get('change_pct', 0) or 0
                    volume = mover.get('volume', 0) or 0
                    arrow = get_arrow_emoji(change_pct)
                    volume_ratio = max(1.0, volume / 5_000_000) if volume > 0 else 1.0

                    widget = self.mover_widgets['gainers'][i]
                    widget.label.configure(
                        text=f"{mover['symbol']}: ${price:,.2f} ({change_pct:+.2f}%) | Vol: {volume_ratio:.1f}x avg {arrow}",
                        fg=COLORS['positive']
                    )

            for i, mover in enumerate(losers):
                if i < len(self.mover_widgets['losers']):
                    price = mover.get('price', 0) or 0
                    change_pct = mover.get('change_pct', 0) or 0
                    volume = mover.get('volume', 0) or 0
                    arrow = get_arrow_emoji(change_pct)
                    volume_ratio = max(1.0, volume / 5_000_000) if volume > 0 else 1.0

                    widget = self.mover_widgets['losers'][i]
                    widget.label.configure(
                        text=f"{mover['symbol']}: ${price:,.2f} ({change_pct:+.2f}%) | Vol: {volume_ratio:.1f}x avg {arrow}",
                        fg=COLORS['negative']
                    )
        except Exception as e:
            log_error("Error rendering movers", e)

    def clear(self):
        """Clear all data."""
        for widgets in self.mover_widgets.values():
            for widget in widgets:
                widget.label.configure(text="---")
