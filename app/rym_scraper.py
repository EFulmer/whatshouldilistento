# rym_scraper.py

from collections import namedtuple

import requests

from lxml import html


RYM_BASE = 'http://rateyourmusic.com/artist/'
ROOT_ALBUM_XPATH = '//div[@id="disco_type_s"]'
ARTIST_NAME_XPATH = '//h1[@class="artist_name_hdr"]/text()'

RYMInfo = namedtuple('RYMInfo', ['name', 'best_album'])


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
    # this is a bit too involved to mark with a to-do though
    return requests.get( RYM_BASE + artist_name )


def tree_from_page(artist_page):
    """
    Return a lxml HTML tree for the Response artist_page.
    """
    return html.fromstring(artist_page.text)


def get_album_titles(html_tree):
    """
    Return a list containing the titles of all the artist's 
    studio albums, given an lxml HtmlTree.
    """
    title_xpath = ROOT_ALBUM_XPATH + '//a[@class="album"]/text()'
    titles = html_tree.xpath(title_xpath)
    return titles


def get_album_ratings(html_tree):
    """
    Return a list containing the ratings for each of the artist's 
    studio albums, given an lxml HtmlTree.
    """
    rating_xpath = ROOT_ALBUM_XPATH + '//div[@class="disco_avg_rating"]/text()'
    ratings = html_tree.xpath(rating_xpath)
    return ratings


def get_best_album(album_info):
    """
    Given a list of (title, rating) tuples, return the best-rated 
    album.
    """
    return max(album_info, key=lambda x: x[1])[0]


def best_album(artist):
    """
    Given the name of an artist, returns their best album based on 
    Rate Your Music user ratings.
    """
    rym_name = rymify_name(artist)
    rym_page = get_artist_page(rym_name)
    page_src = tree_from_page(rym_page)
    titles   = get_album_titles(page_src)
    ratings  = get_album_ratings(page_src)
    info     = zip(titles, ratings)
    best     = get_best_album(info)
    return best


def get_artist_name(html_tree):
    """
    Return the artist's name, as displayed on RYM (in other words, 
    their "proper name").

    html_tree -- lxml HTML tree for the artist's RYM page
    """
    return html_tree.xpath(ARTIST_NAME_XPATH)[0]


def get_artist_info(artist):
    """
    Return a new namedtuple of (artist's name, best album from artist), 
    given an artist's name.
    """
    rym_name = rymify_name(artist)
    rym_page = get_artist_page(rym_name)
    page_src = tree_from_page(rym_page)
    name     = get_artist_name(page_src)
    titles   = get_album_titles(page_src)
    ratings  = get_album_ratings(page_src)
    info     = zip(titles, ratings)
    best     = get_best_album(info)
    return RYMInfo(name.encode('utf8'), best.encode('utf8'))

