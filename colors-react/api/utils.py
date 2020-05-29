import os
import gzip
import numpy as np
import struct
import urllib
from urllib.parse import urlparse
from os.path import splitext
import json
from urllib import request
from py3pin.Pinterest import Pinterest
# from pyunsplash import PyUnsplash

WIDTH = 128
HEIGHT = 128
DEBUG = True

with open("credentials.json") as f:
    credentials = json.load(f)
    PINTEREST_USER = credentials['username']
    PINTEREST_PASS = credentials['password']


def print_(m):
    if DEBUG is True:
        return
    print(m)


def calculate_new_size(image):
    if image.width >= image.height:
        wpercent = (WIDTH / float(image.width))
        hsize = int((float(image.height) * float(wpercent)))
        new_width, new_height = WIDTH, hsize
    else:
        hpercent = (HEIGHT / float(image.height))
        wsize = int((float(image.width) * float(hpercent)))
        new_width, new_height = wsize, HEIGHT
    return new_width, new_height


def rgb2hex(rgb):
    hex = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    return hex

# return list of aesthetic urls


def get_url(result):
    return result['images']['orig']['url']


def get_ext(url):
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext  # or ext[1:] if you don't want the leading '.'

# return
# {
#     title: ..
#     link: ..
#     url: ..
# }


def prepare_data(query, num_items, skip={}, scope="pins"):
    valid_ext = {".jpg", ".png", ".gif"}
    # UNSPLASH -------------
    # photos = pu.photos(type_='random', count=num_items, query=query)
    # urls = []
    # for photo in photos.entries:
    #     print_(photo)
    #     urls.append(photo.link_download)
    # return urls

    # PINTEREST -----------------
    pinterest = Pinterest(email=PINTEREST_USER, password=PINTEREST_PASS,
                          username=PINTEREST_USER, cred_root='cache')
    results = []
    search_batch = pinterest.search(
        scope=scope, query=query, page_size=num_items)

    while len(search_batch) > 0 and len(results) < num_items:
        for datum in search_batch:
            print_(json.dumps(datum, indent=2))

            if 'is_promoted' in datum and datum['is_promoted'] is True:
                continue
            if 'images' not in datum:
                continue
            url = get_url(datum)
            if url in skip:
                continue
            if get_ext(url) not in valid_ext:
                continue

            results.append({
                # "title":
                "url": url,
                "title": datum["grid_title"],
                "link": datum["link"]
            })
        if len(results) >= num_items:
            break
        search_batch = pinterest.search(
            scope=scope, query=query, page_size=num_items*3)

    # print_(results)

    return results[:num_items]
