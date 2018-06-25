#!/usr/bin/env python
"""Main executable for the pleroline application. A CLI pleroma client."""
from pathlib import Path
import sys

import urwid

import config
from login_view import LoginView
from auth import Auth

#pylint: disable=too-many-instance-attributes
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

    def _set_up_auth(self):
        auth = Auth(self.config.configs['instance'])
        try:
            app_creds = self.config.load_app_cred()
        except config.MissingAppAuthFileError:
            app_creds = auth.get_app_credentials()
            self.config.save_app_cred(app_creds[0], app_creds[1])
        try:
            token = self.config.load_user_cred()
            self.api = auth.get_api_client(token, app_creds)
        except config.MissingUserAuthFileError:
            self.api = None

    def __init__(self):
        self.config = config.Config(str(Path.home()))
        if self.config.is_first_run():
            # TODO:This is super ugly, I'll fix it one day.
            print('This is a first run, the pleroline software is missing a '
                  'config file. Please create ~/.pleroline/pleroline.cfg file '
                  'and make sure its contents look like this:')
            print('')
            print('[DEFAULT]')
            print('instance = nyan.cafe')
            print('')
            print('')
            print('I\'m sorry but this software is too dumb yet to deal with '
                  'this kind of shit automatically. I\'ll fix it one day, I '
                  'promise! - Faris')
            sys.exit(1)
        self.config.load_config()
        # I hate python.
        self.api = None
        self.main_view = None
        self.views = None
        self.frame = None
        self.header = None
        self.footer = None
        self._set_up_views()
        self._set_up_auth()

        if not self.api:
            # TODO: login view here
            pass
        else:
            # TODO: main view here
            pass

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
        urwid.MainLoop(self.frame).run()
#pylint: enable=too-few-public-methods
#pylint: enable=too-many-instance-attributes

#pylint: disable=unused-argument
def main(argv=None):
    """Main function."""
    app = PleroApp()
    app.Run()
    return 0
#pylint: enable=unused-argument

if __name__ == '__main__':
    sys.exit(main(sys.argv))
