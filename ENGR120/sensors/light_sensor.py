# author Connor Fletcher
# date 03-07-2026
# sensor logic for light_sensor #

import machine
import time

light_sensor = None

# sets up light_sensor global variable and configures ADC pin
# param pin ADC pin to assign to
def setup(pin):
    global light_sensor
    light_sensor = machine.ADC(pin)
    print("Light Sensor: setup complete\n")

# reads light sensor data and assigns boolean return value depending on brightness #
def read_light_sensor():
    sensor_out = light_sensor.read_u16()
    print(sensor_out) #prints resistance to console
    if sensor_out < 50000:
        is_bright = "High"
            
    else:
        is_bright = "Low"
    return {
        "brightness": is_bright
        }