import argparse
import os
import xml.dom.minidom as minidom
import numpy as np

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arrow, Circle

from scipy.spatial import ConvexHull
from math import atan2, cos, sin, pi, degrees, sqrt
from collections import namedtuple
from skimage.io import imshow, show, imread, imsave
from skimage.transform import rotate
from skimage import img_as_uint
from skimage import io


a = (4347.43, 285.61)
b = (1819.19, -22.78)
c = (4355.25, 68.57)
d = (1811.37, 194.25)


def is_orthogonal(a, b, c):
    dot_product = (b[0] - a[0]) * (b[0] - c[0]) + (b[1] - a[1]) * (b[1] - c[1])
    return dot_product
    # if -1.0 <= dot_product <=1.0:
    #     return True
    # else:
    #     return False

def is_rectangle(a, b, c, d):
    bool_abc = is_orthogonal(a, b, c)
    bool_adc = is_orthogonal(a, d, c)
    bool_abd = is_orthogonal(a, b, d)
    bool_acd = is_orthogonal(a, c, d)
    bool_acb = is_orthogonal(a, c, b)
    bool_adb = is_orthogonal(a, d, b)

    print(bool_abc)
    print(bool_adc)
    print(bool_abd)
    print(bool_acd)
    print(bool_acb)
    print(bool_adb)


is_rectangle(a, b, c, d)
print('code complete')





