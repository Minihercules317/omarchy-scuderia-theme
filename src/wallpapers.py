#!/usr/bin/env python3
"""Generate original Scuderia / Leclerc wallpapers as SVG.

Variants: sedici (carbon fibre + #16), monaco (stylised circuit map), livery (bodywork sweep).
Text uses Titillium Web from ../fonts (point FONTCONFIG_FILE at a config that includes it).
"""
import sys

W, H = 2560, 1600
# 16:9 screens crop ~80px off top and bottom; keep text >= 180px from those edges
FONT = "Titillium Web"
ROSSO = "#ff2800"
CORSA = "#dc0000"
GIALLO = "#ffcf00"

DEFS = f'''
<pattern id="carbon" width="28" height="28" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <rect width="28" height="28" fill="#0b0a0a"/>
  <rect x="0" y="0" width="14" height="14" fill="url(#weaveA)"/>
  <rect x="14" y="14" width="14" height="14" fill="url(#weaveA)"/>
  <rect x="14" y="0" width="14" height="14" fill="url(#weaveB)"/>
  <rect x="0" y="14" width="14" height="14" fill="url(#weaveB)"/>
</pattern>
<linearGradient id="weaveA" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#0d0c0c"/><stop offset="0.5" stop-color="#262222"/><stop offset="1" stop-color="#0d0c0c"/>
</linearGradient>
<linearGradient id="weaveB" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0a0909"/><stop offset="0.5" stop-color="#1a1717"/><stop offset="1" stop-color="#0a0909"/>
</linearGradient>
<linearGradient id="rosso" x1="0" y1="0" x2="0.3" y2="1">
  <stop offset="0" stop-color="#ff4a26"/><stop offset="0.45" stop-color="{ROSSO}"/><stop offset="1" stop-color="#9e0000"/>
</linearGradient>
<radialGradient id="vignette" cx="50%" cy="50%" r="75%">
  <stop offset="0.45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.85"/>
</radialGradient>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="softglow" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
'''


def text(x, y, s, size, fill="#f2ecec", weight=700, anchor="start", spacing=0, opacity=1, italic=False, extra=""):
    style = "italic" if italic else "normal"
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" font-style="{style}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}" opacity="{opacity}" {extra}>{s}</text>')


def monaco_flag(x, y, w=120, h=80):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h/2}" fill="{CORSA}"/>'
            f'<rect x="{x}" y="{y+h/2}" width="{w}" height="{h/2}" fill="#f5f5f5"/>')


def speed_lines(seed_rows):
    out = []
    for i, (y, x0, length, op, sw) in enumerate(seed_rows):
        out.append(f'<line x1="{x0}" y1="{y}" x2="{x0+length}" y2="{y}" stroke="{ROSSO if i % 3 else "#ffffff"}" '
                   f'stroke-width="{sw}" stroke-linecap="round" opacity="{op}"/>')
    return "\n".join(out)


def sedici():
    lines = speed_lines([
        (380, 120, 700, 0.35, 3), (430, 60, 980, 0.18, 2), (1180, 1500, 900, 0.25, 3),
        (1230, 1700, 760, 0.4, 2), (1280, 1300, 1100, 0.15, 2), (520, 200, 520, 0.22, 2),
    ])
    num = (f'<g transform="translate(1280,1080) skewX(-12)">'
           f'<text x="18" y="18" font-family="{FONT}" font-size="1100" font-weight="900" text-anchor="middle" '
           f'fill="#000" opacity="0.6">16</text>'
           f'<text x="0" y="0" font-family="{FONT}" font-size="1100" font-weight="900" text-anchor="middle" '
           f'fill="url(#rosso)" stroke="#ffffff" stroke-width="10" filter="url(#glow)">16</text></g>')
    return f'''
<rect width="{W}" height="{H}" fill="url(#carbon)"/>
<radialGradient id="redhaze" cx="50%" cy="55%" r="45%"><stop offset="0" stop-color="{CORSA}" stop-opacity="0.35"/><stop offset="1" stop-color="{CORSA}" stop-opacity="0"/></radialGradient>
<rect width="{W}" height="{H}" fill="url(#redhaze)"/>
{lines}
{num}
<rect width="{W}" height="{H}" fill="url(#vignette)"/>
<rect x="0" y="{H-260}" width="{W}" height="6" fill="{ROSSO}"/>
<rect x="0" y="{H-250}" width="{W}" height="3" fill="{GIALLO}" opacity="0.9"/>
{text(140, H-180, "CHARLES LECLERC", 64, weight=900, spacing=14)}
{text(W-140, H-180, "SCUDERIA · MARANELLO · MONTE-CARLO", 36, fill="#d6caca", weight=600, anchor="end", spacing=10)}
{monaco_flag(140, 200, 90, 60)}
{text(260, 250, "MONACO", 44, weight=700, spacing=12, fill="#f2ecec")}
{text(W-140, 255, "FORZA CHARLES", 52, fill=ROSSO, weight=900, anchor="end", spacing=8, italic=True)}
'''


