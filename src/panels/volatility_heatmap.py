"""
Volatility Heat Map Panel - displays IV vs 30-day average.
"""

import tkinter as tk
from config import IV_STOCKS, COLORS, FONTS
from ui_components import VolatilityBar, LabeledFrame
from utils import get_iv_color_code, log_error


class VolatilityHeatMapPanel(LabeledFrame):
    """Display implied volatility heat map."""

    def __init__(self, parent, data_fetcher, **kwargs):
        super().__init__(parent, title="Volatility Heat Map", **kwargs)

        self.data_fetcher = data_fetcher
        self.iv_widgets = {}

        # Create grid layout for stocks
        grid_frame = tk.Frame(self, bg=COLORS['bg_secondary'])
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Two columns for better layout
        col1 = tk.Frame(grid_frame, bg=COLORS['bg_primary'])
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        col2 = tk.Frame(grid_frame, bg=COLORS['bg_primary'])
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create widgets for each stock
        for i, stock in enumerate(IV_STOCKS):
            parent_frame = col1 if i < len(IV_STOCKS) // 2 else col2
            widget = VolatilityBar(parent_frame, stock, 0, 0, "")
            widget.pack(fill=tk.X)
            self.iv_widgets[stock] = widget

    def update_data(self):
        """Fetch data (thread-safe) and schedule UI update on main thread."""
        try:
            iv_data = self.data_fetcher.get_iv_data_batch(IV_STOCKS)
            self.after(0, lambda d=iv_data: self._render(d))

        except Exception as e:
            log_error("Error updating volatility heat map", e)

    def _render(self, iv_data):
        """Update widgets on the main thread."""
        try:
            for stock in IV_STOCKS:
                if stock in iv_data:
                    data = iv_data[stock]
                    current_iv = data.get('current_iv', 0) or 0
                    avg_iv = data.get('avg_iv_30d', 0) or 0

                    if avg_iv > 0:
                        diff_pct = ((current_iv - avg_iv) / avg_iv) * 100
                    else:
                        diff_pct = 0

                    # Color based on IV vs average
                    if avg_iv > 0:
                        ratio = (current_iv - avg_iv) / avg_iv
                        if ratio > 0.10:
                            fg_color = COLORS['red']
                        elif ratio >= 0.05:
                            fg_color = COLORS['yellow']
                        elif ratio >= -0.05:
                            fg_color = COLORS['text_primary']
                        else:
                            fg_color = COLORS['blue']
                    else:
                        fg_color = COLORS['text_primary']

                    text = f"{stock}: IV {current_iv:.1f}% (avg: {avg_iv:.1f}%) [{diff_pct:+.0f}%]"
                    widget = self.iv_widgets[stock]
                    widget.label.configure(text=text, fg=fg_color)
        except Exception as e:
            log_error("Error rendering volatility heat map", e)

    def clear(self):
        """Clear all data."""
        for stock in IV_STOCKS:
            widget = self.iv_widgets[stock]
            widget.label.configure(
                text=f"{stock}: IV ---% (avg: ---%) [---]",
                fg=COLORS['text_secondary']
            )
