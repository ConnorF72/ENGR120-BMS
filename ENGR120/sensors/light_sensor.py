# author Connor Fletcher
# date 03-07-2026
# sensor logic for light_sensor #

import machine
import time

BRIGHTNESS_THRESHOLD_ON = 40000
BRIGHTNESS_THRESHOLD_OFF = 45000
is_bright = False

light_sensor = None

# sets up light_sensor global variable and configures ADC pin
# param pin ADC pin to assign to
def setup(pin):
    global light_sensor
    light_sensor = machine.ADC(pin)
    print("Light Sensor: setup complete\n")

# reads light sensor data and assigns boolean return value depending on brightness #
def read_light_sensor():
    global is_bright
    raw = light_sensor.read_u16()
    print(raw) #prints resistance to console
    
    if is_bright:
        if raw > BRIGHTNESS_THRESHOLD_OFF:
            is_bright = False
            
    else:
        if raw < BRIGHTNESS_THRESHOLD_ON:
            is_bright = True
    return {
        "brightness": "High" if is_bright else "Low"
        }