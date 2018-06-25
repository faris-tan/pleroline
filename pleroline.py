#!/usr/bin/env python
"""Main executable for the pleroline application. A CLI pleroma client."""
import sys
import urwid

#pylint: disable=too-few-public-methods
class PleroApp(object):
    """Pleroline main app, entry point of everything."""

    @staticmethod
    def create_title(text):
        """Returns a title widget."""
        text_label = urwid.Text(text)
        widgets = [
            urwid.Padding(urwid.Text('~', align='left')),
            text_label,
            urwid.Padding(urwid.Text('~', align='right')),
        ]
        container = urwid.Columns(widgets)
        return urwid.LineBox(container)

    def __init__(self):
        # This is the main application's view, a container widget to be filled
        # by whatever is currently in the scene.
        self.main_view = urwid.SolidFill('x')
        self.header = PleroApp.create_title(
            'Pleroline - A Pleroma client.')
        self.footer = PleroApp.create_title('by Faris <faris@nyan.cafe>')
        self.frame = urwid.Frame(
            urwid.LineBox(self.main_view),
            header=self.header,
            footer=self.footer,
            focus_part='body')

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
            new_view: a urwid container widget.
        """
        self.main_view = new_view
        self.frame.body = urwid.LineBox(self.main_view)

    #def temp_handler(self, _):
    #    # Example for future use on how to replace widgets.
    #    # new_widget = urwid.SolidFill('o')
    #    # self.replace_view(new_widget)
    #    # Example on how to set header/footer
    #    # self.set_footer('hello world')
    #    # self.set_header('foo bar')

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
