"""Module containing the Toot class which encapsulate user data for Toots."""
from html.parser import HTMLParser

import urwid

class Toot():
    def __init__(self, username, display_name, contents):
        self.username = username
        self.display_name = display_name
        self.contents = contents
        self.plain_contents = self.parse_contents()

    def display(self):
        """Wraps toots around the relevant urwid widgets and returns it."""
        return self._wrap_toot_in_widgets()

    def parse_contents(self):
        """Parses HTML contents of the toot."""
        parser = TootParser()
        parser.feed(self.contents)
        return parser.get_plain_text()

    def _wrap_toot_in_widgets(self):
        username_widget = urwid.Text(self.username)
        display_name_widget = urwid.Text(self.display_name)
        contents_widget = urwid.Text(self.plain_contents)
        box = urwid.LineBox(
            urwid.Pile([
                urwid.Columns([display_name_widget, username_widget]),
                contents_widget]))
        return box

class TootParser(HTMLParser):

    def __init__(self):
        super(TootParser, self).__init__()
        self.text = ''

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        self.text += data

    def handle_comment(self, data):
        # we ignore comments intentionally, they shouldn't exist.
        pass

    def handle_decl(self, decl):
        # we ignore decls intentionally, they shouldn't exist.
        pass

    def get_plain_text(self):
        return self.text
