# get_albums.py

import requests

from lxml import html


RYM_BASE = 'http://rateyourmusic.com/artist/'
ROOT_ALBUM_XPATH = '//div[@id="disco_type_s"]'

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
    # in the long term future I'd like to handle artist names more 
    # intelligently, i.e. distinguish between "Kurt Vile" and 
    # "Kurt Vile & The Violators"
    return requests.get( RYM_BASE + rymify_name(artist_name) )


def tree_from_page(artist_page):
    """
    Return a lxml HTML tree for the Response artist_page.
    """
    return html.fromstring(artist_page.text)


def get_albums(html_tree):
    """
    Return each album from the artist, given an lxml HtmlTree.
    """
    # '//div[@id="disco_type_s"]//div[@class="disco_mainline"]'
    # '//div[@id="disco_type_s"]//div[@class="disco_avg_rating"]/text'
    # return html_tree.xpath('//div[@id="disco_type_s"]')
    title_xpath = ROOT_ALBUM_XPATH + '//a[@class="album"]/text()'
    rating_xpath = ROOT_ALBUM_XPATH + '//div[@class="disco_avg_rating"]/text()'
    titles = html_tree.xpath(title_xpath)
    ratings = html_tree.xpath(rating_xpath)
    # return html_tree.xpath('//div[@id="disco_type_s"]//a[@class="album"]/text()')
    return zip(titles, ratings)



def get_best_album(albums):
    """
    """
    # TODO
    # //div[@class="disco_avg_rating"]/text() returns the ratings
    pass
