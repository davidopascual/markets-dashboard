"""
Earnings Calendar Panel - displays today's earnings reports.
"""

import tkinter as tk
from config import COLORS, FONTS
from ui_components import LabeledFrame
from utils import log_error


class EarningsCalendarPanel(LabeledFrame):
    """Display today's earnings reports."""

    def __init__(self, parent, data_fetcher, **kwargs):
        super().__init__(parent, title="Earnings Calendar", **kwargs)

        self.data_fetcher = data_fetcher
        self.earnings_widgets = []

        # Create frame for earnings
        self.earnings_frame = tk.Frame(self, bg=COLORS['bg_secondary'])
        self.earnings_frame.pack(fill=tk.BOTH, expand=True)

    def update_data(self):
        """Fetch data (thread-safe) and schedule UI update on main thread."""
        try:
            earnings = self.data_fetcher.get_earnings_calendar()
            self.after(0, lambda e=earnings: self._render(e))

        except Exception as e:
            log_error("Error updating earnings calendar", e)

    def _render(self, earnings):
        """Update widgets on the main thread."""
        try:
            # Clear existing widgets
            for widget in self.earnings_widgets:
                widget.destroy()
            self.earnings_widgets = []

            before_open = earnings.get('before_open', [])
            after_close = earnings.get('after_close', [])

            if before_open:
                before_label = tk.Label(
                    self.earnings_frame,
                    text="Before Open:",
                    font=FONTS['header'],
                    fg=COLORS['text_primary'],
                    bg=COLORS['bg_secondary']
                )
                before_label.pack(anchor=tk.W, padx=5, pady=5)

                before_text = ", ".join(before_open)
                before_stocks = tk.Label(
                    self.earnings_frame,
                    text=before_text,
                    font=FONTS['body'],
                    fg=COLORS['positive'],
                    bg=COLORS['bg_secondary']
                )
                before_stocks.pack(anchor=tk.W, padx=15, pady=2)
                self.earnings_widgets.extend([before_label, before_stocks])

            if after_close:
                after_label = tk.Label(
                    self.earnings_frame,
                    text="After Close:",
                    font=FONTS['header'],
                    fg=COLORS['text_primary'],
                    bg=COLORS['bg_secondary']
                )
                after_label.pack(anchor=tk.W, padx=5, pady=5)

                after_text = ", ".join(after_close)
                after_stocks = tk.Label(
                    self.earnings_frame,
                    text=after_text,
                    font=FONTS['body'],
                    fg=COLORS['negative'],
                    bg=COLORS['bg_secondary']
                )
                after_stocks.pack(anchor=tk.W, padx=15, pady=2)
                self.earnings_widgets.extend([after_label, after_stocks])

            if not before_open and not after_close:
                placeholder = tk.Label(
                    self.earnings_frame,
                    text="No earnings scheduled for today",
                    font=FONTS['body'],
                    fg=COLORS['text_secondary'],
                    bg=COLORS['bg_secondary']
                )
                placeholder.pack(pady=20)
                self.earnings_widgets.append(placeholder)
        except Exception as e:
            log_error("Error rendering earnings calendar", e)

    def clear(self):
        """Clear all earnings."""
        for widget in self.earnings_widgets:
            widget.destroy()
        self.earnings_widgets = []
