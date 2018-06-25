#!/usr/bin/env python
"""Main executable for the pleroline application. A CLI pleroma client."""
from pathlib import Path
import sys

import mastodon
import urwid

import config
from login_view import LoginView

#pylint: disable=too-few-public-methods
class PleroApp(object):
    """Pleroline main app, entry point of everything."""

    @staticmethod
    def create_title(text):
        """Returns a title widget."""
        text_label = urwid.Text(text, align='center')
        return urwid.LineBox(text_label)

    def _set_up_views(self):
        # This is the main application's view, a container widget to be filled
        # by whatever is currently in the scene.
        self.header = PleroApp.create_title(
            'Pleroline - A Pleroma client.')
        self.footer = PleroApp.create_title('by Faris <faris@nyan.cafe>')
        self.frame = urwid.Frame(
            urwid.LineBox(self.main_view),
            header=self.header,
            footer=self.footer,
            focus_part='body')
        self.views = {}
        self.views['login'] = LoginView(self)
        self.replace_view('login')

    def __init__(self):
        self.config = config.Config(str(Path.home()))
        self.config.load_config()
        # I hate python.
        self.api = None
        self.main_view = None
        self.views = None
        self.frame = None
        self.header = None
        self.footer = None
        self._set_up_views()

    def set_footer(self, text):
        """Sets the footer text.

        Args:
            text: str, the new footer message.
        """
        self.footer = PleroApp.create_title(text)
        self.frame.footer = self.footer

    def set_header(self, text):
        """Sets the header text.

        Args:
            text: str, the new header message.
        """
        self.header = PleroApp.create_title(text)
        self.frame.header = self.header

    def replace_view(self, new_view):
        """Replace the old main_view with a new one, for a scene manager.

        Args:
            new_view: str, view key in the views map.
        """
        self.main_view = new_view
        self.frame.body = urwid.LineBox(self.views[self.main_view])

    def Run(self):
        """Call this method to start the app."""
        urwid.MainLoop(self.frame).run() # , unhandled_input=self.temp_handler).run()
#pylint: enable=too-few-public-methods

#pylint: disable=unused-argument
def main(argv=None):
    """Main function."""
    app = PleroApp()
    app.Run()
    return 0
#pylint: enable=unused-argument

if __name__ == '__main__':
    sys.exit(main(sys.argv))
