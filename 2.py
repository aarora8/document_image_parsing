#!/usr/bin/env python3

# local/process_data.py data/local

import argparse
import os
import sys
import xml.dom.minidom as minidom

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np


im = np.array(Image.open('/Users/ashisharora/madcat_sample_1/CNS_CMN_20070126.0303_002_LDC0523.tif'), dtype=np.uint8)
xml_path = os.path.join('/Users/ashisharora/madcat_sample_1' , 'CNS_CMN_20070126.0303_002_LDC0523.gedi.xml')

# Create figure and axes
fig,ax = plt.subplots(1)
doc = minidom.parse(xml_path)

DL_ZONE = doc.getElementsByTagName('DL_ZONE')
previous_id="-1"
start="true"
for node in DL_ZONE:
    id=node.getAttribute('lineID')
    if id=="":
        continue
    if previous_id != id and start=="false":
        print(previous_id, id)
        break
    col=node.getAttribute('col')
    row=node.getAttribute('row')
    width=node.getAttribute('width')
    height=node.getAttribute('height')
    rect1 = patches.Rectangle((col, row), width, height, linewidth=1, edgecolor='w', facecolor='none')
    ax.add_patch(rect1)
    previous_id = id
    start="false"

ax.imshow(im)
plt.show()
