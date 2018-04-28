#!/usr/bin/env python3

# python b_1.py /Users/ashisharora
import argparse
import os
import xml.dom.minidom as minidom

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

parser = argparse.ArgumentParser(description="""Creates line images from page image.""")
parser.add_argument('--width_buffer', type=int, default=10,
                    help='width buffer across annotate character')
parser.add_argument('--height_buffer', type=int, default=10,
                    help='height buffer across annotate character')
parser.add_argument('--char_width_buffer', type=int, default=50,
                    help='white space between two characters')
parser.add_argument('--char_height_buffer', type=int, default=20,
                    help='starting location from the top of the line')
args = parser.parse_args()

### main ###
data_path = '/Users/ashisharora/'
height_buffer = int(args.height_buffer)
width_buffer = int(args.width_buffer)
char_width_buffer = int(args.char_width_buffer)
char_height_buffer = int(args.char_height_buffer)

xml_file_loc = os.path.join(data_path, 'madcat_sample_2')
image_file_loc = os.path.join(xml_file_loc,
                            'AAW_ARB_20061111.0058-S1_1_LDC0367.tif')
im = Image.open(image_file_loc)
fig,ax = plt.subplots(1)
ax.imshow(im)
xml_path = os.path.join(xml_file_loc, 'AAW_ARB_20061111.0058-S1_1_LDC0367.madcat' + '.xml')
doc = minidom.parse(xml_path)

previous_id = ""
start = "true"
zone = doc.getElementsByTagName('zone')
region_list = list()
for node in zone:
    id = node.getAttribute('id')
    print(id)
    if id != 'z2':
        continue
    region_list = list()
    timage = node.getElementsByTagName('token-image')
    for tnode in timage:
        tid = tnode.getAttribute('id')
        print(tid)
        point = tnode.getElementsByTagName('point')
        col, row = [], []
        max_col, max_row, min_col, min_row = '', '', '', ''
        width, height = '', ''
        for pnode in point:
            col.append(int(pnode.getAttribute('x')))
            row.append(int(pnode.getAttribute('y')))
            max_col, max_row = max(col), max(row)
            min_col, min_row = min(col), min(row)
            height = max_col - min_col
            width = max_row - min_row
        box = (min_col, min_row, max_col, max_row)
        region = im.crop(box)
        region_list.append(region)
        rect1 = patches.Rectangle((min_col, min_row), height, width, linewidth=1, edgecolor='w', facecolor='none')
        ax.add_patch(rect1)
    break

ax.imshow(im)
plt.show()