import math
import random
from pathlib import Path

OUT = Path(__file__).parent
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(screen="#010409", border="#30363d", muted="#8b949e", grid="#161b22", grid2="#21262d",
                 trace="#e3b341", accent="#58a6ff"),
    "light": dict(screen="#f6f8fa", border="#d0d7de", muted="#59636e", grid="#eaeef2", grid2="#d8dee4",
                  trace="#9a6700", accent="#0969da"),
}

DOTS = {"green": "#2da44e", "blue": "#218bff", "amber": "#d4a72c", "purple": "#a475f9", "cyan": "#1b9aaa", "pink": "#e85aad"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&#39;")


def trace(seed, xs, floor, peaks, jitter):
    rnd = random.Random(seed)
    pts = []
    for x in xs:
        y = floor + 4 * math.sin(x / 97.0) + rnd.gauss(0, 2.6)
        for xc, amp in peaks:
            a = amp + rnd.uniform(-jitter, jitter)
            y -= a * math.exp(-((x - xc) / 4.5) ** 2) + 0.16 * a * math.exp(-((x - xc) / 26) ** 2)
        pts.append((x, y))
    return pts


def fmt(pts):
    return " ".join(f"{x:.0f},{y:.1f}" for x, y in pts)


def banner(t):
    c = THEMES[t]
    W, H = 1200, 240
    px0, px1, py0, py1 = 40, 1160, 34, 196
    span = px1 - px0
    floor = 180
    peaks = [(px0 + span * 0.20, 96), (px0 + span * (0.20 + 66.01 / 100), 88)]
    xs = list(range(px0, px1 + 1, 3))
    frames = [fmt(trace(s, xs, floor, peaks, 4)) for s in range(1, 7)]
    runs = [trace(100 + s, xs, floor, peaks, 4) for s in range(14)]
    hold = [(x, min(r[i][1] for r in runs)) for i, x in enumerate(xs)]

    grid = []
    for i in range(11):
        x = px0 + span * i / 10
        g = c["grid2"] if i in (0, 10) else c["grid"]
        grid.append(f'<line x1="{x:.1f}" y1="{py0}" x2="{x:.1f}" y2="{py1}" stroke="{g}"/>')
    for j in range(9):
        y = py0 + (py1 - py0) * j / 8
        g = c["grid2"] if j in (0, 8) else c["grid"]
        grid.append(f'<line x1="{px0}" y1="{y:.1f}" x2="{px1}" y2="{y:.1f}" stroke="{g}"/>')

    marks = []
    for k, (xc, amp) in enumerate(peaks, 1):
        top = floor - amp * 1.16 - 10
        marks.append(f'<polygon points="{xc-6:.1f},{top-12:.1f} {xc+6:.1f},{top-12:.1f} {xc:.1f},{top-1:.1f}" fill="{c["accent"]}"/>')
        marks.append(f'<text x="{xc:.1f}" y="{top-17:.1f}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{c["accent"]}">{k}</text>')

    glow = ""
    gref = ""
    if t == "dark":
        glow = ('<filter id="g" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur stdDeviation="2.2" result="b"/>'
                '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
        gref = ' filter="url(#g)"'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="tinySA Ultra+ spectrum analyzer screen with two carriers 66.01 MHz apart">
<title>tinySA Ultra+ spectrum analyzer screen with two carriers 66.01 MHz apart</title>
<defs>{glow}</defs>
<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="14" fill="{c["screen"]}" stroke="{c["border"]}"/>
{"".join(grid)}
<polyline points="{fmt(hold)}" fill="none" stroke="{c["trace"]}" stroke-opacity="0.28" stroke-width="1.2"/>
<polyline fill="none" stroke="{c["trace"]}" stroke-width="1.8" stroke-linejoin="round"{gref} points="{frames[0]}"><animate attributeName="points" dur="0.9s" repeatCount="indefinite" calcMode="discrete" values="{";".join(frames)}"/></polyline>
{"".join(marks)}
<rect x="{px0}" y="{py0}" width="2" height="{py1-py0}" fill="{c["accent"]}" opacity="0.22"><animate attributeName="x" from="{px0}" to="{px1}" dur="2.6s" repeatCount="indefinite"/></rect>
<text x="{px0+16}" y="{py0+24}" font-family="{MONO}" font-size="15" fill="{c["accent"]}">\u0394Mkr2  66.01 MHz</text>
<text x="{px0}" y="{H-24}" font-family="{MONO}" font-size="13" fill="{c["muted"]}">tinySA Ultra+</text>
<text x="{px1}" y="{H-24}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{c["muted"]}">SPAN 100 MHz</text>
</svg>
'''


def dot(color, delay):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">
<circle cx="12" cy="12" r="5" fill="{color}"/>
<circle cx="12" cy="12" r="5" fill="none" stroke="{color}" stroke-width="1.6"><animate attributeName="r" values="5;11" dur="2.4s" begin="{delay:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0" dur="2.4s" begin="{delay:.1f}s" repeatCount="indefinite"/></circle>
</svg>
'''


for t in THEMES:
    (OUT / f"banner-{t}.svg").write_text(banner(t), encoding="utf-8", newline="\n")
for i, (name, color) in enumerate(DOTS.items()):
    (OUT / f"dot-{name}.svg").write_text(dot(color, i * 0.4), encoding="utf-8", newline="\n")
