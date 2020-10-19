# openMV button controls the LED, while the LCD synchronously displays the screen captured by openMV
# Initial state :LCD synchronously displays the screen captured by openMV, and the external LED is extinguished
# Operation effect: press the button light to go on, press the button light to go off again

# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, pyb, image, lcd
from pyb import Pin, Timer

usb = pyb.USB_VCP()
tim = Timer(4, freq=1000)           # Frequency in Hz
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA2)   # Set frame size to QVGA (320x240)

lcd.init()

sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.
Button = Pin('P6', Pin.IN, Pin.PULL_UP)
Led = tim.channel(3, Timer.PWM, pin=Pin("P9"), pulse_width_percent=0)
i=1
while(True):
    lcd.display(sensor.snapshot())
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
    if Button.value()==0:
        while Button.value()==0:
            pass
        if i:
            Led.pulse_width_percent(10)
            i=0
        else:
            Led.pulse_width_percent(0)
            i=1


