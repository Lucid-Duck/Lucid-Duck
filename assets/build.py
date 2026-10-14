import math
import random
from pathlib import Path

OUT = Path(__file__).parent
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

THEMES = {
    "dark": dict(screen="#010409", border="#30363d", fg="#e6edf3", muted="#8b949e",
                 grid="#161b22", grid2="#21262d", trace="#e3b341", accent="#58a6ff",
                 green="#3fb950", hash="#d29922", bar="#161b22"),
    "light": dict(screen="#f6f8fa", border="#d0d7de", fg="#1f2328", muted="#59636e",
                  grid="#eaeef2", grid2="#d8dee4", trace="#9a6700", accent="#0969da",
                  green="#1a7f37", hash="#9a6700", bar="#eaeef2"),
}

TAGLINE = "Linux internals · reverse engineering · vulnerability research"

COMMITS = [
    ("af97bf5a7e72", "wifi: mt76: mt792x: pick the SAR table layout from the table itself"),
    ("5796b2bf9ff7", "wifi: mt76: mt7925: don't put the band auto marker in TGID"),
    ("2b04d6556964", "wifi: mac80211: refuse to make a monitor active when it has no queue"),
    ("7825de3f75d1", "wifi: mt76: mt792x: fix NULL dereference in ACPI SAR init during probe"),
    ("6f6c9800e54c", "wifi: mt76: mt792x: do not advertise active monitor"),
    ("ef3e34874d23", "wifi: mt76: mt7925: ensure tx headroom in usb_sdio_tx_prepare_skb"),
    ("81faf578320d", "wifi: mt76: mt7925: cancel mlo_pm_work on stop"),
    ("ddae0bcb01e7", "wifi: mt76: mt76x02: report rx FCS errors to mac80211"),
    ("81497634d9f8", "wifi: mt76: mt76x02: do not WARN on invalid rx descriptor length"),
    ("7981aca2bd28", "wifi: mt76: restrict NPU/PPE active checks to MMIO devices"),
    ("39afc46c0243", "wifi: mt76: mt7615: drop TXRX_NOTIFY on non-mmio buses"),
    ("feeff151c83e", "wifi: mt76: mt7925: drop TXRX_NOTIFY on non-mmio buses"),
    ("da4082e91aca", "wifi: mt76: mt7921: drop TXRX_NOTIFY on non-mmio buses"),
    ("a7d35545c2ce", "wifi: mt76: mt7921: assert sniffer on chanctx change"),
    ("291b067a02b9", "wifi: mt76: mt7925: add Netgear A8500 USB device ID"),
    ("80119a77e5b0", "wifi: rtw89: usb: fix TX flow control by tracking in-flight URBs"),
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


def terminal(t):
    c = THEMES[t]
    W = 1200
    lh, fs, cw = 25, 15, 9.0
    y0 = 36 + 26
    cmd = "git log --oneline --author=lucid_duck@justthetip.ca origin/master"
    n = len(cmd)
    H = y0 + (len(COMMITS) + 1) * lh + 20
    typed = 0.6 + 2.0
    widths = ";".join(f"{i*cw:.1f}" for i in range(n + 1))
    carets = ";".join(f"{46 + i*cw:.1f}" for i in range(n + 1))

    rows = [f'<text x="28" y="{y0}" font-family="{MONO}" font-size="{fs}" fill="{c["green"]}">$</text>',
            f'<g clip-path="url(#cmd)"><text x="46" y="{y0}" font-family="{MONO}" font-size="{fs}" fill="{c["fg"]}" textLength="{n*cw:.1f}" lengthAdjust="spacingAndGlyphs">{esc(cmd)}</text></g>']
    for i, (h, s) in enumerate(COMMITS, 1):
        y = y0 + i * lh
        b = typed + 0.25 + i * 0.11
        rows.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{b:.2f}s"/>'
                    f'<text x="28" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">'
                    f'<tspan fill="{c["hash"]}">{h}</tspan><tspan fill="{c["fg"]}"> {esc(s)}</tspan></text></g>')
    yl = y0 + (len(COMMITS) + 1) * lh
    bl = typed + 0.25 + (len(COMMITS) + 1) * 0.11
    rows.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{bl:.2f}s"/>'
                f'<text x="28" y="{yl}" font-family="{MONO}" font-size="{fs}" fill="{c["green"]}">$</text>'
                f'<rect x="46" y="{yl-14}" width="9" height="18" fill="{c["fg"]}">{blink(f"{bl:.2f}s")}</rect></g>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="git log of my commits in mainline Linux">
<title>git log of my commits in mainline Linux</title>
<defs><clipPath id="cmd"><rect x="46" y="{y0-18}" height="26" width="0"><animate attributeName="width" begin="0.6s" dur="2.0s" calcMode="discrete" values="{widths}" fill="freeze"/></rect></clipPath></defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{c["screen"]}" stroke="{c["border"]}"/>
<path d="M1 11a10 10 0 0 1 10-10h{W-22}a10 10 0 0 1 10 10v25H1z" fill="{c["bar"]}"/>
<line x1="1" y1="36" x2="{W-1}" y2="36" stroke="{c["border"]}"/>
<circle cx="22" cy="18.5" r="6" fill="#ff5f57"/><circle cx="42" cy="18.5" r="6" fill="#febc2e"/><circle cx="62" cy="18.5" r="6" fill="#28c840"/>
<text x="{W/2:.0f}" y="23" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{c["muted"]}">lucid_duck@bench: ~/src/linux</text>
{"".join(rows)}
<rect x="46" y="{y0-14}" width="9" height="18" fill="{c["fg"]}"><animate attributeName="x" begin="0.6s" dur="2.0s" calcMode="discrete" values="{carets}" fill="freeze"/><set attributeName="opacity" to="0" begin="{typed+0.2:.2f}s"/></rect>
</svg>
'''


for t in THEMES:
    (OUT / f"banner-{t}.svg").write_text(banner(t), encoding="utf-8", newline="\n")
    (OUT / f"terminal-{t}.svg").write_text(terminal(t), encoding="utf-8", newline="\n")
