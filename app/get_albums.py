# get_albums.py

import requests

from lxml import html


RYM_BASE = 'http://rateyourmusic.com/artist/'

def rymify_name(name):
    """
    Convert name to a lowercase string, with spaces replaced by 
    underscores.
    """
    # TODO handle accented letters
    return name.replace(' ', '_').lower()


def get_artist_page(artist_name):
    """
    Return a requests.models.Response representing RYM's page for 
    artist_name.
    """
    return requests.get( RYM_BASE + rymify_name(artist_name) )


def tree_from_page(artist_page):
    """
    Return a lxml HTML tree for the Response artist_page.
    """
    return html.fromstring(artist_page.text)

# //div[@class="disco_release"] -- this returns a list of 
# lxml.HtmlElements, for parsing further.


def get_albums(html_tree):
    """
    Return each album from the artist, given an lxml HtmlTree.
    """
    return html_tree.xpath('//div[@class="disco_release"]')


def get_best_album(albums):
    """
    """
    # TODO
    # //div[@class="disco_avg_rating"]/text() returns the ratings
    pass
