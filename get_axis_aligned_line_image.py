#!/usr/bin/env python3

import sys
import argparse
import os
import numpy as np
from math import atan2, cos, sin, pi, degrees, sqrt
from collections import namedtuple

from scipy.spatial import ConvexHull
from PIL import Image
from scipy.misc import toimage
import logging
import csv

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import unicodedata


def set_line_image_data(image, line_id, image_fh, transcription):
    """ Given an image, saves a flipped line image. It also stores
        line image and transcription mapping.
    """

    image_path = os.path.abspath(line_id)
    image.save(image_path)
    image_fh.write(image_path + ' ' + transcription + '\n')


def get_line_images_from_page_image(image_file_name, csv_path, image_fh):
    im = Image.open(image_file_name)
    # im.show()
    with open(csv_path, 'r', encoding='utf-8') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            line_id = row[1]
            transcription = row[11]
            new_transcription = list()
            for word in transcription:
                word = unicodedata.normalize('NFKC', word)
                new_transcription.append(word)
            new_transcription = " ".join(new_transcription)
            x = [int(row[2]), int(row[4]), int(row[6]), int(row[8])]
            y = [int(row[3]), int(row[5]), int(row[7]), int(row[9])]
            min_x, min_y = min(x), min(y)
            max_x, max_y = max(x), max(y)
            box = (min_x, min_y, max_x, max_y)
            region_initial = im.crop(box)
            set_line_image_data(region_initial, line_id, image_fh, new_transcription)


### main ###
fig,ax = plt.subplots(1)
data_path = '/Users/ashisharora/madcat_ar'
csv_path = os.path.abspath("hindi_phone_books_0001.csv")
image_path = os.path.abspath("hindi_phone_books_0001.jpg")
image_file = os.path.abspath('images.txt')
image_fh = open(image_file, 'w', encoding='utf-8')
get_line_images_from_page_image(image_path, csv_path, image_fh)
