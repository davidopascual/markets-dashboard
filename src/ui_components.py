"""
Reusable UI components for the Markets Dashboard.
Uses tk widgets (not ttk) for reliable color rendering on macOS.
"""

import tkinter as tk
from tkinter import ttk
from config import COLORS, FONTS


class QuoteDisplay(tk.Frame):
    """Display a single quote: SYMBOL: $123.45 (+2.3%)"""

    def __init__(self, parent, symbol: str, price: float = 0, change_pct: float = 0,
                 arrow: str = "", **kwargs):
        super().__init__(parent, bg=COLORS['bg_primary'], **kwargs)

        # Create label with quote information
        text = f"{symbol}: ${price:,.2f} ({change_pct:+.2f}%) {arrow}"

        # Determine color based on change
        if change_pct > 0:
            fg_color = COLORS['positive']
        elif change_pct < 0:
            fg_color = COLORS['negative']
        else:
            fg_color = COLORS['text_primary']

        self.label = tk.Label(
            self,
            text=text,
            font=FONTS['body'],
            fg=fg_color,
            bg=COLORS['bg_primary'],
            anchor='w'
        )
        self.label.pack(fill=tk.X, padx=5, pady=2)

    def update_quote(self, price: float, change_pct: float, arrow: str = ""):
        """Update displayed quote."""
        symbol = self.label.cget('text').split(':')[0]
        text = f"{symbol}: ${price:,.2f} ({change_pct:+.2f}%) {arrow}"

        # Update color
        if change_pct > 0:
            fg_color = COLORS['positive']
        elif change_pct < 0:
            fg_color = COLORS['negative']
        else:
            fg_color = COLORS['text_primary']

        self.label.configure(text=text, fg=fg_color)


class StockRow(tk.Frame):
    """Display a stock mover: NVDA: $142.50 (+8.2%) | Vol: 2.3x avg"""

    def __init__(self, parent, symbol: str, price: float = 0, change_pct: float = 0,
                 volume_ratio: float = 0, arrow: str = "", **kwargs):
        super().__init__(parent, bg=COLORS['bg_primary'], **kwargs)

        # Determine color
        if change_pct > 0:
            fg_color = COLORS['positive']
        elif change_pct < 0:
            fg_color = COLORS['negative']
        else:
            fg_color = COLORS['text_primary']

        # Format text
        text = f"{symbol}: ${price:,.2f} ({change_pct:+.2f}%) | Vol: {volume_ratio:.1f}x avg {arrow}"

        self.label = tk.Label(
            self,
            text=text,
            font=FONTS['body'],
            fg=fg_color,
            bg=COLORS['bg_primary'],
            anchor='w'
        )
        self.label.pack(fill=tk.X, padx=5, pady=3)


class VolatilityBar(tk.Frame):
    """Display volatility: AAPL: IV 28.5% (avg: 24.3%) [+17%]"""

    def __init__(self, parent, symbol: str, current_iv: float = 0, avg_iv: float = 0,
                 emoji: str = "", **kwargs):
        super().__init__(parent, bg=COLORS['bg_primary'], **kwargs)

        # Calculate percentage difference
        if avg_iv > 0:
            diff_pct = ((current_iv - avg_iv) / avg_iv) * 100
        else:
            diff_pct = 0

        # Determine text color
        fg_color = COLORS['text_primary']

        # Format text
        text = f"{symbol}: IV {current_iv:.1f}% (avg: {avg_iv:.1f}%) [{diff_pct:+.0f}%]"

        self.label = tk.Label(
            self,
            text=text,
            font=FONTS['body'],
            fg=fg_color,
            bg=COLORS['bg_primary'],
            anchor='w'
        )
        self.label.pack(fill=tk.X, padx=5, pady=2)


class NewsItem(tk.Frame):
    """Display news: [8:42am] Headline text - Source"""

    def __init__(self, parent, time_str: str, headline: str, source: str, **kwargs):
        super().__init__(parent, bg=COLORS['bg_primary'], **kwargs)

        # Time label
        time_label = tk.Label(
            self,
            text=f"[{time_str}]",
            font=FONTS['mono'],
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        )
        time_label.pack(side=tk.LEFT, padx=5)

        # Headline and source
        text = f"{headline} - {source}"
        headline_label = tk.Label(
            self,
            text=text,
            font=FONTS['body'],
            fg=COLORS['text_primary'],
            bg=COLORS['bg_primary'],
            wraplength=800,
            anchor='w',
            justify='left'
        )
        headline_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)


