# author Ben Bligh
# date 07-03-2026

from machine import Pin
import time

OCCUPANCY_TIMER = 5

last_motion_time = 0
is_occupied = False
motion_detected = False

pir_pin = None
occupancy_led_pin = None

def pir_interrupt(pin):
    global motion_detected
    if pin.value() == 1:
        motion_detected = True

def setup(pir_sensor, occupancy_led):
    global pir_pin, occupancy_led_pin
    pir_pin = Pin(pir_sensor, Pin.IN)
    occupancy_led_pin = Pin(occupancy_led, Pin.OUT)
    occupancy_led_pin.value(0)
    pir_pin.irq(trigger=Pin.IRQ_RISING, handler=pir_interrupt)
    print("PIR: setup complete")

def update():
    global motion_detected, last_motion_time, is_occupied
    current_time = time.time()

    if motion_detected:
        last_motion_time = current_time
        motion_detected = False
        if not is_occupied:
            print("PIR: space is occupied")
            is_occupied = True
            occupancy_led_pin.value(1)

    elif is_occupied and (current_time - last_motion_time > OCCUPANCY_TIMER):
        print("PIR: space is no longer occupied")
        is_occupied = False
        occupancy_led_pin.value(0)

    return is_occupied