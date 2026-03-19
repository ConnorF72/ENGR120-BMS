# author Brian Stothers Dawson #
# date 07-03-2026 #
# defines a pin for thermistor circuit, reads resistance, and uses Beta-parameter equation to express value as celcius #
import math
import machine

temp_sensor = None

# establishes ADC pin for thermisor data sensing, taking pin defined in main.py
def setup(pin):
    global temp_sensor
    temp_sensor = machine.ADC(pin)
    print("Thermistor: Setup Complete")

# read thermistor data and convert to degrees celcius
def read_temp():
    temp_sensor_val = temp_sensor.read_u16()
    
    if temp_sensor_val >= 65535: #handle /0
        return None
    temp_val = round(((((1/(1/298+(1/3960)*math.log((65535/(temp_sensor_val)-1)))) - 273)*1)),1)
    # reference temp is 298K (25C)
    # adjust 1/298 accordingly
    
    return temp_val