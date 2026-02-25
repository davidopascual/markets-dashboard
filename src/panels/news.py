"""
News Panel - displays market headlines from multiple sources.
"""

import tkinter as tk
from config import COLORS, FONTS
from ui_components import NewsItem, LabeledFrame, ScrollableFrame
from utils import log_error


class NewsPanel(LabeledFrame):
    """Display latest market news."""

    def __init__(self, parent, data_fetcher, **kwargs):
        super().__init__(parent, title="Market News", **kwargs)

        self.data_fetcher = data_fetcher
        self.news_widgets = []

        # Create scrollable content area
        self.scrollable = ScrollableFrame(self)
        self.scrollable.pack(fill=tk.BOTH, expand=True)

    def update_data(self):
        """Fetch data (thread-safe) and schedule UI update on main thread."""
        try:
            headlines = self.data_fetcher.get_news_headlines(limit=10)
            self.after(0, lambda h=headlines: self._render(h))

        except Exception as e:
            log_error("Error updating news", e)

    def _render(self, headlines):
        """Update widgets on the main thread."""
        try:
            # Clear existing widgets
            for widget in self.news_widgets:
                widget.destroy()
            self.news_widgets = []

            for headline in headlines:
                time_str = headline.get('published_time', 'N/A')
                title = headline.get('title', 'No title')
                source = headline.get('source', 'Unknown')

                link = headline.get('link', '')

                widget = NewsItem(
                    self.scrollable.scrollable_frame,
                    time_str,
                    title,
                    source,
                    link=link
                )
                widget.pack(fill=tk.X, pady=5)
                self.news_widgets.append(widget)

            if not headlines:
                placeholder = tk.Label(
                    self.scrollable.scrollable_frame,
                    text="No news available",
                    font=FONTS['body'],
                    fg=COLORS['text_secondary'],
                    bg=COLORS['bg_primary']
                )
                placeholder.pack(pady=20)
                self.news_widgets.append(placeholder)
        except Exception as e:
            log_error("Error rendering news", e)

    def clear(self):
        """Clear all news."""
        for widget in self.news_widgets:
            widget.destroy()
        self.news_widgets = []
