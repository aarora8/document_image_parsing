import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
from scipy.misc import toimage

# im = np.array(Image.open('/Users/ashisharora/madcat_sample/CNS_CMN_20070126.0303_002_LDC0523.tif'), dtype=np.uint8)
# fig,ax = plt.subplots(1)
# rect1 = patches.Rectangle((1266,279),128,163,linewidth=1,edgecolor='w',facecolor='none')
# ax.add_patch(rect1)
# plt.show()

img = Image.open('/Users/ashisharora/madcat_sample_4/lines/ASB_ARB_20070119.0006_2_LDC0001z1.tif')
B = np.fliplr(img)
C = toimage(B)
C.show()
