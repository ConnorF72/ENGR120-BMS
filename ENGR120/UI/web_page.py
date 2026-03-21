# author Connor Fletcher #
# date 07-03-2026 #
# Creates the BMS web page with bidirectional controls #
# Status cards update via JS fetch every 3s — control forms are never refreshed #
#
# param temp           Temperature in Celsius
# param occupied       Occupancy boolean
# param lighting       Lighting state boolean
# param hvac_state     Current HVAC state string
# param is_bright      Light sensor brightness string ("High" / "Low")
# param kill_active    Whether kill switch is currently engaged
# param occ_setpoint   Current occupied temperature target
# param unocc_setpoint Current unoccupied temperature target
# return html          HTML string for socket server response
 
def web_page(temp, occupied, lighting, hvac_state,
             is_bright="--", kill_active=False,
             occ_setpoint=25, unocc_setpoint=15):
 
    occ_label        = "Occupied"    if occupied    else "Unoccupied"
    lights_label     = "On"          if lighting    else "Off"
    kill_label       = "ACTIVE"      if kill_active else "Inactive"
    kill_btn_label   = "Deactivate"  if kill_active else "Activate"
    kill_btn_href    = "/?kill=0"    if kill_active else "/?kill=1"
    lights_btn_label = "Turn Off"    if lighting    else "Turn On"
    lights_btn_href  = "/?lights=off" if lighting   else "/?lights=on"
    kill_color       = "#e05555"     if kill_active else "#4caf78"
 
    hvac_icon = {
        "heating":     "&#9651;",
        "cooling":     "&#9661;",
        "off":         "&#9711;",
        "kill switch": "&#9940;",
    }.get(hvac_state, "&#9711;")
 
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ENGR 120 BMS</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;600&display=swap');
 
    :root {{
      --bg:      #1a1d27;
      --surface: #23273a;
      --border:  #2e3450;
      --accent:  #4fa3e0;
      --ok:      #4caf78;
      --danger:  #e05555;
      --text:    #c8d0e7;
      --muted:   #5a6080;
      --mono:    'Share Tech Mono', monospace;
      --sans:    'Exo 2', sans-serif;
    }}
 
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
 
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--sans);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 2rem 1rem;
      gap: 1.5rem;
    }}
 
    header {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.25rem;
    }}
    header h1 {{
      font-size: 1.05rem;
      font-weight: 300;
      letter-spacing: 0.35em;
      text-transform: uppercase;
      color: var(--muted);
    }}
    .subtitle {{
      font-family: var(--mono);
      font-size: 0.72rem;
      color: var(--muted);
      letter-spacing: 0.1em;
    }}
 
    .status-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.75rem;
      width: 100%;
      max-width: 680px;
    }}
 
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1rem 1.1rem 0.9rem;
      display: flex;
      flex-direction: column;
      gap: 0.3rem;
    }}
    .card .label {{
      font-size: 0.65rem;
      font-weight: 600;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--muted);
    }}
    .card .value {{
      font-family: var(--mono);
      font-size: 1.4rem;
      color: var(--text);
    }}
    .card .sub {{
      font-size: 0.7rem;
      color: var(--muted);
      font-family: var(--mono);
    }}
 
    .controls {{
      width: 100%;
      max-width: 680px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.2rem 1.4rem;
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
    }}
    .controls h2 {{
      font-size: 0.65rem;
      font-weight: 600;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--muted);
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.6rem;
    }}
 
    .ctrl-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      flex-wrap: wrap;
    }}
    .ctrl-label {{
      font-size: 0.85rem;
      color: var(--text);
      font-weight: 300;
      min-width: 160px;
    }}
    .ctrl-label span {{
      display: block;
      font-size: 0.65rem;
      color: var(--muted);
      font-family: var(--mono);
      margin-top: 0.1rem;
    }}
 
    .setpoint-form {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .setpoint-form input[type=number] {{
      width: 70px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 5px;
      color: var(--text);
      font-family: var(--mono);
      font-size: 0.95rem;
      padding: 0.35rem 0.5rem;
      text-align: center;
      outline: none;
    }}
    .setpoint-form input[type=number]:focus {{
      border-color: var(--accent);
    }}
 
    .btn {{
      display: inline-block;
      padding: 0.38rem 1rem;
      border-radius: 5px;
      font-size: 0.78rem;
      font-family: var(--sans);
      font-weight: 600;
      letter-spacing: 0.05em;
      cursor: pointer;
      text-decoration: none;
      border: none;
      transition: opacity 0.15s;
    }}
    .btn:hover {{ opacity: 0.82; }}
    .btn-accent {{ background: var(--accent); color: #0f1220; }}
    .btn-ok     {{ background: var(--ok);     color: #0f1220; }}
    .btn-danger {{ background: var(--danger); color: #fff;    }}
 
    .kill-row {{
      background: color-mix(in srgb, {kill_color} 8%, var(--surface));
      border: 1px solid color-mix(in srgb, {kill_color} 30%, var(--border));
      border-radius: 6px;
      padding: 0.7rem 0.9rem;
    }}
 
    .divider {{
      height: 1px;
      background: var(--border);
      width: 100%;
    }}
 
    @media (max-width: 520px) {{
      .status-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
  </style>
</head>
<body>
 
  <header>
    <h1>Building Management System</h1>
    <div class="subtitle">ENGR 120 &mdash; <span id="refresh-indicator">LIVE</span></div>
  </header>
 
  <div class="status-grid">
    <div class="card">
      <div class="label">Temperature</div>
      <div class="value" id="stat-temp">{temp}&deg;C</div>
      <div class="sub">thermistor</div>
    </div>
    <div class="card">
      <div class="label">Occupancy</div>
      <div class="value" id="stat-occ">{occ_label}</div>
      <div class="sub">pir sensor</div>
    </div>
    <div class="card">
      <div class="label">Lighting</div>
      <div class="value" id="stat-light">{lights_label}</div>
      <div class="sub">ambient: <span id="stat-bright">{is_bright}</span></div>
    </div>
    <div class="card">
      <div class="label">HVAC</div>
      <div class="value" id="stat-hvac">{hvac_icon} {hvac_state}</div>
      <div class="sub">occ <span id="stat-occ-sp">{occ_setpoint}</span>&deg;C
           / unocc <span id="stat-unocc-sp">{unocc_setpoint}</span>&deg;C</div>
    </div>
    <div class="card">
      <div class="label">Occ Setpoint</div>
      <div class="value" id="stat-occ-sp2">{occ_setpoint}&deg;C</div>
      <div class="sub">occupied target</div>
    </div>
    <div class="card">
      <div class="label">Unocc Setpoint</div>
      <div class="value" id="stat-unocc-sp2">{unocc_setpoint}&deg;C</div>
      <div class="sub">unoccupied target</div>
    </div>
  </div>
 
  <div class="controls">
    <h2>Controls</h2>
 
    <div class="ctrl-row">
      <div class="ctrl-label">
        Occupied Setpoint
        <span>Current: <span id="ctrl-occ-sp">{occ_setpoint}</span>&deg;C</span>
      </div>
      <form class="setpoint-form" action="/" method="get">
        <input type="number" name="occ_temp" value="{occ_setpoint}" min="10" max="35" step="1">
        <button class="btn btn-accent" type="submit">Set</button>
      </form>
    </div>
 
    <div class="ctrl-row">
      <div class="ctrl-label">
        Unoccupied Setpoint
        <span>Current: <span id="ctrl-unocc-sp">{unocc_setpoint}</span>&deg;C</span>
      </div>
      <form class="setpoint-form" action="/" method="get">
        <input type="number" name="unocc_temp" value="{unocc_setpoint}" min="5" max="30" step="1">
        <button class="btn btn-accent" type="submit">Set</button>
      </form>
    </div>
 
    <div class="divider"></div>
 
    <div class="ctrl-row">
      <div class="ctrl-label">
        Lighting Override
        <span>Currently: <span id="ctrl-light-status">{lights_label}</span></span>
      </div>
      <a class="btn {'btn-ok' if not lighting else 'btn-danger'}"
         id="ctrl-light-btn" href="{lights_btn_href}">{lights_btn_label}</a>
    </div>
 
    <div class="divider"></div>
 
    <div class="ctrl-row kill-row" id="kill-row">
      <div class="ctrl-label">
        Kill Switch
        <span>Status: <span id="ctrl-kill-status">{kill_label}</span></span>
      </div>
      <a class="btn {'btn-danger' if not kill_active else 'btn-ok'}"
         id="ctrl-kill-btn" href="{kill_btn_href}">{kill_btn_label}</a>
    </div>
  </div>
 
    var HVAC_ICONS = {{
      "heating":     "&#9651;",
      "cooling":     "&#9661;",
      "off":         "&#9711;",
      "kill switch": "&#9940;"
    }};
 
    function updateCards(data) {{

      document.getElementById("stat-temp").innerHTML   = data.temp + "&deg;C";
 
      document.getElementById("stat-occ").textContent  = data.occupied ? "Occupied" : "Unoccupied";
 
      var lightText = data.lighting ? "On" : "Off";
      document.getElementById("stat-light").textContent  = lightText;
      document.getElementById("stat-bright").textContent = data.is_bright;
 
      var icon = HVAC_ICONS[data.hvac_state] || "&#9711;";
      document.getElementById("stat-hvac").innerHTML = icon + " " + data.hvac_state;
 
      // Setpoints in status cards
      document.getElementById("stat-occ-sp").textContent   = data.occ_setpoint;
      document.getElementById("stat-unocc-sp").textContent = data.unocc_setpoint;
      document.getElementById("stat-occ-sp2").innerHTML    = data.occ_setpoint + "&deg;C";
      document.getElementById("stat-unocc-sp2").innerHTML  = data.unocc_setpoint + "&deg;C";
 
      // Setpoint labels in controls section (not the inputs themselves)
      document.getElementById("ctrl-occ-sp").textContent   = data.occ_setpoint;
      document.getElementById("ctrl-unocc-sp").textContent = data.unocc_setpoint;
 
      // Lighting button label/href reflect live state
      var lightBtn = document.getElementById("ctrl-light-btn");
      document.getElementById("ctrl-light-status").textContent = lightText;
      if (data.lighting) {{
        lightBtn.textContent = "Turn Off";
        lightBtn.href        = "/?lights=off";
        lightBtn.className   = "btn btn-danger";
      }} else {{
        lightBtn.textContent = "Turn On";
        lightBtn.href        = "/?lights=on";
        lightBtn.className   = "btn btn-ok";
      }}
 
      var killBtn = document.getElementById("ctrl-kill-btn");
      var killRow = document.getElementById("kill-row");
      document.getElementById("ctrl-kill-status").textContent = data.kill_active ? "ACTIVE" : "Inactive";
      if (data.kill_active) {{
        killBtn.textContent = "Deactivate";
        killBtn.href        = "/?kill=0";
        killBtn.className   = "btn btn-ok";
      }} else {{
        killBtn.textContent = "Activate";
        killBtn.href        = "/?kill=1";
        killBtn.className   = "btn btn-danger";
      }}
    }}
 
    function pollStatus() {{
      fetch("/?status=1")
        .then(function(response) {{ return response.json(); }})
        .then(function(data)     {{ updateCards(data); }})
        .catch(function(err)     {{ console.log("Poll failed:", err); }});
    }}
 
    pollStatus();
    setInterval(pollStatus, 3000);
  </script>
 
</body>
</html>
"""
    return html
