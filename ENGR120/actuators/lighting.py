# author Connor Fletcher
# date 07-03-2026
from machine import Pin
import time
 
LIGHTING_TIMER = 7
 
lighting_led_pin = None
lighting_active = False
occupancy_end_time = 0
force_state = None
 
 
def setup(lighting_led):
    global lighting_led_pin
    lighting_led_pin = Pin(lighting_led, Pin.OUT)
    lighting_led_pin.value(0)
    print("Lighting: setup complete")
 
 
# Overrides automatic lighting logic with a fixed state #
# param state  True = force on, False = force off, None = return to auto #
def force_lighting(state):
    global force_state
    force_state = state
 
 
# Clears any manual override and returns lighting to automatic control #
def clear_force():
    global force_state
    force_state = None
# param is_occupied  Occupancy boolean from PIR sensor #
# param is_bright    Brightness string ("High" / "Low") from light sensor #
# return             Current lighting state boolean #
def update(is_occupied, is_bright):
    global lighting_active, occupancy_end_time
    current_time = time.time()
 
    if force_state is not None:
        lighting_led_pin.value(1 if force_state else 0)
        return bool(force_state)
 
    if is_occupied and is_bright == "Low":
        occupancy_end_time = 0
        lighting_active = True
 
    elif is_bright == "High" and lighting_active:
        print("Lighting: suppressed by brightness")
        lighting_active = False
        occupancy_end_time = 0
 
    elif not is_occupied and lighting_active:
        if occupancy_end_time == 0:
            occupancy_end_time = current_time
        if current_time - occupancy_end_time > LIGHTING_TIMER:
            print("Lighting: timer expired")
            lighting_active = False
            occupancy_end_time = 0
 
    lighting_led_pin.value(1 if lighting_active else 0)
    return lighting_active