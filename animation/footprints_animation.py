import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyBboxPatch
from matplotlib import transforms

footprints = [[0, 0, 6, 12, 0],
              [1, 0, 6, 12, math.pi*(1/6)],
              [2, 0, 6, 12, math.pi*(2/6)],
              [3, 0, 6, 12, math.pi*(3/6)],
              [4, 0, 6, 12, math.pi*(4/6)],
              [5, 0, 6, 12, math.pi*(5/6)],
              [6, 0, 6, 12, math.pi*(6/6)],
              [7, 0, 6, 12, math.pi*(7/6)],
              [8, 0, 6, 12, math.pi*(8/6)],
              [9, 0, 6, 12, math.pi*(9/6)]]

centerxs = []
centerys = []

# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)
ax.set_xlim(-10, 15)
ax.set_ylim(-10, 15)

def obb(center_x, center_y, width, length, heading):
  centerxs.append(center_x)
  centerys.append(center_y)

  corners = []

  dx1 = math.cos(heading) * length / 2
  dy1 = math.sin(heading) * length / 2
  dx2 = math.sin(heading) * width / 2
  dy2 = -math.cos(heading) * width / 2

  corners.append([center_x + dx1 + dx2, center_y + dy1 + dy2])
  corners.append([center_x + dx1 - dx2, center_y + dy1 - dy2])
  corners.append([center_x - dx1 - dx2, center_y - dy1 - dy2])
  corners.append([center_x - dx1 + dx2, center_y - dy1 + dy2])

  min_x = float("inf")
  max_x = -float("inf")
  min_y = float("inf")
  max_y = -float("inf")
  for corner in corners:
    max_x = max(corner[0], max_x)
    min_x = min(corner[0], min_x)
    max_y = max(corner[1], max_y)
    min_y = min(corner[1], min_y)
  corners.append(corners[0])
  corners = np.array(corners)

  scat = ax.scatter(centerxs, centerys, s=100)

  obbx = ax.plot(corners[:,0], corners[:,1], '-')

  round_obb = FancyBboxPatch((center_x-length/2, center_y-width/2),
                             length, width,
                             boxstyle="round,pad=1",
                             fill=False,
                             #fc=(1., .8, 1.),
                             ec=(1., 0.5, 1.))

  t2 = transforms.Affine2D().rotate_around(center_x, center_y, heading) + ax.transData
  round_obb.set_transform(t2)

  ax.add_patch(round_obb)

  arrow_length = length * 0.8

  ax.arrow(center_x, center_y,
           arrow_length * math.cos(heading), arrow_length * math.sin(heading),
           head_width=0.5, head_length=1)

def update(frame_number):
    # Get an index which we can use to re-spawn the oldest raindrop.
    current_index = frame_number % 10
    footprint = footprints[current_index]

    ax.clear()
    ax.axis('equal')
    ax.set_xlim(-10, 15)
    ax.set_ylim(-10, 15)

    obb(footprint[0], footprint[1], footprint[2], footprint[3], footprint[4])


# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=1000)
plt.show()
