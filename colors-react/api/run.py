# get color palette from data
# Example usage: python run.py --search-term goth
# Results: color palettes from goth pins from pinterest

import os
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from sklearn.cluster import MiniBatchKMeans
import random
import functools
from math import ceil

# from kMeans import *
# from nltk.cluster import KMeansClusterer, euclidean_distance
# NUM_CLUSTERS = <choose a value>
# data = <sparse matrix that you would normally give to scikit>.toarray()

# kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
# assigned_clusters = kclusterer.cluster(data, assign_clusters=True)
from utils import *
# from my_args import args

# avoid getting different color palettes
np.random.seed(0)

CLUSTERS = 10
NUM_COLORS = 6
NUM_ITEMS = 3

QUERY_APPEND = ["aesthetic", "style", "graphic design",
                "illustration", "art",  "wallpaper",
                "photography", "fashion", "instagram", "tumblr", "weheartit",
                "background", "korean"]


# def euclidean(p, q):
#     n_dim = len(p.coordinates)
#     return math.sqrt(sum([
#         (p.coordinates[i] - q.coordinates[i]) ** 2 for i in range(n_dim)
#     ]))


def run(query, cache):
    if not query:
        query = "aesthetic"

    if random.random() > 0.1:
        query += " " + random.choice(QUERY_APPEND)
    print_(query)
    # get images
    images = prepare_data(query, NUM_ITEMS, skip=cache)
    # get random img
    # images = [random.choice(images)]
    imgToColors = {}
    error = ""

    # For each image, get color palette
    for obj in images:
        url = obj["url"]
        # TEST: Reshape fails on the following URL
        # url = 'https://i.pinimg.com/originals/b2/3a/91/b23a91d69ede2d066cb76d66b97f0be9.png'
        response = requests.get(url)
        res_bytes = BytesIO(response.content)
        image = Image.open(res_bytes).convert('RGB')
        # image = image
        print_("Loaded {f} image. Dimensions: ({d})".format(
            f=image.format, d=image.size))
        # Resize image to speed up performance
        new_width, new_height = calculate_new_size(image)
        # print_("New size: {f}, {d}".format(
        #     f=new_width, d=new_height))
        image = image.resize((new_width, new_height), Image.ANTIALIAS)
        # Turn image into np array
        img_array = np.array(image)
        # m, n, _ = img_array.shape
        # img_vector = img_array.reshape( (img_array.shape[0] * img_array.shape[1], 3))
        try:
            # points = get_points(image)
            img_vector = img_array.reshape(-1, 3)
        except ValueError:
            print_("Couldn't reshape")
            continue
        # Fit to KMeans model
        # kclusterer = KMeansClusterer(
        #     CLUSTERS, distance=euclidean_distance, repeats=25, avoid_empty_clusters=True)
        # clusters = kclusterer.cluster(img_vector, assign_clusters=True)
        # clusters = KMeans(n_clusters=CLUSTERS).fit(points)
        # rgbs = [map(int, c.center.coordinates) for c in clusters]
        model = MiniBatchKMeans(CLUSTERS)
        model.fit(img_vector)
        centers = model.cluster_centers_
        cmp = functools.cmp_to_key(color_distance)
        centers = sorted(centers, key=cmp)
        centers = takespread(centers, NUM_COLORS)
        # '''d = {} distance between two colors(3)'''

        # Get colors
        hex_colors = [
            rgb2hex(center) for center in centers
        ]
        # print_("Got colors: {f}".format(
        #     f=hex_colors))
        imgToColors[url] = {
            "colors": hex_colors,
            "title": obj["title"],
            "link": obj["link"]
        }
        break
    # print_("wtf")
    if not imgToColors:
        error = "No results :("
    return imgToColors, error


# if __name__ == '__main__':
#     main()

def color_distance(rgb1, rgb2):
    rm = 0.5*(rgb1[0]+rgb2[0])
    d = sum((2+rm, 4, 3-rm)*(rgb1-rgb2)**2)**0.5
    return d


def takespread(sequence, num):
    length = float(len(sequence))
    results = []
    for i in range(num):
        results.append(sequence[int(ceil(i * length / num))])
    return results
