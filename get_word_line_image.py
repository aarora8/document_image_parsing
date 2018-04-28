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


def get_line_images_from_page_image(image_file_name, madcat_file_path):
    im = Image.open(image_file_name)
    doc = minidom.parse(madcat_file_path)
    zone = doc.getElementsByTagName('zone')
    for node in zone:
        id = node.getAttribute('id')
        # if id == 'z1':
        point = node.getElementsByTagName('point')
        col, row = [], []
        max_col, max_row, min_col, min_row = '', '', '', ''
        for pnode in point:
            col.append(int(pnode.getAttribute('x')))
            row.append(int(pnode.getAttribute('y')))
            max_col, max_row = max(col), max(row)
            min_col, min_row = min(col), min(row)
        rect1 = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, linewidth=1,
                                  edgecolor='r', facecolor='none')
        ax.add_patch(rect1)
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
            rect1 = patches.Rectangle((min_col, min_row), max_col- min_col, max_row-min_row, linewidth=1, edgecolor='r',facecolor='none')
            ax.add_patch(rect1)
    ax.imshow(im)
    plt.show()
    input("Press the <ENTER> key to continue...")


### main ###
fig,ax = plt.subplots(1)
data_path = '/Users/ashisharora/madcat_ar'
line_images_path = '/Users/ashisharora/madcat_ar'

for file in os.listdir(os.path.join(data_path, 'images')):
    if file.endswith(".tif"):
        image_path = os.path.join(data_path, 'images', file)
        gedi_file_path = os.path.join(data_path, 'madcat', file)
        gedi_file_path = gedi_file_path.replace(".tif", ".madcat.xml")
        im = Image.open(image_path)
        get_line_images_from_page_image(image_path, gedi_file_path)

