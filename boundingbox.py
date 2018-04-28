import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

# im = np.array(Image.open('/Users/ashisharora/madcat_sample/CNS_CMN_20070126.0303_002_LDC0523.tif'), dtype=np.uint8)
# fig,ax = plt.subplots(1)
# rect1 = patches.Rectangle((1266,279),128,163,linewidth=1,edgecolor='w',facecolor='none')
# ax.add_patch(rect1)
# plt.show()

data = np.zeros([100,100,3],dtype=np.uint8)
data.fill(255) # or img[:] = 255
img = Image.fromarray(data, 'RGB')
img.show()
##print(id, col, row, width, height)