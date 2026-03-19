# author Connor Fletcher #
# date 07-03-2026 #
# Creates a web_page #
# param temp Takes temperature reading from thermistor after it has been converted to celcius
# param occupied Takes occupancy state as a boolean value
# param lighting Takes lighting state as a boolean value
# return html Returns html string to main.py to be displayed on socket server

def web_page(temp, occupied, lighting, hvac_state): # add parameters as we need to feed more data to webpage #
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="2">
  <title>ENGR 120 BMS</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
 
    body {{
      background-color: #2c2f38;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      font-family: sans-serif;
      gap: 1rem;
    }}
 
    h1 {{
      color: #ccc;
      font-size: 1.2rem;
    }}
 
    .container {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: 1rem;
      width: 700px;
      height: 400px;
    }}
 
    .box {{
      background-color: #3b3f4c;
      border-radius: 6px;
      padding: 1rem;
      color: #ccc;
    }}
  </style>
</head>
<body>
  <h1>ENGR 120 BMS</h1>
  <div class="container">
    <div class="box" id="occupancy">
      <span>Occupancy</span>
      <p>{occupied}</p>
    </div>
    <div class="box" id="lighting">
      <span>Lighting</span>
      <p>{lighting}</p>
    </div>
    <div class="box" id="temperature">
      <span>Temperature (&#176;C)</span>
      <p>{temp}</p>
    </div>
    <div class="box" id="hvac">
      <span>HVAC</span>
      <p>{hvac_state}</p>   
    </div>
    <div class="box" id="controls">Controls</div>
    <div class="box" id="killswitch">Kill Switch</div>
  </div>
</body>
</html>
"""
    return html