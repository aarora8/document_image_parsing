#!/usr/bin/env python3

# python b_1.py /Users/ashisharora 10 10 20

import argparse
import os
import xml.dom.minidom as minidom

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

parser = argparse.ArgumentParser(description="""Creates text, utt2spk
                                                and images.scp files.""")
parser.add_argument('height_buffer', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
parser.add_argument('width_buffer', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
parser.add_argument('char_buffer', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
args = parser.parse_args()

xml_file_loc = os.path.join('/Users/ashisharora/',
                              'madcat_sample_1')

image_file_loc=os.path.join(xml_file_loc,
                            'CNS_CMN_20070126.0303_002_LDC0523.tif')

height_buffer = int(args.height_buffer)
width_buffer = int(args.width_buffer)
char_buffer = int(args.char_buffer)
im = Image.open(image_file_loc)

# Create figure and axes
fig,ax = plt.subplots(1)
ax.imshow(im)

xml_path = os.path.join(xml_file_loc , 'CNS_CMN_20070126.0303_002_LDC0523.gedi' + '.xml')
doc = minidom.parse(xml_path)

DL_ZONE = doc.getElementsByTagName('DL_ZONE')
previous_id="-1"
start="true"

for node in DL_ZONE:
    id = node.getAttribute('lineID')
    if id == "":
        continue
    if previous_id != id and start == "false":
        print(previous_id, id)
        break

    col = node.getAttribute('col')
    row = node.getAttribute('row')

    col = int(col) - height_buffer
    row = int(row) - width_buffer

    width = node.getAttribute('width')
    height = node.getAttribute('height')

    col_down = int(col) + int(width) + height_buffer
    row_right = int(row) + int(height) + width_buffer
    box = (int(col), int(row), col_down, row_right)

    rect1 = patches.Rectangle((col, row), width, height, linewidth=1, edgecolor='w', facecolor='none')
    ax.add_patch(rect1)
    previous_id = id
    start = "false"

plt.show()
