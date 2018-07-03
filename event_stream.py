"""Module to generate timeline-like widget streams from the Mastodon API."""
import urwid

def _wrap_toot_in_widgets(toot_dict):
    username = urwid.Text(toot_dict['account']['acct'])
    display_name = urwid.Text(toot_dict['account']['display_name'])
    contents = urwid.Text(toot_dict['content'])
    box = urwid.LineBox(
        urwid.Pile([
            urwid.Columns([display_name, username]),
            contents]))
    return box

def fetch_timeline(api, timeline='home', since_id=None):
    if timeline == 'public':
        toots = api.timeline_public(since_id=since_id)
    else:
        toots = api.timeline(timeline, since_id=since_id)
    return [_wrap_toot_in_widgets(t) for t in toots]
