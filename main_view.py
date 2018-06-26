"""Main pleroline client view."""
import urwid

import view

class MainView(view.Base):
    """Main Pleroline view when a user is logged in."""

    def __init__(self, main_view):
        super(MainView, self).__init__(main_view)
