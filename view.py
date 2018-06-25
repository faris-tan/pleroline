"""Generic wrapper around views, to be subclassed."""

import urwid

class Base(urwid.WidgetPlaceholder):
    """Base class for views."""

    def __init__(self, main_view, optional_base=None):
        self.main = main_view
        if not optional_base:
            super(Base, self).__init__(urwid.SolidFill('▒'))
        else:
            super(Base, self).__init__(optional_base)
