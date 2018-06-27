"""Generic wrapper around views, to be subclassed."""
import os

import urwid

import error

class Base(urwid.PopUpLauncher):
    """Base class for views."""

    def __init__(self, main_view, optional_base=None):
        self.main = main_view
        if not optional_base:
            self.base = urwid.SolidFill('▒')
        else:
            self.base = optional_base
        self.error_dialog = error.ErrorDialog()
        urwid.connect_signal(self.error_dialog, 'close',
                             lambda button: self.close_pop_up())
        super(Base, self).__init__(self.base)

    def get_pop_up_parameters(self):
        rows, cols = os.popen('stty size', 'r').read().split()
        return {'left': int(cols) / 2 - 40 / 2,
                'top': int(rows) / 2 - 10,
                'overlay_width': 40,
                'overlay_height': 10}

    def create_pop_up(self):
        return self.error_dialog

    def spawn_error(self, msg):
        """Spawns an error message.

        Args:
            msg: str, the error message to show in the popup.
        """
        self.error_dialog.set_error_message(msg)
        self.open_pop_up()
