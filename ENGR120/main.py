import network
import socket
import json
import math
import time
import sensors.thermistor
from UI.web_page import web_page
import sensors.pir
import sensors.light_sensor
import actuators.hvac
 
sensors.thermistor.setup(1)
sensors.pir.setup(16, 17, 18)
sensors.light_sensor.setup(0)
actuators.hvac.setup(HEATING_PIN, COOLING_PIN) # designate pins when ready
 
# --- Wi-Fi Access Point ---
ssid     = 'RPI_PICO_AP'
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

def parse_param(request_str, key):
    """Return the string value of ?key=VALUE from the request line, or None."""
    marker = key + "="
    idx = request_str.find(marker)
    if idx == -1:
        return None
    start = idx + len(marker)
    end   = request_str.find("&", start)
    if end == -1:
        end = request_str.find(" ", start)
    if end == -1:
        end = len(request_str)
    return request_str[start:end]
 
kill_switch = False
 
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request_bytes = conn.recv(1024)
    request_str   = str(request_bytes)

    if "?kill=1" in request_str:
        kill_switch = True
        print("Kill switch activated")
    elif "?kill=0" in request_str:
        kill_switch = False
        print("Kill switch deactivated")

    if "?lights=on" in request_str:
        sensors.pir.force_lighting(True)
    elif "?lights=off" in request_str:
        sensors.pir.force_lighting(False)

    occ_val   = parse_param(request_str, "occ_temp")
    unocc_val = parse_param(request_str, "unocc_temp")
    if occ_val is not None:
        try:
            actuators.hvac.set_occupied_temp(int(occ_val))
        except ValueError:
            pass
    if unocc_val is not None:
        try:
            actuators.hvac.set_unoccupied_temp(int(unocc_val))
        except ValueError:
            pass

    temp        = sensors.thermistor.read_temp()
    pir_state   = sensors.pir.update()
    is_occupied = pir_state["occupied"]
    lights_on   = pir_state["lighting"]
    brightness  = sensors.light_sensor.read_light_sensor()
    is_bright   = brightness["brightness"]

    if kill_switch:
        actuators.hvac.force_off()
        hvac_state = "kill switch"
    else:
        hvac_state = actuators.hvac.hvac_actuation(temp, is_occupied)
 
    time.sleep(0.1)
 
    if "?status=1" in request_str:
        payload = {
            "temp":           temp,
            "occupied":       is_occupied,
            "lighting":       lights_on,
            "hvac_state":     hvac_state,
            "is_bright":      is_bright,
            "occ_setpoint":   actuators.hvac.OCCUPIED_TEMP,
            "unocc_setpoint": actuators.hvac.UNOCCUPIED_TEMP,
            "kill_active":    kill_switch,
        }
        body = json.dumps(payload)
        conn.send("HTTP/1.1 200 OK\r\n")
        conn.send("Content-Type: application/json\r\n")
        conn.send("Connection: close\r\n\r\n")
        conn.sendall(body)
        conn.close()
        continue  
 
    response = web_page(
        temp           = temp,
        occupied       = is_occupied,
        lighting       = lights_on,
        hvac_state     = hvac_state,
        is_bright      = is_bright,
        kill_active    = kill_switch,
        occ_setpoint   = actuators.hvac.OCCUPIED_TEMP,
        unocc_setpoint = actuators.hvac.UNOCCUPIED_TEMP,
    )
 
    conn.send("HTTP/1.1 200 OK\r\n")
    conn.send("Content-Type: text/html\r\n")
    conn.send("Connection: close\r\n\r\n")
    conn.sendall(response)
    conn.close()
