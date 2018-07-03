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
        self.left_pane = urwid.ListBox(
            [urwid.Text('Left Pane', align='center')])
        self.mid_pane = urwid.ListBox(
            [urwid.Text('Mid Pane', align='center')])
        self.right_pane = urwid.ListBox(
            [urwid.Text('Right Pane', align='center')])
        (rows, cols) = MainView.calculate_window_size()
        boxes = [self.left_pane, self.mid_pane, self.right_pane]
        #TODO: Figure out how to make cell_width change on term resize.
        grid = urwid.GridFlow(
            [urwid.LineBox(urwid.BoxAdapter(b, height=rows-4)) for b in boxes],
            cell_width=int(cols/3)-1, h_sep=0, v_sep=0, align='center')
        super(MainView, self).__init__(
            main_view, optional_base=urwid.Filler(grid))
