#!/usr/bin/env python3

import argparse
import os
import xml.dom.minidom as minidom
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

parser = argparse.ArgumentParser(description="""Creates line images from page image.""")
parser.add_argument('database_path', type=str,
                    help='Path to the downloaded (and extracted) mdacat data')
parser.add_argument('--width_buffer', type=int, default=0,
                    help='width buffer across annotate character')
parser.add_argument('--height_buffer', type=int, default=0,
                    help='height buffer across annotate character')
parser.add_argument('--char_width_buffer', type=int, default=10,
                    help='white space between two characters')
parser.add_argument('--char_height_buffer', type=int, default=20,
                    help='starting location from the top of the line')
args = parser.parse_args()


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


def get_line_images_from_page_image(image_file_name, gedi_file_path):
    im = Image.open(image_file_name)
    doc = minidom.parse(gedi_file_path)

    height_offset_list = list()
    region_list = list()
    first_image_top_loc = -1
    previous_line_id = "-1"
    start = "true"
    DL_ZONE = doc.getElementsByTagName('DL_ZONE')
    for node in DL_ZONE:
        line_id = node.getAttribute('lineID')
        if line_id == "":
            continue
        col = int(node.getAttribute('col'))
        row = int(node.getAttribute('row'))
        if start == "true":
            first_image_top_loc = row
            previous_line_id = line_id
            region_list = list()
            height_offset_list = list()

        if previous_line_id != line_id:
            ax.imshow(im)
            plt.show()
            image = merge_characters_into_line_image(region_list, height_offset_list)
            set_line_image_data(image, previous_line_id, image_file_name)

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
        rect1 = patches.Rectangle((col, row), width, height, linewidth=1, edgecolor='w', facecolor='none')
        ax.add_patch(rect1)
        region_list.append(region)
        start = "false"
    ax.imshow(im)
    plt.show()
    image = merge_characters_into_line_image(region_list, height_offset_list)
    set_line_image_data(image, previous_line_id, image_file_name)


def set_line_image_data(image, line_id, image_file_name):
    base_name = os.path.splitext(os.path.basename(image_file_name))[0]
    line_image_file_name = base_name + '_0' + line_id + '.tif'
    imgray = image.convert('L')
    imgray.save(os.path.join(data_path, 'lines', line_image_file_name))


def remove_corrupt_xml_files(gedi_file_path):
    doc = minidom.parse(gedi_file_path)
    line_id_list = list()
    unique_lineid = list()
    DL_ZONE = doc.getElementsByTagName('DL_ZONE')
    for node in DL_ZONE:
        line_id = node.getAttribute('lineID')
        if line_id == "":
            continue
        line_id_list.append(int(line_id))
        unique_lineid = list(set(line_id_list))
        unique_lineid.sort()

    #check if the lineID is empty
    if len(unique_lineid) == 0:
        return False

    # check if list contain consequtive entries
    if sorted(unique_lineid) != range(min(unique_lineid), max(unique_lineid) + 1):
        return False
    else:
        return True


### main ###
data_path = args.database_path

height_buffer = int(args.height_buffer)
width_buffer = int(args.width_buffer)
char_width_buffer = int(args.char_width_buffer)
char_height_buffer = int(args.char_height_buffer)

# Create figure and axes
fig,ax = plt.subplots(1)

for file in os.listdir(os.path.join(data_path, 'images')):
    if file.endswith(".tif"):
        image_path = os.path.join(data_path, 'images', file)
        gedi_file_path = os.path.join(data_path, 'gedi', file)
        gedi_file_path = gedi_file_path.replace(".tif", ".gedi.xml")

        if remove_corrupt_xml_files(gedi_file_path):
            get_line_images_from_page_image(image_path, gedi_file_path)