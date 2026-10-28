#!/usr/bin/env python3
"""Small 2D icons for the hardware table (assets/drone/icons/*.svg). Re-run after editing."""
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "icons"; OUT.mkdir(exist_ok=True)
N, RED, GOLD, GREEN, YEL = "#1e3c78", "#c0392b", "#e8c547", "#2e7d32", "#f4d03f"
def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">\n{body}\n</svg>\n'
icons = {}
# F450 frame: X arms (2 white, 2 red) and the centre plate
icons["frame"] = (
 f'<g stroke="{N}" stroke-width="1.6" stroke-linejoin="round">'
 f'<path d="M 32 32 L 8 8 L 14 4 L 36 28 Z" fill="#ffffff"/><path d="M 32 32 L 56 56 L 50 60 L 28 36 Z" fill="#ffffff"/>'
 f'<path d="M 32 32 L 56 8 L 50 4 L 28 28 Z" fill="{RED}"/><path d="M 32 32 L 8 56 L 14 60 L 36 36 Z" fill="{RED}"/>'
 f'<circle cx="32" cy="32" r="9" fill="#e9eef7"/><circle cx="8" cy="8" r="4" fill="#e9eef7"/><circle cx="56" cy="8" r="4" fill="#e9eef7"/><circle cx="8" cy="56" r="4" fill="#e9eef7"/><circle cx="56" cy="56" r="4" fill="#e9eef7"/></g>')
# A2212 outrunner: gold bell, shaft, three wires
icons["motor"] = (
 f'<circle cx="32" cy="28" r="20" fill="{GOLD}" stroke="{N}" stroke-width="1.6"/><circle cx="32" cy="28" r="12" fill="#f7e9a6" stroke="{N}" stroke-width="1"/>'
 f'<circle cx="32" cy="28" r="3" fill="{N}"/><rect x="30" y="4" width="4" height="8" fill="{N}"/>'
 f'<g stroke="{N}" stroke-width="1.6" fill="none"><path d="M 24 46 Q 22 56 16 60"/><path d="M 32 48 L 32 60"/><path d="M 40 46 Q 42 56 48 60"/></g>')
# 30 A ESC in heat-shrink with its leads
icons["esc"] = (
 f'<rect x="14" y="20" width="36" height="24" rx="5" fill="#2b2b2b" stroke="{N}" stroke-width="1.6"/>'
 f'<text x="32" y="36" font-family="Helvetica, Arial, sans-serif" font-size="10" font-weight="bold" text-anchor="middle" fill="#ffffff">30A</text>'
 f'<g stroke-width="2" fill="none"><path d="M 14 26 L 4 26" stroke="{RED}"/><path d="M 14 38 L 4 38" stroke="#1b1b1b"/>'
 f'<path d="M 50 25 L 60 25" stroke="{N}"/><path d="M 50 32 L 60 32" stroke="{N}"/><path d="M 50 39 L 60 39" stroke="{N}"/><path d="M 32 44 L 32 56 L 24 60" stroke="#8a8a8a"/></g>')
# 1045 propeller
icons["propeller"] = (
 f'<g fill="#e9eef7" stroke="{N}" stroke-width="1.6"><path d="M 32 32 C 44 20 60 22 60 30 C 56 34 44 36 32 32 Z"/><path d="M 32 32 C 20 44 4 42 4 34 C 8 30 20 28 32 32 Z"/></g>'
 f'<circle cx="32" cy="32" r="5" fill="{N}"/><circle cx="32" cy="32" r="1.8" fill="#ffffff"/>')
# Pixhawk PRO: board with port rows and the arrow
rows = "".join(f'<rect x="{x}" y="{y}" width="8" height="4" fill="#ffffff" stroke="{N}" stroke-width="0.8"/>' for y in (22, 30, 38) for x in (20, 36))
icons["pixhawk"] = (
 f'<rect x="14" y="6" width="36" height="52" rx="7" fill="#e9eef7" stroke="{N}" stroke-width="1.6"/><rect x="18" y="9" width="28" height="3" fill="#c9d3e6"/>'
 f'<text x="32" y="19" font-family="Helvetica, Arial, sans-serif" font-size="5.5" font-weight="bold" font-style="italic" text-anchor="middle" fill="{N}">pixhawk</text>{rows}'
 f'<path d="M 28 46 L 36 46 L 32 55 Z" fill="#ffffff" stroke="{N}" stroke-width="1"/>')
# M8N GPS puck on its mast
icons["gps"] = (
 f'<ellipse cx="32" cy="16" rx="18" ry="9" fill="#2b2b2b" stroke="{N}" stroke-width="1.6"/><ellipse cx="32" cy="14" rx="12" ry="5" fill="#3d3d3d"/>'
 f'<rect x="30" y="24" width="4" height="26" fill="#2b2b2b"/><rect x="20" y="50" width="24" height="6" rx="2" fill="#2b2b2b"/>')
