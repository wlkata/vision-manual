# LCD synchronizes display of images captured by openMV
# Initial state :LCD synchronously displays the screen captured by openMV, and the external LED is extinguished
# Running effect :LCD synchronously displays the screen captured by openMV
# Welcome to the OpenMV IDE!Click the green Run arrow button below to run the script

import sensor, image, time, ustruct, pyb, image, lcd
from pyb import USB_VCP

usb = USB_VCP()

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

lcd.init()

while(True):
    lcd.display(sensor.snapshot())
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
