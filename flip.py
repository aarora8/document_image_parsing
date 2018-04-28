#!/usr/bin/env python3

import argparse
import os
import sys
import xml.dom.minidom as minidom
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from PIL import Image
import numpy as np
from scipy.misc import toimage

im = np.array(Image.open('/Users/ashisharora/QDS_ARB_20070102.0008_1_LDC0002_00z1.tif'), dtype=np.uint8)
imgray_rev_arr = np.fliplr(im)
imgray_rev = toimage(imgray_rev_arr)
imgplot = plt.imshow(imgray_rev)
plt.show()