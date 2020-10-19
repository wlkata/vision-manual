# Keystroke control example
# Initial state: external LED extinguish state
# Operation effect: press the button light to go on, release the button light to go off
# This example shows how to control keystrokes in OpenMV Cam
import time
from pyb import Pin, Timer

# Connect a switch to pin 0 that will pull it low when the switch is closed.
# LED will then light up.

tim = Timer(4, freq=1000)
clock = time.clock()                    #Create a clock object to track the FPS
Button = Pin('P6', Pin.IN, Pin.PULL_UP)         #Define Button
Led = tim.channel(3, Timer.PWM, pin=Pin("P9"), pulse_width_percent=0)   #Define LED

while(True):
    if Button.value():   #Determine if the button is pressed
        Led.pulse_width_percent(0) #Did not press the LED state unchanged
    else:
        Led.pulse_width_percent(10) # Press to light the LED
