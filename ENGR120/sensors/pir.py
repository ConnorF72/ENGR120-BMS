# author Connor Fletcher
# date 07-03-2026
# Detects motion using infrared sensor
from machine import Pin
import time

OCCUPANCY_TIMER = 5
LIGHTING_TIMER = 10 

last_motion_time = 0
occupancy_end_time = 0
is_occupied = False
motion_detected = False
lighting_active = False

pir_pin = None
occupancy_led_pin = None
lighting_led_pin = None

# interrupt handler runs when motion is detected and updates motion_detected
def pir_interrupt(pin):
    global motion_detected
    if pin.value() == 1:
        motion_detected = True

# sets up pins for circuit and defines the interrupt process
def setup(pir_sensor, occupancy_led, lighting_led):
    global pir_pin, occupancy_led_pin, lighting_led_pin

    pir_pin = Pin(pir_sensor, Pin.IN)
    occupancy_led_pin = Pin(occupancy_led, Pin.OUT)
    lighting_led_pin = Pin(lighting_led, Pin.OUT)

    occupancy_led_pin.value(0)
    lighting_led_pin.value(0)

    pir_pin.irq(trigger=(Pin.IRQ_RISING), handler=pir_interrupt)
    print("PIR: setup complete")


def update():
    global motion_detected, last_motion_time, occupancy_end_time
    global is_occupied, lighting_active

    current_time = time.time()

    if motion_detected:
        last_motion_time = current_time
        motion_detected = False

        if lighting_active:
            lighting_active = False
            occupancy_end_time = 0

        if not is_occupied:
            print("PIR: space is occupied")
            is_occupied = True
            occupancy_led_pin.value(0) #change back to 1 - is 0 for testing
            lighting_led_pin.value(1) #change back to 1 - is 0 for testing

    if is_occupied and (current_time - last_motion_time > OCCUPANCY_TIMER):
        print("PIR: space is no longer occupied")
        is_occupied = False
        occupancy_led_pin.value(0)
        lighting_active = True
        occupancy_end_time = current_time

    if lighting_active:
        lighting_led_pin.value(1)
        if current_time - occupancy_end_time > LIGHTING_TIMER:
            print("PIR: lighting timer expired")
            lighting_active = False
            lighting_led_pin.value(0)
            occupancy_end_time = 0

    return {
        "occupied": is_occupied,
        "lighting": lighting_active or lighting_led_pin.value() == 1
    }