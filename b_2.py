#!/usr/bin/env python3

# python b_1.py /Users/ashisharora
import argparse
import os
import xml.dom.minidom as minidom

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

parser = argparse.ArgumentParser(description="""Creates text, utt2spk
                                                and images.scp files.""")
parser.add_argument('database_path', type=str,
                    help='Path to the downloaded (and extracted) IAM data')
args = parser.parse_args()
xml_file_loc = os.path.join(args.database_path, 'madcat_sample_1')
image_file_loc = os.path.join(xml_file_loc,
                            'CNS_CMN_20070126.0303_002_LDC0523.tif')
im = Image.open(image_file_loc)
fig,ax = plt.subplots(1)
ax.imshow(im)
xml_path = os.path.join(xml_file_loc, 'CNS_CMN_20070126.0303_002_LDC0523.gedi' + '.xml')
doc = minidom.parse(xml_path)


previous_id = ""
start = "true"
DL_ZONE = doc.getElementsByTagName('DL_ZONE')
for node in DL_ZONE:
    id = node.getAttribute('lineID')
    if id == "":
        continue
    if previous_id != id and start == "false":
        break

    col = int(node.getAttribute('col'))
    row = int(node.getAttribute('row'))
    width = int(node.getAttribute('width'))
    height = int(node.getAttribute('height'))
    rect1 = patches.Rectangle((col, row), width, height, linewidth=1, edgecolor='w', facecolor='none')

    ax.add_patch(rect1)
    previous_id = id
    start = "false"

plt.show()
