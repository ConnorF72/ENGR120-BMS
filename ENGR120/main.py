import network
import socket
import math
import time
import sensors.thermistor
from UI.web_page import web_page
import sensors.pir
import sensors.light_sensor

sensors.thermistor.setup(1)
sensors.pir.setup(16, 17, 18)
sensors.light_sensor.setup(0)

ssid = 'RPI_PICO_AP'
password = '12345678'

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while not ap.active():
    time.sleep_ms(100)
print('Connection is successful')
print(ap.ifconfig())
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    #print(request) # print request details for debugging
    
    temp = sensors.thermistor.read_temp()
    pir_state = sensors.pir.update()
    is_occupied = pir_state["occupied"]
    lights_on   = pir_state["lighting"]
    brightness = sensors.light_sensor.read_light_sensor()
    is_bright = brightness["brightness"]
    time.sleep(0.1)
    
    response = web_page(temp, is_occupied, lights_on, brightness)
    
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    
    conn.sendall(response)
    
    conn.close()