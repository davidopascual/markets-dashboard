"""
Economic Calendar Panel - displays today's economic events.
"""

import tkinter as tk
from config import COLORS, FONTS
from ui_components import LabeledFrame
from utils import log_error


class EconomicCalendarPanel(LabeledFrame):
    """Display today's economic events."""

    def __init__(self, parent, data_fetcher, **kwargs):
        super().__init__(parent, title="Economic Calendar", **kwargs)

        self.data_fetcher = data_fetcher
        self.event_widgets = []

        # Create frame for events
        self.events_frame = tk.Frame(self, bg=COLORS['bg_secondary'])
        self.events_frame.pack(fill=tk.BOTH, expand=True)

    def update_data(self):
        """Fetch data (thread-safe) and schedule UI update on main thread."""
        try:
            events = self.data_fetcher.get_economic_calendar()
            self.after(0, lambda e=events: self._render(e))

        except Exception as e:
            log_error("Error updating economic calendar", e)

    def _render(self, events):
        """Update widgets on the main thread."""
        try:
            # Clear existing widgets
            for widget in self.event_widgets:
                widget.destroy()
            self.event_widgets = []

            for event in events:
                event_frame = tk.Frame(self.events_frame, bg=COLORS['bg_primary'])
                event_frame.pack(fill=tk.X, pady=2, padx=2)

                time_label = tk.Label(
                    event_frame,
                    text=event.get('time', ''),
                    font=FONTS['mono'],
                    fg=COLORS['text_secondary'],
                    bg=COLORS['bg_primary'],
                    width=10,
                    anchor='w'
                )
                time_label.pack(side=tk.LEFT, padx=5)

                event_label = tk.Label(
                    event_frame,
                    text=event.get('event', ''),
                    font=FONTS['body'],
                    fg=COLORS['text_primary'],
                    bg=COLORS['bg_primary'],
                    anchor='w'
                )
                event_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

                importance = event.get('importance', '')
                if importance == '🔴':
                    imp_text = 'HIGH'
                    imp_color = COLORS['red']
                elif importance == '🟡':
                    imp_text = 'MED'
                    imp_color = COLORS['yellow']
                else:
                    imp_text = 'LOW'
                    imp_color = COLORS['text_secondary']

                importance_label = tk.Label(
                    event_frame,
                    text=imp_text,
                    font=FONTS['mono'],
                    fg=imp_color,
                    bg=COLORS['bg_primary']
                )
                importance_label.pack(side=tk.RIGHT, padx=5)

                self.event_widgets.append(event_frame)

            if not events:
                placeholder = tk.Label(
                    self.events_frame,
                    text="No economic events scheduled for today",
                    font=FONTS['body'],
                    fg=COLORS['text_secondary'],
                    bg=COLORS['bg_primary']
                )
                placeholder.pack(pady=20)
                self.event_widgets.append(placeholder)
        except Exception as e:
            log_error("Error rendering economic calendar", e)

    def clear(self):
        """Clear all events."""
        for widget in self.event_widgets:
            widget.destroy()
        self.event_widgets = []
