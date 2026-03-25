# author Connor Fletcher #
# date 12-03-26 #
# Handles HVAC actuation logic for building management system #
 
from machine import Pin
 
UNOCCUPIED_TEMP = 15
OCCUPIED_TEMP = 25
heating_led = None
cooling_led = None
STATE = None
 
# Sets up pins and global variables and prints setup confirmation to terminal #
# param heating_pin GPIO OUT pin for symbolic heating actuation #
# param cooling_pin GPIO OUT pin for symbolic cooling actuation #
def setup(heating_pin, cooling_pin):
    global heating_led, cooling_led
 
    heating_led = Pin(heating_pin, Pin.OUT)
    cooling_led = Pin(cooling_pin, Pin.OUT)
    heating_led.value(0)
    cooling_led.value(0)
 
    print("HVAC Systems: Setup Complete")
 
 
# Updates the occupied temperature setpoint #
# param temp  New occupied setpoint in Celsius #
def set_occupied_temp(temp):
    global OCCUPIED_TEMP
    OCCUPIED_TEMP = temp
    print("HVAC: Occupied setpoint updated to {}C".format(temp))
 
 
# Updates the unoccupied temperature setpoint #
# param temp  New unoccupied setpoint in Celsius #
def set_unoccupied_temp(temp):
    global UNOCCUPIED_TEMP
    UNOCCUPIED_TEMP = temp
    print("HVAC: Unoccupied setpoint updated to {}C".format(temp))
 
 
# Forces both HVAC outputs off (used by kill switch) #
def force_off():
    global STATE
    heating_led.value(0)
    cooling_led.value(0)
    STATE = "kill switch"
    print("HVAC: Forced off by kill switch")
 
 
# Determines and applies HVAC state based on temperature and occupancy #
# param temp          Current temperature in Celsius #
# param is_occupied   Occupancy boolean from PIR sensor #
# return STATE        Current HVAC state string #
def hvac_actuation(temp, is_occupied):
    global UNOCCUPIED_TEMP, OCCUPIED_TEMP, STATE
    
    if temp is None or not isinstance(temp, (int, float)):
        heating_led.value(0)
        cooling_led.value(0)
        STATE = "off"
        return STATE
 
    setpoint = OCCUPIED_TEMP if is_occupied else UNOCCUPIED_TEMP
 
    if temp < setpoint - 2:
        heating_led.value(1)
        cooling_led.value(0)
        STATE = "heating"
 
    elif temp > setpoint + 2:
        cooling_led.value(1)
        heating_led.value(0)
        STATE = "cooling"
 
    else:
        heating_led.value(0)
        cooling_led.value(0)
        STATE = "off"
 
    return STATE