"""Module with style & color settings for the Pleroline program."""
import urwid

BASE_ATTRS = [
    #('h&f_colors', urwid.AttrSpec('black', '#a6a', 256)),
    ('popup_colors', 'black', 'light magenta')
]

ATTRS = {
    'head/foot': urwid.AttrSpec('black', '#a8a', 256),
    'button': urwid.AttrSpec('black', '#a8a', 256),
    'error': urwid.AttrSpec('black', '#f06', 256)
}
