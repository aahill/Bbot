#!/usr/bin/env python
import matplotlib.pyplot as plt
#plt.rcdefaults()
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

arena_height = 287.5
arena_width = 174

brick_height_laying = 15
brick_width_laying = 40

brick_height_standing = 20
brick_width_standing = 40

#draw the arena exterior
arena_verts = [
	(0,0), #left, bottom
	(0,arena_height), #left, top
	(arena_width,arena_height), #right, top
	(arena_width,0), # right, bottom
	(0,0) #ignored
]
#codes for path movement for a rectangle
rect_codes = [Path.MOVETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.CLOSEPOLY,
         ]
#path for arena outline
arena_path = Path(arena_verts, rect_codes)

left_brick_verts = [
	(28,84),#left, bottom (starting coordinate)
	(28,84+brick_height_laying),#left, top
	(28+brick_width_laying,84+brick_height_laying), #right, top
	(28+brick_width_laying,84),# right, bottom
	(28,84)
]
left_brick_path = Path(left_brick_verts, rect_codes)




fig = plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)
patch = patches.PathPatch(arena_path, facecolor='none', lw=1)
patch2 = patches.PathPatch(left_brick_path, facecolor='none', lw=1)

ax.add_patch(patch)
ax.add_patch(patch2)
#buffer for centering figure
buf = 20
ax.set_xlim(-buf,arena_width+buf)
ax.set_ylim(-buf,arena_height+buf)
#set axis' tick marks
#ax.xaxis.set_ticks(np.arange(0, arena_width, 20))
#ax.yaxis.set_ticks(np.arange(0, arena_height, 20))
ax.xaxis.set_major_locator(MultipleLocator(20.0))
ax.yaxis.set_major_locator(MultipleLocator(20.0))

#stop axis' from scaling
ax.set_autoscale_on(False)
plt.show()