class LoadingSpinner(tk.Frame):
    """Simple animated loading spinner."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['bg_primary'], **kwargs)

        self.spinner_chars = ['|', '/', '-', '\\']
        self.current_index = 0
        self.is_running = False

        self.label = tk.Label(
            self,
            text="Loading market data...",
            font=FONTS['body'],
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        )
        self.label.pack(pady=20)

    def start(self):
        """Start the spinner animation."""
        if not self.is_running:
            self.is_running = True
            self.pack(fill=tk.X)
            self.animate()

    def stop(self):
        """Stop the spinner animation and hide."""
        self.is_running = False
        self.pack_forget()

    def animate(self):
        """Animate the spinner."""
        if self.is_running:
            spinner_char = self.spinner_chars[self.current_index % len(self.spinner_chars)]
            self.label.configure(text=f"{spinner_char} Loading market data...")
            self.current_index += 1
            self.after(100, self.animate)


class ScrollableFrame(tk.Frame):
    """A scrollable frame that adapts to content."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['bg_primary'], **kwargs)

        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, bg=COLORS['bg_primary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)

        # Configure canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)

        # Layout
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create scrollable frame
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS['bg_primary'])
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        # Update scroll region when frame is resized
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)

    def _on_frame_configure(self, event=None):
        """Update scroll region."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")


class LabeledFrame(tk.Frame):
    """Custom labeled frame with consistent dark styling."""

    def __init__(self, parent, title: str, **kwargs):
        super().__init__(parent, bg=COLORS['bg_secondary'], bd=1, relief=tk.GROOVE, **kwargs)

        # Title label
        title_label = tk.Label(
            self,
            text=f" {title} ",
            font=FONTS['header'],
            fg=COLORS['text_primary'],
            bg=COLORS['bg_secondary']
        )
        title_label.pack(anchor=tk.W, padx=5, pady=(5, 2))

        # Separator line
        sep = tk.Frame(self, bg=COLORS['text_secondary'], height=1)
        sep.pack(fill=tk.X, padx=5, pady=(0, 5))


class StatusBar(tk.Frame):
    """Status bar showing market status and last update time."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['bg_primary'], **kwargs)

        self.status_label = tk.Label(
            self,
            text="Initializing...",
            font=FONTS['body'],
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.time_label = tk.Label(
            self,
            text="",
            font=FONTS['body'],
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        )
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def update_status(self, status: str):
        """Update status text."""
        self.status_label.configure(text=status)

    def update_time(self, time_str: str):
        """Update time text."""
        self.time_label.configure(text=f"Last update: {time_str}")


class RefreshButton(tk.Button):
    """Styled refresh button."""

    def __init__(self, parent, command=None, **kwargs):
        super().__init__(
            parent,
            text="Refresh",
            command=command,
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            activebackground=COLORS['bg_primary'],
            activeforeground=COLORS['text_primary'],
            relief=tk.RAISED,
            bd=1,
            **kwargs
        )


class PanelContainer(tk.Frame):
    """Container for dashboard panels with consistent layout."""

    def __init__(self, parent, title: str, **kwargs):
        super().__init__(parent, bg=COLORS['bg_primary'], **kwargs)

        # Title bar
        title_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        title_frame.pack(fill=tk.X, padx=5, pady=5)

        title_label = tk.Label(
            title_frame,
            text=title,
            font=FONTS['header'],
            fg=COLORS['text_primary'],
            bg=COLORS['bg_primary']
        )
        title_label.pack(side=tk.LEFT)

        # Separator
        separator = tk.Frame(self, bg=COLORS['text_secondary'], height=1)
        separator.pack(fill=tk.X, padx=5)

        # Content frame
        self.content = tk.Frame(self, bg=COLORS['bg_primary'])
        self.content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
