import math
import random
from pathlib import Path

OUT = Path(__file__).parent
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

THEMES = {
    "dark": dict(screen="#010409", card="#0d1117", border="#30363d", fg="#e6edf3", muted="#8b949e",
                 grid="#161b22", grid2="#21262d", trace="#e3b341", accent="#58a6ff", green="#3fb950",
                 green_c="#3fb950", blue_c="#58a6ff", amber_c="#e3b341", purple_c="#bc8cff",
                 pink_c="#f778ba", cyan_c="#39c5cf"),
    "light": dict(screen="#f6f8fa", card="#ffffff", border="#d0d7de", fg="#1f2328", muted="#59636e",
                  grid="#eaeef2", grid2="#d8dee4", trace="#9a6700", accent="#0969da", green="#1a7f37",
                  green_c="#1a7f37", blue_c="#0969da", amber_c="#9a6700", purple_c="#8250df",
                  pink_c="#bf3989", cyan_c="#1b7c83"),
}

TAGLINE = "Linux internals · reverse engineering · vulnerability research"

CARDS = [
    ("linus", "green_c", "Applied by Linus Torvalds",
     ("My mt792x ACPI SAR crash fix, pulled", "straight off the list into mainline."), "7825de3f75d1 · MAINLINE"),
    ("cisco", "blue_c", "CVE-2026-20161",
     ("Cisco ThousandEyes agent: any local user", "could overwrite any file on the box."), "CREDITED BY CISCO PSIRT"),
    ("mainline", "amber_c", "18 patches in mainline",
     ("mt76, rtw89 and mac80211, with 14 more", "queued for the 7.4 merge window."), "LINUX-WIRELESS PATCHWORK"),
    ("cves", "purple_c", "7 kernel CVEs",
     ("Assigned to fixes I wrote. Two of them", "are backported all the way to 5.10."), "LINUX KERNEL CNA"),
    ("aic8800", "cyan_c", "My own firmware, on air",
     ("AIC8800 clean-room: two carriers commanded", "66 MHz apart landed 66.01 MHz apart."), "CLEAN-ROOM · IN PROGRESS"),
    ("hire", "pink_c", "Available for contracts",
     ("Linux drivers, firmware and protocol RE,", "vulnerability research. Remote."), "LUCID_DUCK@JUSTTHETIP.CA"),
]


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


def blink(begin):
    return (f'<animate attributeName="opacity" begin="{begin}" dur="1.1s" values="1;1;0;0" '
            f'keyTimes="0;0.5;0.5;1" calcMode="discrete" repeatCount="indefinite"/>')


def banner(t):
    c = THEMES[t]
    W, H = 1200, 300
    px0, px1, py0, py1 = 40, 1160, 40, 250
    span = px1 - px0
    floor = 236
    peaks = [(px0 + span * 0.20, 47), (px0 + span * (0.20 + 66.01 / 100), 43)]
    xs = list(range(px0, px1 + 1, 3))
    frames = [fmt(trace(s, xs, floor, peaks, 3)) for s in range(1, 7)]
    runs = [trace(100 + s, xs, floor, peaks, 3) for s in range(14)]
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

    n = len(TAGLINE)
    cw = 11.4
    widths = ";".join(f"{i*cw:.1f}" for i in range(n + 1))
    carets = ";".join(f"{62 + i*cw:.1f}" for i in range(n + 1))
    glow = ""
    gref = ""
    if t == "dark":
        glow = ('<filter id="g" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur stdDeviation="2.2" result="b"/>'
                '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
        gref = ' filter="url(#g)"'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Lucid Duck: {esc(TAGLINE)}">
<title>Lucid Duck: {esc(TAGLINE)}</title>
<defs>{glow}<clipPath id="tl"><rect x="60" y="112" height="30" width="0"><animate attributeName="width" begin="0.4s" dur="2.4s" calcMode="discrete" values="{widths}" fill="freeze"/></rect></clipPath></defs>
<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="14" fill="{c["screen"]}" stroke="{c["border"]}"/>
{"".join(grid)}
<polyline points="{fmt(hold)}" fill="none" stroke="{c["trace"]}" stroke-opacity="0.28" stroke-width="1.2"/>
<polyline fill="none" stroke="{c["trace"]}" stroke-width="1.8" stroke-linejoin="round"{gref} points="{frames[0]}"><animate attributeName="points" dur="0.9s" repeatCount="indefinite" calcMode="discrete" values="{";".join(frames)}"/></polyline>
{"".join(marks)}
<rect x="{px0}" y="{py0}" width="2" height="{py1-py0}" fill="{c["accent"]}" opacity="0.22"><animate attributeName="x" from="{px0}" to="{px1}" dur="2.6s" repeatCount="indefinite"/></rect>
<text x="60" y="96" font-family="{SANS}" font-size="56" font-weight="700" fill="{c["fg"]}">Lucid Duck</text>
<g clip-path="url(#tl)"><text x="62" y="134" font-family="{MONO}" font-size="19" fill="{c["muted"]}" textLength="{n*cw:.1f}" lengthAdjust="spacingAndGlyphs">{esc(TAGLINE)}</text></g>
<rect x="62" y="117" width="10" height="22" fill="{c["green"]}"><animate attributeName="x" begin="0.4s" dur="2.4s" calcMode="discrete" values="{carets}" fill="freeze"/>{blink("2.8s")}</rect>
<text x="1140" y="62" text-anchor="end" font-family="{MONO}" font-size="15" fill="{c["accent"]}">ΔMkr2  66.01 MHz</text>
<text x="{px0}" y="272" font-family="{MONO}" font-size="13" fill="{c["muted"]}">tinySA Ultra+</text>
<text x="{px1}" y="272" text-anchor="end" font-family="{MONO}" font-size="13" fill="{c["muted"]}">SPAN 100 MHz</text>
</svg>
'''


def card(t, color, title, sub, tag, delay):
    c = THEMES[t]
    a = c[color]
    W, H = 600, 190
    label = esc(f"{title}. {' '.join(sub)}")
    lines = "".join(f'<text x="40" y="{100 + i*28}" font-family="{SANS}" font-size="19" fill="{c["muted"]}">{esc(s)}</text>'
                    for i, s in enumerate(sub))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">
<title>{label}</title>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{c["card"]}" stroke="{c["border"]}"/>
<path d="M1 13a12 12 0 0 1 12-12h5v{H-2}h-5a12 12 0 0 1-12-12z" fill="{a}"/>
<circle cx="40" cy="49" r="6" fill="{a}"/>
<circle cx="40" cy="49" r="6" fill="none" stroke="{a}" stroke-width="2"><animate attributeName="r" values="6;16" dur="2.4s" begin="{delay:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0" dur="2.4s" begin="{delay:.1f}s" repeatCount="indefinite"/></circle>
<text x="62" y="58" font-family="{SANS}" font-size="27" font-weight="700" fill="{c["fg"]}">{esc(title)}</text>
<text x="{W-26}" y="52" text-anchor="end" font-family="{SANS}" font-size="22" fill="{c["muted"]}">↗</text>
{lines}
<text x="40" y="166" font-family="{MONO}" font-size="14" letter-spacing="0.5" fill="{a}">{esc(tag)}</text>
</svg>
'''


for t in THEMES:
    (OUT / f"banner-{t}.svg").write_text(banner(t), encoding="utf-8", newline="\n")
    for i, (name, color, title, sub, tag) in enumerate(CARDS):
        (OUT / f"card-{name}-{t}.svg").write_text(card(t, color, title, sub, tag, i * 0.4), encoding="utf-8", newline="\n")
