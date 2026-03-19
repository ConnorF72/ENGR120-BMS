# author Connor Fletcher #
# date 12-03-26 #
# Handles HVAC actuation logic for building management system #

from machine import Pin

# TODO: Ability to alter this from html page #
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


def hvac_actuation(temp, is_occupied):
    global UNOCCUPIED_TEMP, OCCUPIED_TEMP, STATE
    
    if is_occupied:
        if temp < OCCUPIED_TEMP-2:
            heating_led.value(1)
            cooling_led.value(0)
            STATE = "heating"
            
        elif temp > OCCUPIED_TEMP+2:
            cooling_led.value(1)
            heating_led.value(0)
            STATE = "cooling"
            
        elif temp >= OCCUPIED_TEMP-2 and temp <= OCCUPIED_TEMP+2:
            STATE = "off"
            heating_led.value(0)
            cooling_led.value(0)
            
    if not is_occupied:
        
        if temp < UNOCCUPIED_TEMP-2:
            heating_led.value(1)
            cooling_led.value(0)
            STATE = "heating"
            
        elif temp > UNOCCUPIED_TEMP+2:
            cooling_led.value(1)
            heating_led.value(0)
            STATE = "cooling"
            
        elif temp >= UNOCCUPIED_TEMP-2 and temp <= UNOCCUPIED_TEMP+2:
            STATE = "off"
            heating_led.value(0)
            cooling_led.value(0)
                  
    return STATE