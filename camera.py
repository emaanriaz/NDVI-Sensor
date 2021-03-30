import math
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from picamera import PiCamera
from time import sleep
from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys
import numpy as np
import cv2
import picamera
import picamera.array

def label(image, text):
    # Labels image
    return cv2.putText(image, text, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)


def contrast_stretch(im):
    # Performs a simple contrast stretch of the given image, from 5-100%.
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 100)
    out_min = 0.0
    out_max = 255.0
    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min
    return out

def run():
    # open camera and take photo
    camera = PiCamera()
    camera.resolution = (1867,1400)
    camera.framerate = 15
    camera.rotation = 180
    camera.start_preview()
    sleep(3)
    camera.capture('/home/pi/Desktop/capture.jpg')
    camera.stop_preview()
    filename = 'capture.jpg'
    image = Image.open(filename)

    # split image
    b, g, r, = cv2.split(image)

    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom == 0] = 0.00001 # Make sure we don't divide by zero
    
    # apply ndvi formula r-b/r+b
    ndvi = (r.astype(float) - b) / bottom
    ndvi = contrast_stretch(ndvi)
    ndvi = ndvi.astype(np.uint8)
        
    # labelling
    label(image, 'original')
    label(ndvi, 'NDVI')
            
    # Display
    cv2.imshow('NDVI Image', ndvi)
    cv2.imshow('Original Image', image)
    

    # cleanup
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run()
