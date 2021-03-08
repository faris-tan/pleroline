#!/usr/bin/env python
"""Main executable for the pleroline application. A CLI pleroma client."""
from pathlib import Path
import sys

import urwid
import mastodon

from auth import Auth
import config
from login_view import LoginView
from main_view import MainView
import style

#pylint: disable=too-many-instance-attributes
#pylint: disable=too-few-public-methods
class PleroApp():
    """Pleroline main app, entry point of everything."""

    @staticmethod
    def create_title(text):
        """Returns a title widget."""
        text_label = urwid.Text(text, align='center')
        return urwid.AttrWrap(urwid.LineBox(text_label),
                              style.ATTRS['head/foot'])

    def _set_up_views(self):
        # This is the main application's view, a container widget to be filled
        # by whatever is currently in the scene.
        self.header = PleroApp.create_title(
            'Pleroline - A Pleroma client.')
        self.footer = PleroApp.create_title('by Faris <faris@nyan.cafe>')
        self.views = {}
        self.views['login'] = LoginView(self)
        self.views['main'] = MainView(self)
        self.frame = urwid.Frame(
            urwid.LineBox(self.views['main']),
            header=self.header,
            footer=self.footer,
            focus_part='body')


    def _set_up_auth(self):
        self.auth = Auth(self.config.configs['instance'])
        try:
            app_creds = self.config.load_app_cred()
        except config.MissingAppAuthFileError:
            app_creds = self.auth.get_app_credentials()
            self.config.save_app_cred(app_creds[0], app_creds[1])
        try:
            token = self.config.load_user_cred()
            self.api = self.auth.get_api_client(token, app_creds)
        except config.MissingUserAuthFileError:
            self.api = None

    def __init__(self):
        # TODO: Have proper color palette for different ranges (8, 16, 256)
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
        self.auth = None
        self._set_up_views()
        self._set_up_auth()

        if not self.api:
            self.replace_view('login')
        else:
            self.replace_view('main')

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

    def try_log_in(self, email, password):
        """Tries to log into the pleroma instance.

        If successful, self.api will be set to the appropriate
        value.

        Args:
            email: str, the user's email.
            password: str, the user's password.

        Returns:
            (True, '') in case of success.
            (False, error) in case of failure, where error is a str with the
            error message.
        """
        app_creds = self.config.load_app_cred()
        try:
            token = self.auth.log_in_user(email, password, app_creds)
            self.api = self.auth.get_api_client(token, app_creds)
        except (mastodon.MastodonAPIError,
                mastodon.MastodonIllegalArgumentError) as err:
            return (False, str(err))
        self.config.save_user_cred(token)
        return (True, '')

    def replace_view(self, new_view):
        """Replace the old main_view with a new one, for a scene manager.

        Args:
            new_view: str, view key in the views map.
        """
        self.main_view = new_view
        self.frame.body = urwid.LineBox(self.views[self.main_view])
        #XXX: hack
        if new_view == 'main':
            self.views[self.main_view].refresh_mid_pane()

    @staticmethod
    def timed_refresh(main_loop, self):
        """Refresh the main page every 2 seconds."""
        if self.main_view == 'main':
            self.replace_view('main')
        main_loop.set_alarm_in(2.0, self.timed_refresh, user_data=self)

    def Run(self):
        """Call this method to start the app."""
        def _show_or_exit(key):
            """Handler for stray inputs in the urwid main loop"""
            if key in ('q', 'Q', 'esc'):
                raise urwid.ExitMainLoop()
        loop = urwid.MainLoop(
            self.frame,
            style.BASE_ATTRS,
            handle_mouse=True,
            unhandled_input=_show_or_exit,
            pop_ups=True)
        # TODO - Have the refresh timer set and read from the app configs
        loop.set_alarm_in(2.0, self.timed_refresh, user_data=self)
        loop.run()
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
