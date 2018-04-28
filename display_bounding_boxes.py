import argparse
import os
import xml.dom.minidom as minidom
from PIL import Image
import numpy as np
from scipy.misc import toimage
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def set_line_image_data(image, line_id, image_file_name):
    base_name = os.path.splitext(os.path.basename(image_file_name))[0]
    line_image_file_name = base_name + line_id + '.tif'
    imgray = image.convert('L')
    imgray_rev_arr = np.fliplr(imgray)
    imgray_rev = toimage(imgray_rev_arr)
    imgray_rev.save(os.path.join(data_path, 'lines', line_image_file_name))


def merge_characters_into_line_image(region_list):
    # get image width and height
    blank_space = 50
    image_width = blank_space
    image_height = -1
    for x in region_list:
        (width, height) = x.size
        image_width += width
        image_height = max(image_height, height)
    image_width += blank_space

    stitched_image = Image.new('RGB', (image_width, image_height), "white")
    width_offset = blank_space
    for x in reversed(region_list):
        height_offset = 0
        stitched_image.paste(im=x, box=(width_offset, height_offset))
        (width, height) = x.size
        width_offset = width_offset + width

    return stitched_image


def get_line_images_from_page_image(image_file_name, madcat_file_path):
    im = Image.open(image_file_name)
    doc = minidom.parse(madcat_file_path)
    zone = doc.getElementsByTagName('zone')
    for node in zone:
        id = node.getAttribute('id')
        region_list = list()
        timage = node.getElementsByTagName('token-image')
        for tnode in timage:
            point = tnode.getElementsByTagName('point')
            col, row = [], []
            max_col, max_row, min_col, min_row = '', '', '', ''
            for pnode in point:
                col.append(int(pnode.getAttribute('x')))
                row.append(int(pnode.getAttribute('y')))
                max_col, max_row = max(col) , max(row)
                min_col, min_row = min(col), min(row)
            box = (min_col, min_row, max_col, max_row)
            rect1 = patches.Rectangle((min_col, min_row), max_col- min_col, max_row-min_row, linewidth=1, edgecolor='r',facecolor='none')
            ax.add_patch(rect1)
            region = im.crop(box)
            region_list.append(region)
    ax.imshow(im)
    plt.show()
    input("Press the <ENTER> key to continue...")

        # ax.imshow(im)
        # plt.show()
        # raw_input("Press the <ENTER> key to continue...")
        #image = merge_characters_into_line_image(region_list)
        #set_line_image_data(image, id, image_file_name)


### main ###
fig,ax = plt.subplots(1)
data_path = '/Users/ashisharora/madcat_ar'

for file in os.listdir(os.path.join(data_path, 'images')):
    if file.endswith(".tif"):
        image_path = os.path.join(data_path, 'images', file)
        gedi_file_path = os.path.join(data_path, 'madcat', file)
        gedi_file_path = gedi_file_path.replace(".tif", ".madcat.xml")
        im = Image.open(image_path)
        # im.show()
        get_line_images_from_page_image(image_path, gedi_file_path)

