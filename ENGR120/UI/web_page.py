# author Connor Fletcher
# date 07-03-2026
# Creates a web_page #
# param temp Takes temperature reading from thermistor after it has been converted to celcius
# param occupied Takes occupancy state as a boolean value
# param lighting Takes lighting state as a boolean value
# return html Returns html string to main.py to be displayed on socket server

def web_page(temp, occupied, lighting, brightness): # add parameters as we need to feed more data to webpage #
    html = f"""<!DOCTYPE html>
  <html>
  <head>
   <meta http-equiv="refresh" content="2">
  </head>
  <body>
  <p>Ambient temperature is {temp} degrees celcius</p>
  <p>Occupancy state: {occupied}</p>
  <p>Lighting state: {lighting}</p>
  <p>Brightness: {brightness}</p>
  </body>
  </html>
"""
    return html