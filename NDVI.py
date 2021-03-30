import time
import picamera

##Start a preview for 10 seconds with the default settings from
##https://picamera.readthedocs.io/en/release-1.10/quickstart.html

camera = picamera.PiCamera()
try:
    camera.start_preview()
    time.sleep(10)
    camera.stop_preview()
finally:
    camera.close()