# Stylised Monte-Carlo layout (not survey-accurate), clockwise from the start line
MONACO = [
    (510, 1010), (560, 860), (600, 720),                    # pit straight
    (650, 610), (760, 570),                                  # Sainte Devote
    (900, 520), (1060, 450),                                 # Beau Rivage
    (1200, 370), (1330, 300),                                # Massenet
    (1460, 290), (1540, 330),                                # Casino
    (1620, 390), (1690, 450),                                # down to Mirabeau
    (1650, 530), (1560, 600),                                # Mirabeau -> hairpin
    (1500, 650), (1560, 680),                                # Grand Hotel hairpin
    (1660, 680), (1760, 720), (1810, 800),                   # Mirabeau Bas -> Portier
    (1780, 870), (1640, 900), (1460, 905), (1300, 890),      # tunnel
    (1220, 880), (1180, 920), (1130, 905),                   # Nouvelle Chicane
    (1060, 930), (980, 980),                                 # Tabac
    (900, 1010), (860, 1050), (800, 1060),                   # Piscine
    (740, 1070), (700, 1110), (640, 1130),                   # Piscine 2
    (560, 1150), (520, 1120),                                # Rascasse
    (500, 1070),                                             # Anthony Nogues
]

CORNERS = [
    ("SAINTE DÉVOTE", 690, 575, "end", -40, -30), ("BEAU RIVAGE", 960, 470, "end", -20, -30),
    ("MASSENET", 1260, 320, "start", 10, 60), ("CASINO", 1500, 300, "middle", 0, -50),
    ("MIRABEAU", 1690, 450, "start", 40, 0), ("GRAND HOTEL", 1500, 650, "end", -40, 10),
    ("PORTIER", 1810, 800, "start", 40, 10), ("TUNNEL", 1550, 902, "middle", 0, 70),
    ("NOUVELLE CHICANE", 1180, 915, "middle", 0, 75), ("TABAC", 1000, 965, "end", -40, 0),
    ("PISCINE", 800, 1060, "middle", 30, 80), ("RASCASSE", 560, 1150, "middle", 0, 80),
    ("ANTHONY NOGHÈS", 500, 1070, "end", -40, 20),
]


def catmull_rom(points):
    n = len(points)
    d = f"M{points[0][0]},{points[0][1]} "
    for i in range(n):
        p0, p1, p2, p3 = points[i - 1], points[i], points[(i + 1) % n], points[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]} "
    return d + "Z"