# PM02 power module with XT60 on both ends
icons["pm02"] = (
 f'<rect x="16" y="22" width="32" height="20" rx="4" fill="#ffffff" stroke="{N}" stroke-width="1.6"/>'
 f'<rect x="4" y="25" width="12" height="14" rx="2" fill="{YEL}" stroke="#8c6d00" stroke-width="1"/><rect x="48" y="25" width="12" height="14" rx="2" fill="{YEL}" stroke="#8c6d00" stroke-width="1"/>'
 f'<path d="M 32 42 L 32 52 L 44 58" fill="none" stroke="{N}" stroke-width="1.6"/><rect x="22" y="27" width="20" height="10" fill="#e9eef7"/>')
# safety switch + buzzer
icons["switch-buzzer"] = (
 f'<circle cx="22" cy="30" r="14" fill="#f8f9fb" stroke="{N}" stroke-width="1.8"/><path d="M 16 26 A 7 7 0 1 0 28 26" fill="none" stroke="{N}" stroke-width="2"/><line x1="22" y1="22" x2="22" y2="30" stroke="{N}" stroke-width="2"/>'
 f'<circle cx="48" cy="34" r="10" fill="#2b2b2b" stroke="{N}" stroke-width="1.4"/><circle cx="48" cy="34" r="3" fill="#555"/><path d="M 22 44 L 22 54 L 48 54 L 48 44" fill="none" stroke="{N}" stroke-width="1.4"/>')
# LiPo 3S
icons["battery"] = (
 f'<rect x="8" y="18" width="44" height="28" rx="4" fill="#ffffff" stroke="{N}" stroke-width="1.6"/><rect x="52" y="26" width="6" height="12" fill="{N}"/>'
 f'<text x="30" y="36" font-family="Helvetica, Arial, sans-serif" font-size="11" font-weight="bold" text-anchor="middle" fill="{N}">3S</text>'
 f'<path d="M 16 46 L 16 54 L 28 54" fill="none" stroke="{RED}" stroke-width="2"/><rect x="28" y="50" width="12" height="9" rx="2" fill="{YEL}" stroke="#8c6d00" stroke-width="1"/>')
# SiK telemetry radio with antenna
icons["radio"] = (
 f'<rect x="12" y="28" width="36" height="24" rx="4" fill="#ffffff" stroke="{N}" stroke-width="1.6"/><rect x="18" y="34" width="24" height="12" fill="#e9eef7"/>'
 f'<line x1="44" y1="28" x2="44" y2="8" stroke="{N}" stroke-width="3"/><circle cx="44" cy="6" r="3" fill="{N}"/><path d="M 12 40 L 4 40" stroke="{N}" stroke-width="2"/>')
# Raspberry Pi 4
pins = "".join(f'<rect x="{12 + i*4}" y="{y}" width="2.4" height="2.4" fill="#444"/>' for i in range(10) for y in (10, 14))
icons["raspberry-pi"] = (
 f'<rect x="6" y="6" width="52" height="40" rx="4" fill="#e3efe3" stroke="{GREEN}" stroke-width="1.6"/>{pins}'
 f'<rect x="26" y="22" width="12" height="12" fill="#cfd8e8" stroke="{N}" stroke-width="0.8"/><rect x="54" y="12" width="6" height="10" fill="#cfd8e8" stroke="{N}" stroke-width="0.8"/><rect x="54" y="26" width="6" height="10" fill="#cfd8e8" stroke="{N}" stroke-width="0.8"/>'
 f'<rect x="4" y="30" width="5" height="8" fill="#cfd8e8" stroke="{N}" stroke-width="0.8"/><text x="32" y="56" font-family="Helvetica, Arial, sans-serif" font-size="6" text-anchor="middle" fill="{GREEN}">Raspberry Pi 4</text>')
# misc: XT60, bullet connector, zip tie
icons["misc"] = (
 f'<rect x="6" y="14" width="18" height="12" rx="2" fill="{YEL}" stroke="#8c6d00" stroke-width="1"/><rect x="24" y="17" width="6" height="6" fill="#8c6d00"/>'
 f'<rect x="38" y="16" width="20" height="8" rx="4" fill="{GOLD}" stroke="{N}" stroke-width="1"/><rect x="36" y="18" width="4" height="4" fill="{N}"/>'
 f'<path d="M 10 40 L 50 40 L 50 48 L 14 48 Z" fill="#ffffff" stroke="{N}" stroke-width="1.4"/><rect x="46" y="36" width="10" height="16" rx="2" fill="#e9eef7" stroke="{N}" stroke-width="1.4"/>')
for name, body in icons.items():
    (OUT / f"{name}.svg").write_text(svg(body), encoding="utf-8")
print("wrote", len(icons), "icons to", OUT)
