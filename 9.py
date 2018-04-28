#!/usr/bin/env python3

import argparse
import os
import xml.dom.minidom as minidom
from PIL import Image

parser = argparse.ArgumentParser(description="""Creates text, utt2spk
                                                and images.scp files.""")
parser.add_argument('database_path', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
parser.add_argument('width_buffer', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
parser.add_argument('height_buffer', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
parser.add_argument('char_width_buffer', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
parser.add_argument('char_height_buffer', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
args = parser.parse_args()

data_path = os.path.join(args.database_path, 'madcat_sample')
height_buffer = int(args.height_buffer)
width_buffer = int(args.width_buffer)
char_width_buffer = int(args.char_width_buffer)
char_height_buffer = int(args.char_height_buffer)

def merge_characters_into_line_image(region_list, offset_list):
    # get image width and height
    image_width = 0
    image_height = -1
    for x in region_list:
        (width, height) = x.size
        image_width += width + char_width_buffer
        image_height = max(image_height, height)
    image_height += char_height_buffer*2

    stitched_image = Image.new('RGB', (image_width, image_height), "white")
    width_offset = 0
    for i, x in enumerate(region_list):
        height_offset = offset_list[i] + int(char_height_buffer)
        stitched_image.paste(im=x, box=(width_offset, height_offset))
        (width, height) = x.size
        width_offset = width_offset + width + char_width_buffer

    return stitched_image


def get_line_images_from_page_image():
    height_offset_list = list()
    region_list = list()
    first_image_top_loc = -1
    previous_line_id = "-1"
    start = "true"

    for node in DL_ZONE:
        line_id = node.getAttribute('lineID')
        if line_id == "":
            image = merge_characters_into_line_image(region_list, height_offset_list)
            image.show()
            continue

        col = int(node.getAttribute('col'))
        row = int(node.getAttribute('row'))
        if start == "true":
            first_image_top_loc = row
            previous_line_id = line_id
            region_list = list()
            height_offset_list = list()

        if previous_line_id != line_id:
            image = merge_characters_into_line_image(region_list, height_offset_list)
            image.show()

            first_image_top_loc = row
            previous_line_id = line_id
            region_list = list()
            height_offset_list = list()

        height_offset = row - first_image_top_loc
        height_offset_list.append(height_offset)

        # get character dimensions
        col -= height_buffer
        row -= width_buffer
        width = int(node.getAttribute('width'))
        height = int(node.getAttribute('height'))
        col_down = col + width + height_buffer
        row_right = row + height + width_buffer
        box = (col, row, col_down, row_right)

        # crop characters
        region = im.crop(box)
        region_list.append(region)
        start = "false"

for file in os.listdir(data_path):
    if file.endswith(".tif"):
        image_path = os.path.join(data_path, file)
        gedi_file_path = image_path.replace(".tif", ".gedi.xml")
        im = Image.open(image_path)
        doc = minidom.parse(gedi_file_path)
        DL_ZONE = doc.getElementsByTagName('DL_ZONE')
        get_line_images_from_page_image()