def monaco():
    d = catmull_rom(MONACO)
    labels = []
    for name, x, y, anchor, dx, dy in CORNERS:
        labels.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#ffffff"/>')
        labels.append(text(x + dx, y + dy, name, 30, fill="#d6caca", weight=600, anchor=anchor, spacing=4))
    # start/finish chequer across the pit straight
    chequer = "".join(
        f'<rect x="{-30 + c*12}" y="{r*12}" width="12" height="12" fill="{"#fff" if (r + c) % 2 == 0 else "#000"}"/>'
        for r in range(2) for c in range(5))
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#ffffff" stroke-width="1" opacity="0.03"/>'
                   for x in range(0, W, 80))
    grid += "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#ffffff" stroke-width="1" opacity="0.03"/>'
                    for y in range(0, H, 80))
    return f'''
<radialGradient id="sea" cx="62%" cy="85%" r="80%"><stop offset="0" stop-color="#14203a"/><stop offset="0.6" stop-color="#0d0c10"/><stop offset="1" stop-color="#070606"/></radialGradient>
<rect width="{W}" height="{H}" fill="url(#sea)"/>
{grid}
<path d="{d}" fill="none" stroke="{CORSA}" stroke-width="46" stroke-linejoin="round" opacity="0.25" filter="url(#glow)"/>
<path d="{d}" fill="none" stroke="#1d1919" stroke-width="30" stroke-linejoin="round"/>
<path d="{d}" fill="none" stroke="url(#rosso)" stroke-width="16" stroke-linejoin="round" filter="url(#softglow)"/>
<path d="{d}" fill="none" stroke="#ffffff" stroke-width="2" stroke-dasharray="18 22" stroke-linejoin="round" opacity="0.7"/>
<g transform="translate(555,875) rotate(-17)">{chequer}</g>
{"".join(labels)}
<rect width="{W}" height="{H}" fill="url(#vignette)" opacity="0.7"/>
{monaco_flag(160, 200, 120, 80)}
{text(310, 265, "CIRCUIT DE MONACO", 72, weight=900, spacing=10)}
{text(310, 325, "3.337 KM · 78 LAPS · 19 CORNERS", 34, fill="#d6caca", weight=600, spacing=8)}
{text(W-160, H-350, "HOME", 150, fill=ROSSO, weight=900, anchor="end", spacing=6, italic=True, extra='filter="url(#softglow)"')}
{text(W-160, H-280, "LECLERC · WINNER · 26 MAY 2024", 38, fill="#f2ecec", weight=700, anchor="end", spacing=8)}
<rect x="{W-760}" y="{H-250}" width="600" height="5" fill="{GIALLO}"/>
'''


def livery():
    return f'''
<rect width="{W}" height="{H}" fill="url(#carbon)"/>
<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffffff" stop-opacity="0.35"/><stop offset="0.25" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
<path d="M-50,520 C700,360 1500,380 2610,120 L2610,1020 C1700,1180 900,1120 -50,1320 Z" fill="url(#rosso)"/>
<path d="M-50,520 C700,360 1500,380 2610,120 L2610,420 C1600,560 800,560 -50,760 Z" fill="url(#gloss)"/>
<path d="M-50,1320 C900,1120 1700,1180 2610,1020" fill="none" stroke="#ffffff" stroke-width="22"/>
<path d="M-50,1372 C900,1172 1700,1232 2610,1072" fill="none" stroke="{GIALLO}" stroke-width="9"/>
<path d="M-50,488 C700,328 1500,348 2610,88" fill="none" stroke="#ffffff" stroke-width="8" opacity="0.85"/>
<g transform="translate(1900,760) skewX(-12)">
  <circle cx="0" cy="-60" r="250" fill="#ffffff"/>
  <circle cx="0" cy="-60" r="226" fill="none" stroke="#111" stroke-width="6"/>
  {text(0, 70, "16", 360, fill="#111", weight=900, anchor="middle")}
</g>
{text(180, 860, "SCUDERIA", 190, fill="#ffffff", weight=900, spacing=18, italic=True, extra='transform="rotate(-6 180 860)"')}
{text(190, 960, "FERRARI · LECLERC", 64, fill="#ffffff", weight=700, spacing=22, opacity=0.9, extra='transform="rotate(-6 190 960)"')}
<rect width="{W}" height="{H}" fill="url(#vignette)" opacity="0.8"/>
{text(140, H-200, "FORZA FERRARI", 44, fill=ROSSO, weight=900, spacing=12, italic=True)}
{monaco_flag(W-230, H-250, 90, 60)}
'''


VARIANTS = {"sedici": sedici, "monaco": monaco, "livery": livery}

if __name__ == "__main__":
    body = VARIANTS[sys.argv[1]]()
    print(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
          f'<defs>{DEFS}</defs>{body}</svg>')
