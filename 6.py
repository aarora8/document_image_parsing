#!/usr/bin/env python3

import argparse
import os
import xml.dom.minidom as minidom

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

parser = argparse.ArgumentParser(description="""Creates text, utt2spk
                                                and images.scp files.""")
parser.add_argument('database_path', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
parser.add_argument('height_buffer', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
parser.add_argument('width_buffer', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
parser.add_argument('char_buffer', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
args = parser.parse_args()

xml_file_loc = os.path.join(args.database_path,
                              'madcat_sample')

image_file_loc=os.path.join(xml_file_loc,
                            'CNS_CMN_20070126.0303_002_LDC0523.tif')

height_buffer = int(args.height_buffer)
width_buffer = int(args.width_buffer)
char_buffer = int(args.char_buffer)
im = Image.open(image_file_loc)
print("Processing data...")
xml_path = os.path.join(xml_file_loc, 'CNS_CMN_20070126.0303_002_LDC0523.gedi' + '.xml')
doc = minidom.parse(xml_path)


DL_ZONE = doc.getElementsByTagName('DL_ZONE')
previous_id = "-1"
start = "true"
region_list = list()
offset_list = list()
first_image_top_loc = -1
for node in DL_ZONE:
    id = node.getAttribute('lineID')
    if id == "":
        continue
    if start == "true":
        previous_id = id

    if previous_id != id:
        print(previous_id, id)
        break

    col = int(node.getAttribute('col'))
    row = int(node.getAttribute('row'))

    if start == "true":
        first_image_top_loc = row

    offset = row - first_image_top_loc
    offset_list.append(offset)

    col -= height_buffer
    row -= width_buffer

    width = int(node.getAttribute('width'))
    height = int(node.getAttribute('height'))

    col_down = col + width + height_buffer
    row_right = row + height + width_buffer
    box = (col, row, col_down, row_right)

    region = im.crop(box)
    region_list.append(region)
    start = "false"

result_width = 0
result_height = -1
for x in region_list:
    (width, height) = x.size
    result_width += width + char_buffer
    result_height = max(result_height, height)

result = Image.new('RGB', (result_width, result_height), "white")

box_width = 0
height_offset = 0
for i, x in enumerate(region_list):
    height_offset = offset_list[i]
    print height_offset
    result.paste(im=x, box=(box_width, height_offset))
    (width, height) = x.size
    box_width = box_width + width + char_buffer

result.show()
