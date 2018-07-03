"""Main pleroline client view."""
import urwid

import view

class MainView(view.Base):
    """Main Pleroline view when a user is logged in."""

    @staticmethod
    def calculate_window_size():
        """Returns the (rows, cols) tuple of the drawable window."""
        (rows, cols) = view.Base.get_term_size()
        # Removing header/footer.
        return (rows - 6, cols)


    def __init__(self, main_view):
        self.reply_box = None
        self.left_pane = urwid.ListBox(
            urwid.SimpleFocusListWalker([]))
        self.mid_pane = urwid.ListBox(
            urwid.SimpleFocusListWalker([
                urwid.Text('Mid Pane', align='center')]))
        self.right_pane = urwid.ListBox(
            urwid.SimpleFocusListWalker([
                urwid.Text('Right Pane', align='center')]))
        (rows, cols) = MainView.calculate_window_size()
        boxes = [self.left_pane, self.mid_pane, self.right_pane]
        #TODO: Figure out how to make cell_width change on term resize.
        grid = urwid.GridFlow(
            [urwid.LineBox(urwid.BoxAdapter(b, height=rows-4)) for b in boxes],
            cell_width=int(cols/3)-1, h_sep=0, v_sep=0, align='center')
        self.create_reply_box()
        super(MainView, self).__init__(
            main_view, optional_base=urwid.Filler(grid))

    def create_reply_box(self):
        """Generates the reply box widget on the left pane."""
        #TODO: This is just a mess of spaghetti code. Make it more flexible.
        self.reply_box = urwid.Edit(
            caption='', edit_text='Just landed in L.A.', multiline=True)
        #TODO: Make the text_counter increase/decrease characters based on
        #      the contents of the reply_box.
        text_counter = urwid.Text('0/5000', align='right')
        post_button = urwid.Button('Submit')
        container = urwid.BoxAdapter(
            urwid.ListBox(
                urwid.SimpleFocusListWalker([
                    urwid.LineBox(
                        urwid.BoxAdapter(
                            urwid.Filler(self.reply_box), height=7)),
                    urwid.GridFlow(
                        [post_button, text_counter], align='right',
                        cell_width=30, h_sep=0, v_sep=0)])),
            height=10)
        self.left_pane.body.append(container)
        urwid.connect_signal(
            post_button, 'click', self.send_post)

    def send_post(self, _):
        """Send post to the mastodon API."""
        post = self.reply_box.get_edit_text()
        self.main.api.toot(post)
        #TODO: Remove duplicated string. Also probably remove this text anyway.
        self.reply_box.set_edit_text('Just landed in L.A.')
