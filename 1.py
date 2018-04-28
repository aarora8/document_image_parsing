import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

im = np.array(Image.open('/Users/ashisharora/madcat_sample/CNS_CMN_20070126.0303_002_LDC0523.tif'), dtype=np.uint8)

# Create figure and axes
fig,ax = plt.subplots(1)

# Display the image
ax.imshow(im)

# Create a Rectangle patch
rect1 = patches.Rectangle((1092,269),126,169,linewidth=1,edgecolor='r',facecolor='black')
rect2 = patches.Rectangle((1412,304),104,148,linewidth=1,edgecolor='r',facecolor='black')
rect3 = patches.Rectangle((1536,294),142,155,linewidth=1,edgecolor='r',facecolor='black')
rect4 = patches.Rectangle((1720,308),112,141,linewidth=1,edgecolor='r',facecolor='black')
rect5 = patches.Rectangle((1852,304),128,158,linewidth=1,edgecolor='r',facecolor='black')
rect6 = patches.Rectangle((1996,294),158,220,linewidth=1,edgecolor='r',facecolor='black')
rect7 = patches.Rectangle((2180,302),90,138,linewidth=1,edgecolor='r',facecolor='black')
# Add the patch to the Axes
ax.add_patch(rect1)
ax.add_patch(rect2)
ax.add_patch(rect3)
ax.add_patch(rect4)
ax.add_patch(rect5)
ax.add_patch(rect6)
ax.add_patch(rect7)
plt.show()