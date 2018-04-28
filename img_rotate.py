import argparse
import os
import xml.dom.minidom as minidom
from PIL import Image
import numpy as np
from scipy.misc import toimage
import math
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches



### main ###
fig,ax = plt.subplots(1)
data_path = '/Users/ashisharora/madcat_ar'
rot_in_rad = -0.105860162158

for file in os.listdir(os.path.join(data_path, 'images')):
    if file.endswith(".tif"):
        image_path = os.path.join(data_path, 'images', file)
        im = Image.open(image_path)
        img2 = im.rotate(math.degrees(rot_in_rad))
        rect1 = patches.Rectangle((2008, 3969), 2448, 292, linewidth=1,
                                  edgecolor='r', facecolor='none')
        ax.add_patch(rect1)
        ax.imshow(img2)
        plt.show()
        input("Press the <ENTER> key to continue...")
# 972840
# 714603.463444
# (3315.6752542008444, 4039.588225645718)
# set([(4548.701694947961, 4055.292618010251), (2082.6488134537276, 4023.883833281185), (2113.4814013334094, 4314.052743659968), (4517.86910706828, 3765.1237076314687)])
# (0.9944020436970461, -0.10566255482022922)
# -0.105860162158

p = 2550
q = 3300
rot_in_rad = 0.105860162158
y_1 = 4023
y_2 = 4314
y_3 = 3765
y_4 = 4055

x_1 = 2082
x_2 = 2113
x_3 = 4517
x_4 = 4548

x_dash_1 = (x_1-p)*math.cos(rot_in_rad) - (y_1-q)*math.sin(rot_in_rad) + p
x_dash_2 = (x_2-p)*math.cos(rot_in_rad) - (y_2-q)*math.sin(rot_in_rad) + p
x_dash_3 = (x_3-p)*math.cos(rot_in_rad) - (y_3-q)*math.sin(rot_in_rad) + p
x_dash_4 = (x_4-p)*math.cos(rot_in_rad) - (y_4-q)*math.sin(rot_in_rad) + p

y_dash_1 = (y_1-q)*math.cos(rot_in_rad) + (x_1-p)*math.sin(rot_in_rad) + q
y_dash_2 = (y_2-q)*math.cos(rot_in_rad) + (x_2-p)*math.sin(rot_in_rad) + q
y_dash_3 = (y_3-q)*math.cos(rot_in_rad) + (x_3-p)*math.sin(rot_in_rad) + q
y_dash_4 = (y_4-q)*math.cos(rot_in_rad) + (x_4-p)*math.sin(rot_in_rad) + q


print(x_dash_1)
print(x_dash_2)
print(x_dash_3)
print(x_dash_4)


print(y_dash_1)
print(y_dash_2)
print(y_dash_3)
print(y_dash_4)
