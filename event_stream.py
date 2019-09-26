"""Module to generate timeline-like widget streams from the Mastodon API."""
import toot

def fetch_timeline(api, timeline='home', since_id=None):
    if timeline == 'public':
        toots = api.timeline_public(since_id=since_id)
    else:
        toots = api.timeline(timeline, since_id=since_id)
    toots_list = []
    for toot_dict in toots:
        username = toot_dict['account']['acct']
        display_name = toot_dict['account']['display_name']
        contents = toot_dict['content']
        toots_list.append(toot.Toot(username, display_name, contents))
    return toots_list
