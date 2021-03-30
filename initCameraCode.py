import math
from PIL import Image

import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from picamera import PiCamera
from time import sleep
from mpl_toolkits.axes_grid1 import make_axes_locatable

camera = PiCamera()


camera.resolution = (1867,1400)
camera.framerate = 15
camera.rotation = 180

camera.start_preview()

sleep(5)
camera.capture('/home/pi/Desktop/capture.jpg')
camera.stop_preview()

filename = 'capture.jpg'

image = Image.open(filename)
IMAGE = numpy.array(image)
#NIR = numpy.array(image)

#SPLITTING INTO BANDS

#RED, GREEN, BLUE = image.split()

#NIR
NIR = Image.open(filename)
NIR = numpy.array(NIR)
#NIR[:,:,1]*=0
#NIR[:,:,2]*=0
NIR = NIR[:,:,0]

#GREEN
GREEN = Image.open(filename)
GREEN = numpy.array(GREEN)
#GREEN[:,:,0]*=0
#GREEN[:,:,2]*=0
GREEN = GREEN[:,:,1]

#BLUE
BLUE = Image.open(filename)
BLUE = numpy.array(BLUE)
#BLUE[:,:,0]*=0
#BLUE[:,:,1]*=0
BLUE = BLUE[:,:,2]

#NDVI CALCULATION
bottom = (BLUE - GREEN) ** 2

bottom[bottom == 0] = 1  # remove 0 from nd.array

VIS = ((BLUE + GREEN) ** 2 )/ bottom


NDVI = (NIR - VIS) / (NIR + VIS)

plt.imshow(NDVI)
plt.show()



data = numpy.arange(1, -1, -0.01).reshape(20, 10)

fig, ax = plt.subplots()
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.05)

im = ax.imshow(NDVI, cmap='gnuplot2')

fig.colorbar(im, cax=cax, orientation='vertical')
plt.show()

#plot_compare = numpy.concatenate((IMAGE, NDVI), axis=1)

#plt.imshow(plot_compare)
