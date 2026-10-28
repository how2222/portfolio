#!/usr/bin/env python3
"""Builds the complete system diagram of the drone (hardware wiring + software path), with illustrated parts.

Outputs
  assets/drone/system.svg          static SVG (used by the PDF, and as a fallback)
  assets/drone/_system-inline.md   the same SVG wrapped with a toolbar, tooltips and layer toggles (HTML only)
Edit this file and re-run it:  python3 assets/drone/diagrams/system_diagram.py
Keep to plain SVG (presentation attributes, no CSS for visuals, no foreignObject): the PDF is rendered by Typst / resvg.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent

NAVY, RED, PURPLE, AMBER, GREEN = "#1e3c78", "#c0392b", "#6a3d9a", "#c99700", "#2e7d32"
PANEL, PANEL_STROKE = "#f3f6fb", "#b7c4dd"
TXT, NOTE = "#1b1b1b", "#666666"
BLACK, DARK, SILVER, GOLD, YELLOW, PCB, PCB_DARK = "#1b1b1b", "#2b2b2b", "#d9dde3", "#d4a83a", "#f4d03f", "#2f8a46", "#246d37"
FONT = "Helvetica, Arial, sans-serif"
W, H = 1300, 920

parts = []
def add(s): parts.append(s)

def text(x, y, s, size=11, anchor="middle", weight="normal", fill=TXT, style="normal", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}" fill="{fill}" {extra}>{s}</text>')

def lines(x, y, rows, size=10, anchor="middle", fill=TXT, lh=None, weights=None, extra="", style="normal"):
    lh = lh or size * 1.3
    out = []
    for i, r in enumerate(rows):
        w = (weights or [])[i] if weights and i < len(weights) else "normal"
        out.append(text(x, y + i * lh, r, size, anchor, w, fill, style, extra=extra))
    return "\n".join(out)

def box(x, y, w, h, fill="#ffffff", stroke=NAVY, sw=1.6, rx=6, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def circle(cx, cy, r, fill, stroke="none", sw=1):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def comp(cid, info, body):
    return f'<g id="{cid}" class="comp" data-info="{info}">\n{body}\n</g>'

def wire(pts, kind, info, nodes, width=None, dashed=False, color=None):
    col = color or {"power": RED, "signal": NAVY, "radio": PURPLE, "confirm": AMBER}[kind]
    wdt = width or {"power": 3, "signal": 1.8, "radio": 1.8, "confirm": 1.8}[kind]
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    dash = ' stroke-dasharray="7 5"' if (dashed or kind in ("radio", "confirm")) else ""
    return (f'<path class="wire {kind}" d="{d}" fill="none" stroke="{col}" stroke-width="{wdt}" '
            f'stroke-linejoin="round" stroke-linecap="round"{dash} data-info="{info}" data-nodes="{nodes}"/>')

def gh_port(x, y, label, cid, info, unused=False):
    """White JST-GH connector on the black Pixhawk case, label above."""
    body = "#8a8a8a" if unused else "#f2f2f2"
    lab = "#8a8a8a" if unused else "#ffffff"
    return comp(cid, info,
                box(x - 18, y - 7, 36, 14, body, "#555" if unused else "#c9c9c9", 1, 2) +
                f'<rect x="{x-13}" y="{y-2}" width="26" height="4" fill="#4a4a4a"/>' +
                text(x, y - 10, label, 8.5, "middle", "bold", lab))

def antenna(x, y_base, h=40, col=BLACK):
    return (f'<rect x="{x-4}" y="{y_base-6}" width="8" height="8" fill="#8a8f98"/>'
            f'<line x1="{x}" y1="{y_base-6}" x2="{x}" y2="{y_base-h}" stroke="{col}" stroke-width="4"/>'
            + circle(x, y_base - h - 2, 3.5, col))

# ============================================================== panels
add(box(30, 40, 310, 600, PANEL, PANEL_STROKE, 1, 14))
add(text(45, 66, "Ground station — MacBook", 13, "start", "bold", NAVY))
add(box(390, 40, 890, 820, PANEL, PANEL_STROKE, 1, 14))
add(text(405, 66, "Drone — F450 quadcopter", 13, "start", "bold", NAVY))

hw, sw, pw, sg, rd, cf = [], [], [], [], [], []

# ============================================================== ground station
mac = (box(70, 88, 230, 152, SILVER, "#9aa4b5", 1.5, 8) + box(78, 96, 214, 130, "#111111", "#111111", 1, 4) +
       box(84, 102, 202, 118, "#f8f9fb", "#f8f9fb", 1, 2) +
       f'<path d="M 58 240 L 312 240 L 322 258 L 48 258 Z" fill="#c9ced6" stroke="#9aa4b5" stroke-width="1.4"/>' +
       "".join(f'<rect x="{100 + i*14}" y="{244}" width="11" height="4" rx="1" fill="#e9ecf1"/>' for i in range(12)) +
       f'<rect x="160" y="250" width="50" height="5" rx="2" fill="#e9ecf1"/>' + text(185, 274, "MacBook", 11, "middle", "bold", NAVY))
hw.append(comp("mac", "MacBook: QGroundControl for setup and monitoring (over USB-C or the radio), and mavcontrol.py, the Python + pygame program that flies the drone", mac))
hw.append(comp("gradio", "SiK telemetry radio V5, ground module (from the Pixhawk kit): 433 MHz, 100 mW, USB on the Mac — mavcontrol.py opens it as /dev/tty.usbserial-0001 at 57 600 baud",
    box(110, 350, 130, 48, BLACK, "#000000", 1.4, 6) + f'<rect x="96" y="366" width="16" height="16" rx="2" fill="#8a8f98"/>' +
    antenna(225, 350, 42) + circle(122, 358, 2.2, "#e53935") + circle(130, 358, 2.2, "#43a047") +
    lines(178, 370, ["SiK telemetry radio V5", "ground · 433 MHz · 100 mW"], 9.5, weights=["bold", "normal"], fill="#ffffff")))
hw.append(lines(70, 432, ["No RC transmitter: the drone is flown", "from mavcontrol.py on the Mac."], 10, "start", NOTE, style="italic"))
hw.append(text(182, 300, "USB", 9, "start", "normal", NOTE))
sw.append('<g data-comp="mac" data-info="QGroundControl on the Mac: firmware (ArduCopter 4.6.3), calibrations, parameters and monitoring, over USB-C or the telemetry link">' +
          box(90, 108, 190, 48, "#f1e9f7", PURPLE, 1.2, 5) + lines(185, 126, ["QGroundControl", "setup · calibration · monitoring"], 9.5, weights=["bold", "normal"], fill=PURPLE) + "</g>")
sw.append('<g data-comp="mac" data-info="mavcontrol.py (Python + pygame): arm / disarm, take-off, land, throttle and mode keys, RC override of the throttle channel at 10 Hz, live monitor of attitude, yaw rate and motor PWM">' +
          box(90, 162, 190, 56, "#f1e9f7", PURPLE, 1.2, 5) + lines(185, 180, ["mavcontrol.py (pygame)", "arm · throttle · modes · monitor", "RC overrides over MAVLink"], 9.5, weights=["bold", "normal", "normal"], fill=PURPLE) + "</g>")

# ============================================================== motors / ESCs / plate
MOT_X = [735, 825, 915, 1005]
WIRED = ["M1 · front-right · CCW", "M2 · rear-left · CCW", "M3 · front-left · CW", "M4 · rear-right · CW"]   # Quad X convention
for i, cx in enumerate(MOT_X):
    n = i + 1
    slots = "".join(circle(cx + 19 * __import__("math").cos(a), 95 + 19 * __import__("math").sin(a), 2.2, "#8c6d1a") for a in [k * 0.785 for k in range(8)])
    hw.append(comp(f"m{n}", f"Motor {n} of the Quad X layout ({WIRED[i].split(chr(183))[1].strip()}, {WIRED[i].split(chr(183))[2].strip()}): A2212 13T 1000KV brushless outrunner with a 1045 propeller",
        circle(cx, 95, 26, GOLD, "#8c6d1a", 1.5) + slots + circle(cx, 95, 9, SILVER, "#777777", 1) + circle(cx, 95, 2.5, "#555555") +
        lines(cx, 134, [WIRED[i].split(" · ")[0], " · ".join(WIRED[i].split(" · ")[1:])], 8.5, weights=["bold", "normal"], fill=NAVY, lh=10)))
    hw.append(comp(f"esc{n}", f"ESC of motor {n}: 30 A brushless ESC (SimonK-type) with a 5 V / 2 A BEC, in heat-shrink; its power leads end in crimped brass bullet connectors mated to XT60 connectors on the plate (nothing soldered)",
        box(cx - 30, 152, 60, 32, DARK, "#111111", 1.4, 6) + text(cx, 166, f"ESC {n}", 9.5, "middle", "bold", "#ffffff") + text(cx, 178, "30A", 8, "middle", "normal", "#cfcfcf")))
hw.append(lines(1050, 90, ["A2212 1000KV", "+ 1045 props"], 9.5, "start", NOTE, style="italic"))
hw.append(lines(1050, 160, ["30 A ESC (5 V BEC)", "SERVOn_FUNCTION must match the motor", "each output really drives: the numbers", "printed on this board's MAIN OUT rail", "do not match the firmware outputs"], 8.5, "start", NOTE, style="italic", lh=11))
pads = "".join(f'<rect x="{675 + i*52}" y="{216}" width="14" height="6" fill="{GOLD}"/>' for i in range(8))
hw.append(comp("plate", "F450 bottom plate: the frame's power distribution board (black PCB with copper pads), pre-soldered; the ESCs plug into it through XT60 and crimped brass bullet connectors (nothing soldered on this build)",
    box(660, 210, 420, 26, BLACK, "#000000", 1.4, 5) + pads + text(870, 231, "F450 bottom plate = power distribution board (+ / −)", 10.5, "middle", "bold", "#ffffff")))
for i, cx in enumerate(MOT_X):
    n = i + 1
    pw.append(wire([(cx, 152), (cx, 121)], "power", f"ESC {n} → motor: three phase wires on brass bullet connectors (crimped, not soldered); swapping two reverses the spin", f"esc{n} m{n}", 3))
    pw.append(wire([(cx + 16, 210), (cx + 16, 184)], "power", f"Plate → ESC {n}: battery voltage (+ / −)", f"plate esc{n}", 2.5))
for i, (px, jog, tx) in enumerate([(815, 248, 719), (835, 244, 809), (855, 244, 899), (875, 248, 989)]):
    n = i + 1
    sg.append(wire([(px, 264), (px, jog), (tx, jog), (tx, 184)], "signal", f"MAIN OUT → ESC {n}: PWM servo lead (signal + ground); which motor each output drives is set by SERVOn_FUNCTION (the pin numbers printed on this board do not match the firmware outputs)", f"pixhawk esc{n}", 1.6))

# ============================================================== Pixhawk PRO (black case, white labels)
pins = "".join(circle(724 + i * 7, y, 1.3, "#cfcfcf") for i in range(33) for y in (269, 276, 283))
hw.append(comp("pixhawk", "Pixhawk PRO flight controller: STM32F4 @ 168 MHz, 2 MB flash (FMUv3-class), running ArduCopter 4.6.3",
    box(705, 262, 260, 428, BLACK, "#000000", 2, 26) + box(717, 296, 236, 382, "#262626", "#262626", 1, 14) +
    f'<rect x="717" y="264" width="236" height="26" rx="3" fill="#0f0f0f"/>' + pins +
    "".join(circle(x, y, 4, "#8a8f98", "#555", 1) for x, y in ((722, 302), (948, 302), (722, 672), (948, 672))) +
    text(760, 294, "AUX OUT", 7.5, "middle", "bold", "#ffffff") + text(845, 294, "MAIN OUT 1–8", 7.5, "middle", "bold", "#ffffff") + text(925, 294, "SBUS · RCIN", 7.5, "middle", "bold", "#ffffff") +
    text(835, 324, "pixhawk", 22, "middle", "bold", "#ffffff", "italic") + text(835, 339, "PRO", 10, "middle", "bold", "#ffffff") +
    circle(735, 349, 2.5, "#8fd18f") + circle(935, 349, 2.5, "#8fd18f") + text(745, 352, "FMU", 7, "start", "normal", "#bbbbbb") + text(929, 352, "IO", 7, "end", "normal", "#bbbbbb") +
    circle(835, 556, 9, "#555555", "#8a8a8a", 1) +
    f'<path d="M 823 604 L 847 604 L 835 648 Z" fill="#ffffff"/>' +
    f'<rect x="699" y="524" width="12" height="18" rx="2" fill="#cfcfcf" stroke="#777" stroke-width="1"/>' + text(694, 537, "USB-C", 8, "end", "bold", NAVY)))
PORTS = [
    (745, 372, "SPKT/DSM", "p-spkt", "SPKT/DSM: Spektrum satellite receiver input (unused)"),
    (925, 372, "BUZZER", "p-buzzer", "BUZZER port: the buzzer from the kit"),
    (745, 418, "TELEM 2", "p-telem2", "TELEM 2 = SERIAL2: MAVLink 2 to the Raspberry Pi at 57 600 baud (SERIAL2_PROTOCOL = 2, SERIAL2_BAUD = 57); its 5 V pin also powers the Pi"),
    (835, 418, "SWITCH", "p-switch", "SWITCH port: safety switch (must be pressed before arming)"),
    (925, 418, "SERIAL 4/5", "p-s45", "SERIAL 4/5 (unused)"),
    (745, 464, "TELEM 1", "p-telem1", "TELEM 1 = SERIAL1: the SiK telemetry radio (air module)"),
    (925, 464, "GPS", "p-gps", "GPS port: u-blox M8N over UART (6-pin cable)"),
    (745, 510, "USB", "p-usb", "USB (GH connector, unused; the side USB-C is used for setup)"),
    (835, 510, "ADC 3.3V", "p-adc33", "ADC 3.3 V input (unused)"),
    (925, 510, "CAN", "p-can", "CAN bus (unused)"),
    (745, 598, "SPI", "p-spi", "SPI (unused)"),
    (925, 598, "I2C", "p-i2c", "I2C port: the M8N module's compass (4-pin cable)"),
    (745, 642, "POWER", "p-power", "POWER port: 6-pin lead from the PM02 — 5.2 V supply plus battery voltage and current sensing"),
    (925, 642, "ADC 6.6V", "p-adc66", "ADC 6.6 V input (unused)"),
]
for x, y, lab, pid, info in PORTS:
    hw.append(gh_port(x, y, lab, pid, info, unused="unused" in info))
sw.append('<g data-comp="pixhawk" data-info="ArduCopter 4.6.3 (fmuv3 build) on the Pixhawk PRO: Quad X; SERIAL2_PROTOCOL = 2, SERIAL2_BAUD = 57; arming checks for RC and GPS disabled, FS_THR_ENABLE = 0, DISARM_DELAY = 0">' +
          box(690, 702, 290, 52, "#f1e9f7", PURPLE, 1.2, 5) + lines(835, 721, ["ArduCopter 4.6.3 (fmuv3 build) · Quad X", "SERIAL2: MAVLink 2 @ 57 600 baud", "RC + GPS arming checks off · FS_THR 0 · DISARM_DELAY 0"], 9.5, weights=["bold", "normal", "normal"], fill=PURPLE) + "</g>")

# ============================================================== Raspberry Pi 4 (85 x 56 mm at 3 px/mm, origin 400,330)
def mm(x, y): return 400 + 3 * x, 330 + 3 * y
pi = box(400, 330, 255, 168, PCB, PCB_DARK, 2, 7)
for hx, hy in ((3.5, 3.5), (61.5, 3.5), (3.5, 52.5), (61.5, 52.5)):
    x, y = mm(hx, hy); pi += circle(x, y, 5, YELLOW, "#c9a40c", 1) + circle(x, y, 2.4, "#f8f9fb")
pi += box(417, 336, 158, 17, "#1b1b1b", "#000000", 1, 2)          # GPIO header block
PIN_COL = {0: RED, 2: "#111111", 3: NAVY, 4: GREEN}                   # pins 2 (5 V), 6 (GND), 8 (TXD), 10 (RXD) on the outer row
for i in range(20):
    x = 421.3 + 7.62 * i
    pi += circle(x, 340.5, 2.3, PIN_COL.get(i, "#9aa4b5")) + circle(x, 348.1, 2.3, "#9aa4b5")
pi += box(587, 350, 12, 10, "#1b1b1b", "#000000", 1, 1)           # PoE header
x, y = mm(65, 2);  pi += box(x, y, 66, 48, SILVER, "#9aa4b5", 1.2, 3) + box(x + 8, y + 10, 50, 28, "#9aa4b5", "#9aa4b5", 1, 2)   # Ethernet
x, y = mm(65, 22); pi += box(x, y, 66, 42, SILVER, "#9aa4b5", 1.2, 3) + box(x + 8, y + 6, 50, 12, "#9aa4b5", "#9aa4b5", 1, 1) + box(x + 8, y + 24, 50, 12, "#9aa4b5", "#9aa4b5", 1, 1)
x, y = mm(65, 38); pi += box(x, y + 12, 66, 42, SILVER, "#9aa4b5", 1.2, 3) + box(x + 8, y + 18, 50, 12, "#9aa4b5", "#9aa4b5", 1, 1) + box(x + 8, y + 36, 50, 12, "#9aa4b5", "#9aa4b5", 1, 1)
x, y = mm(23, 19); pi += box(x, y, 40, 40, SILVER, "#9aa4b5", 1.2, 4) + box(x + 7, y + 7, 26, 26, "#c3c9d2", "#b0b7c2", 1, 2)   # SoC
x, y = mm(38, 19); pi += box(x, y, 30, 30, "#1b1b1b", "#000000", 1, 2) + text(x + 15, y + 18, "RAM", 7, "middle", "normal", "#9aa4b5")
x, y = mm(55, 27); pi += box(x, y, 18, 18, "#1b1b1b", "#000000", 1, 2)
x, y = mm(50, 20); pi += box(x, y, 7, 70, "#1b1b1b", "#000000", 1, 1) + "".join(f'<rect x="{x+2}" y="{y+6+k*4}" width="3" height="2" fill="#c9a40c"/>' for k in range(15))   # camera connector
x, y = mm(1, 15);  pi += box(x, y, 7, 70, "#1b1b1b", "#000000", 1, 1) + "".join(f'<rect x="{x+2}" y="{y+6+k*4}" width="3" height="2" fill="#c9a40c"/>' for k in range(15))   # display connector
x, y = mm(7.5, 53); pi += box(x, y, 27, 12, SILVER, "#9aa4b5", 1.2, 3) + box(x + 6, y + 3, 15, 6, "#9aa4b5", "#9aa4b5", 1, 3)   # USB-C power
for hx in (20, 31.5):
    x, y = mm(hx, 53); pi += box(x, y, 24, 12, SILVER, "#9aa4b5", 1.2, 2) + box(x + 5, y + 3, 14, 6, "#9aa4b5", "#9aa4b5", 1, 1)   # micro-HDMI
x, y = mm(53.5, 51); pi += box(x, y, 16, 20, "#1b1b1b", "#000000", 1, 3) + circle(x + 8, y + 20, 5, "#333333", "#000", 1)   # audio jack
lx, ly = mm(14, 31)
berry = "".join(circle(lx + dx, ly + dy, 3.6, "#ffffff") for dx, dy in ((-4, -3), (4, -3), (-7.5, 2.5), (0, 2.5), (7.5, 2.5), (-4, 8), (4, 8), (0, 12.5)))
leaves = (f'<path d="M {lx-1} {ly-7} C {lx-6} {ly-9} {lx-11} {ly-9} {lx-13} {ly-13} C {lx-8} {ly-14} {lx-3} {ly-12} {lx-1} {ly-7} Z" fill="#ffffff"/>'
          f'<path d="M {lx+1} {ly-7} C {lx+6} {ly-9} {lx+11} {ly-9} {lx+13} {ly-13} C {lx+8} {ly-14} {lx+3} {ly-12} {lx+1} {ly-7} Z" fill="#ffffff"/>')
pi += berry + leaves   # raspberry logo: lobes + two leaves
pi += text(421, 362, "pin 2 · 5 V    6 · GND    8 · TXD    10 · RXD", 7.5, "start", "normal", "#ffffff")
pi += text(421, 456, "Raspberry Pi 4 Model B · 2 GB", 9, "start", "bold", "#ffffff")
hw.append(comp("pi", "Raspberry Pi 4 Model B, 2 GB: companion computer running MAVProxy / pymavlink, linked to the Pixhawk over UART (TELEM 2) and powered from the same connector's 5 V pin", pi))
hw.append(lines(400, 512, ["Powered from the Pixhawk's TELEM 2 5 V pin (via the PM02)"], 8, "start", NOTE, style="italic", lh=10))
sw.append('<g data-comp="pi" data-info="On the Pi: Raspberry Pi OS 32-bit, MAVProxy and pymavlink in a virtual environment (~/mavlink_project/venv), started by hand over SSH: mavproxy.py --master=/dev/serial0 --baudrate 57600">' +
          box(400, 534, 255, 44, "#f1e9f7", PURPLE, 1.2, 5) + lines(527, 550, ["Raspberry Pi OS 32-bit · MAVProxy + pymavlink (venv)", "/dev/serial0 @ 57 600 baud · started by hand over SSH"], 9.5, weights=["bold", "normal"], fill=PURPLE) + "</g>")
sg.append(wire([(444, 335), (444, 300), (690, 300), (690, 418), (727, 418)], "signal", "Pi UART (pin 8 TXD → TELEM2 RX, pin 10 RXD ← TELEM2 TX, pin 6 GND) ↔ Pixhawk TELEM 2: MAVLink 2 at 57 600 baud", "pi p-telem2 pixhawk", 1.8))
pw.append(wire([(421, 335), (421, 292), (682, 292), (682, 412), (727, 412)], "power", "TELEM 2 5 V pin → Pi pin 2 (5 V): the Pi is powered by the flight controller's 5 V rail", "pi p-telem2 pixhawk", 1.6))
sg.append(text(567, 311, "UART · MAVLink 2 · 57 600 baud  (red: 5 V to the Pi)", 9.5, "middle", "normal", NAVY))

# ============================================================== telemetry air module
hw.append(comp("aradio", "SiK telemetry radio V5, air module (from the Pixhawk kit): 433 MHz, 100 mW, on TELEM 1; carries MAVLink between the Mac and the Pixhawk",
    box(440, 606, 150, 48, BLACK, "#000000", 1.4, 6) + antenna(575, 606, 22) + circle(452, 614, 2.2, "#e53935") + circle(460, 614, 2.2, "#43a047") +
    lines(515, 626, ["SiK telemetry radio V5", "air · 433 MHz · 100 mW"], 9.5, weights=["bold", "normal"], fill="#ffffff")))
sg.append(wire([(590, 630), (680, 630), (680, 464), (727, 464)], "signal", "Air radio → TELEM 1 (6-pin GH cable): MAVLink", "aradio p-telem1 pixhawk", 1.8))
sg.append(text(636, 623, "TELEM 1", 9, "middle", "normal", NAVY))

# ============================================================== power chain
hw.append(comp("pm02", "PM02 V3.2 power module (kit): 2–12S input, 5.2 V / 3 A output to the flight controller, voltage and current sensing; XT60 in and out — battery settings never configured in QGroundControl",
    box(430, 674, 180, 62, DARK, "#111111", 1.4, 6) +
    f'<rect x="422" y="698" width="14" height="14" rx="2" fill="{YELLOW}" stroke="#8c6d00" stroke-width="1"/><rect x="604" y="698" width="14" height="14" rx="2" fill="{YELLOW}" stroke="#8c6d00" stroke-width="1"/>' +
    f'<rect x="505" y="668" width="30" height="8" rx="2" fill="#f2f2f2" stroke="#999" stroke-width="1"/>' +
    lines(520, 695, ["PM02 V3.2 power module", "5.2 V BEC · V / I sensing", "XT60 in / out · 6-pin to POWER"], 9.5, weights=["bold", "normal", "normal"], fill="#ffffff")))
hw.append(comp("battery", "LiPo 3S 11.1 V, 3000 mAh, 35C, XT60 (AMZZN) — stored in a LiPo-safe bag",
    box(430, 778, 150, 60, "#1f2a44", "#0f1830", 1.6, 7) + box(442, 790, 126, 36, "#2d3b5e", "#2d3b5e", 1, 4) +
    f'<rect x="580" y="798" width="10" height="22" rx="2" fill="{YELLOW}" stroke="#8c6d00" stroke-width="1"/><rect x="574" y="826" width="14" height="6" fill="#f2f2f2"/>' +
    lines(505, 805, ["LiPo 3S 11.1 V", "3000 mAh · 35C · XT60"], 10, weights=["bold", "normal"], fill="#ffffff")))
pw.append(wire([(505, 778), (505, 736)], "power", "Battery → PM02 (XT60)", "battery pm02", 3))
pw.append(text(512, 760, "XT60", 9, "start", "normal", RED))
pw.append(wire([(610, 688), (660, 688), (660, 642), (727, 642)], "power", "PM02 6-pin lead → POWER port: 5.2 V supply + battery voltage / current sensing", "pm02 p-power pixhawk", 1.6))
pw.append(text(693, 636, "5.2 V + V/I", 8.5, "middle", "normal", RED))
pw.append(wire([(430, 720), (405, 720), (405, 222), (660, 222)], "power", "PM02 XT60 out → F450 plate: main battery current to the ESCs", "pm02 plate", 3))
pw.append(text(411, 470, "main current", 9, "middle", "normal", RED, extra='transform="rotate(-90 411 470)"'))

# ============================================================== buzzer, switch, GPS
hw.append(comp("buzzer", "Buzzer (kit): arming and status tones", circle(1090, 300, 18, BLACK, "#000", 1.5) + circle(1090, 300, 12, "#2e2e2e") + circle(1090, 300, 4, "#555555") + text(1090, 335, "Buzzer", 10, "middle", "bold", NAVY)))
hw.append(comp("switch", "Safety switch (kit): must be pressed before the motors can be armed; its LED ring blinks until then",
    circle(1190, 300, 19, "#f8f9fb", "#c0392b", 3) + f'<path d="M 1183 294 A 9 9 0 1 0 1197 294" fill="none" stroke="{BLACK}" stroke-width="2.2"/><line x1="1190" y1="289" x2="1190" y2="300" stroke="{BLACK}" stroke-width="2.2"/>' +
    text(1190, 335, "Safety switch", 10, "middle", "bold", NAVY)))
hw.append(comp("gps", "u-blox M8N GPS + compass module on its mast (kit): GPS over UART, compass over I2C; no GPS fix indoors",
    circle(1140, 440, 28, BLACK, "#000", 1.5) + circle(1140, 440, 21, "#2e2e2e") + text(1140, 444, "M8N", 8, "middle", "bold", "#cfcfcf") +
    f'<path d="M 1140 424 L 1145 433 L 1135 433 Z" fill="#cfcfcf"/>' +
    f'<rect x="1137" y="468" width="6" height="32" fill="#111111"/><rect x="1125" y="500" width="30" height="8" rx="2" fill="#222222"/>' +
    text(1140, 526, "M8N GPS + compass", 10, "middle", "bold", NAVY)))
sg.append(wire([(1072, 300), (1000, 300), (1000, 372), (943, 372)], "signal", "Buzzer → BUZZER port", "buzzer p-buzzer pixhawk", 1.6))
sg.append(wire([(1190, 319), (1190, 395), (835, 395), (835, 411)], "signal", "Safety switch → SWITCH port", "switch p-switch pixhawk", 1.6))
sg.append(wire([(1112, 448), (1000, 448), (1000, 464), (943, 464)], "signal", "M8N GPS → GPS port (UART, 6-pin)", "gps p-gps pixhawk", 1.6))
sg.append(text(1040, 441, "GPS (UART)", 9, "middle", "normal", NAVY))
sg.append(wire([(1140, 508), (1140, 598), (943, 598)], "signal", "M8N compass → I2C port (4-pin)", "gps p-i2c pixhawk", 1.6))
sg.append(text(1040, 592, "I2C (compass)", 9, "middle", "normal", NAVY))

# ============================================================== wireless links
rd.append(wire([(300, 190), (360, 190), (360, 410), (400, 410)], "radio", "Wi-Fi: the Mac reaches the Pi over SSH on the home network", "mac pi"))
rd.append(text(352, 300, "Wi-Fi · SSH", 9.5, "middle", "normal", PURPLE, extra='transform="rotate(-90 352 300)"'))
rd.append(wire([(240, 374), (372, 374), (372, 631), (440, 631)], "radio", "433 MHz link between the two SiK radios: MAVLink from mavcontrol.py / QGroundControl to the Pixhawk", "gradio aradio"))
rd.append(text(366, 500, "MAVLink · 433 MHz", 9.5, "middle", "normal", PURPLE, extra='transform="rotate(-90 366 500)"'))
sg.append(wire([(175, 258), (175, 350)], "signal", "USB: ground radio on the Mac", "mac gradio", 1.6))

# ============================================================== legend
leg = []
leg.append(f'<line x1="45" y1="885" x2="75" y2="885" stroke="{RED}" stroke-width="3"/>' + text(82, 889, "Power", 10, "start"))
leg.append(f'<line x1="140" y1="885" x2="170" y2="885" stroke="{NAVY}" stroke-width="2"/>' + text(177, 889, "Wiring (signal / data)", 10, "start"))
leg.append(f'<line x1="315" y1="885" x2="345" y2="885" stroke="{PURPLE}" stroke-width="2" stroke-dasharray="7 5"/>' + text(352, 889, "Wireless link", 10, "start"))
leg.append(f'<rect x="440" y="877" width="22" height="14" rx="3" fill="#f1e9f7" stroke="{PURPLE}" stroke-width="1.2"/>' + text(469, 889, "Software", 10, "start"))
leg.append(text(1275, 889, "Grey ports: unused", 9.5, "end", "normal", NOTE, "italic"))

svg_body = "\n".join([
    "\n".join(parts),
    '<g class="layer layer-hw">', "\n".join(hw), "</g>",
    '<g class="layer layer-software">', "\n".join(sw), "</g>",
    '<g class="layer layer-power">', "\n".join(pw), "</g>",
    '<g class="layer layer-signal">', "\n".join(sg), "</g>",
    '<g class="layer layer-radio">', "\n".join(rd), "</g>",
    '<g class="layer layer-confirm">', "\n".join(cf), "</g>",
    '<g class="legend">', "\n".join(leg), "</g>",
])
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">\n'
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>\n{svg_body}\n</svg>\n')
(OUT / "system.svg").write_text(svg, encoding="utf-8")

inline_svg = svg.replace(f'width="{W}" height="{H}" ', 'id="sysdiag-svg" ')
html = r'''```{=html}
<div class="sysdiag" id="sysdiag">
<div class="sysdiag-bar">
  <span class="sysdiag-lbl">Layers</span>
  <label><input type="checkbox" data-layer="power" checked> Power</label>
  <label><input type="checkbox" data-layer="signal" checked> Wiring</label>
  <label><input type="checkbox" data-layer="radio" checked> Wireless</label>
  <label><input type="checkbox" data-layer="software" checked> Software</label>
  <span class="sysdiag-hint">Hover a wire or a part for details · click a part to highlight its connections</span>
  <button type="button" class="sysdiag-fs" data-act="fs">Full screen</button>
</div>
<div class="sysdiag-stage">
''' + inline_svg + r'''</div>
<div class="sysdiag-tip" hidden></div>
</div>
<style>
.sysdiag { border: 1px solid #d9dfea; border-radius: 8px; background: #fff; margin: 1rem 0 1.5rem; }
.sysdiag-bar { display: flex; flex-wrap: wrap; gap: .4rem .9rem; align-items: center; padding: .5rem .75rem; border-bottom: 1px solid #e3e8f0; font-size: .85rem; }
.sysdiag-bar label { cursor: pointer; user-select: none; }
.sysdiag-bar input { margin-right: .25rem; vertical-align: -1px; }
.sysdiag-lbl { font-weight: 600; color: #1e3c78; }
.sysdiag-hint { color: #666; font-style: italic; margin-left: auto; }
.sysdiag-fs { border: 1px solid #1e3c78; background: #fff; color: #1e3c78; border-radius: 5px; padding: .2rem .6rem; cursor: pointer; font-size: .85rem; }
.sysdiag-fs:hover { background: #1e3c78; color: #fff; }
.sysdiag-stage { overflow: auto; }
.sysdiag-stage svg { display: block; width: 100%; height: auto; }
.sysdiag:fullscreen { border: 0; border-radius: 0; overflow: auto; }
.sysdiag:fullscreen .sysdiag-stage svg { width: auto; height: calc(100vh - 3.2rem); margin: 0 auto; }
.sysdiag .wire { cursor: pointer; transition: opacity .15s; }
.sysdiag .wire:hover { stroke-width: 5px; }
.sysdiag .comp { cursor: pointer; transition: opacity .15s; }
.sysdiag.focus .wire:not(.on) { opacity: .12; }
.sysdiag.focus .comp:not(.on) { opacity: .28; }
.sysdiag.focus .layer-software, .sysdiag.focus .legend { opacity: .35; }
.sysdiag .layer.off { display: none; }
.sysdiag-tip { position: fixed; z-index: 2000; max-width: 340px; background: #1b1b1b; color: #fff; font-size: .8rem; line-height: 1.3; padding: .4rem .6rem; border-radius: 5px; pointer-events: none; box-shadow: 0 2px 8px rgba(0,0,0,.3); }
</style>
<script>
(function () {
  const root = document.getElementById('sysdiag'); if (!root) return;
  const svg = root.querySelector('svg'), tip = root.querySelector('.sysdiag-tip');
  root.querySelectorAll('input[data-layer]').forEach(cb => cb.addEventListener('change', () => {
    svg.querySelector('.layer-' + cb.dataset.layer).classList.toggle('off', !cb.checked);
  }));
  root.querySelector('[data-act="fs"]').addEventListener('click', () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (root.requestFullscreen) root.requestFullscreen();
  });
  svg.addEventListener('mousemove', e => {
    const t = e.target.closest('[data-info]');
    if (!t) { tip.hidden = true; return; }
    tip.textContent = t.dataset.info; tip.hidden = false;
    const x = Math.min(e.clientX + 14, window.innerWidth - 360), y = e.clientY + 16;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
  });
  svg.addEventListener('mouseleave', () => { tip.hidden = true; });
  svg.addEventListener('click', e => {
    const c = e.target.closest('.comp') || (e.target.closest('[data-comp]') && svg.getElementById(e.target.closest('[data-comp]').dataset.comp));
    svg.querySelectorAll('.on').forEach(el => el.classList.remove('on'));
    if (!c) { root.classList.remove('focus'); return; }
    const id = c.id; let hit = false;
    svg.querySelectorAll('.wire').forEach(w => {
      const nodes = (w.dataset.nodes || '').split(' ');
      if (nodes.includes(id)) { hit = true; w.classList.add('on'); nodes.forEach(n => { const el = svg.getElementById(n); if (el) el.classList.add('on'); }); }
    });
    c.classList.add('on');
    root.classList.toggle('focus', hit);
  });
})();
</script>
```
'''
(OUT / "_system-inline.md").write_text(html, encoding="utf-8")
print("wrote", OUT / "system.svg", "and", OUT / "_system-inline.md")
