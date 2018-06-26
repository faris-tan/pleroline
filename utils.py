"""Random utility functions."""

import urwid


def create_pile_flow(widgets, cell_width, align):
    """Creates a Gridflow-like pile widget with the given widget list.

    Args:
        widgets: list of urwid widgets to display, top to bottom.
        cell_width: int, the size of each cell.
        align: str, horizontal alignment of cells (see: GridFlow align parameter).

    Returns:
        A urwid.Filler-wrapped urwid.Pile widget with Gridflow-like behaviour.
    """
    widgets = [urwid.GridFlow([w], cell_width, 0, 0, align) for w in widgets]
    return urwid.Filler(urwid.Pile(widgets))
