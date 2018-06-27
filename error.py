"""Error popup widget module."""

import urwid

import style
import utils

class ErrorDialog(urwid.WidgetWrap):
    """Error dialog widget."""
    signals = ['close']

    def __init__(self):
        close_button = urwid.Button('OK')
        urwid.connect_signal(close_button, 'click',
                             lambda button: self.on_click())
        self.message = urwid.Text('')
        widgets = [
            urwid.Text('Error'),
            self.message,
            urwid.LineBox(close_button)]
        super(ErrorDialog, self).__init__(
            urwid.AttrWrap(utils.create_pile_flow(widgets, 35, 'center'),
                           style.ATTRS['error']))

    def set_error_message(self, msg):
        """Sets the error message for the next window spawn.

        Args:
            msg: str, the error message.
        """
        self.message.set_text(msg)

    def on_click(self):
        """Event called when the ok button is clicked."""
        self.message.set_text('')
        self._emit('close')
#
