"""Builds the hand-made animated SVGs for github-profile-v2/assets.
Usage: python scripts/build_assets.py assets"""
import math, pathlib, sys
from xml.sax.saxutils import escape

OUT = pathlib.Path(sys.argv[1])
MONO = "'JetBrains Mono','Fira Code','SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
C = dict(bg0="#0b0a1a", bg1="#1a0f2e", panel="#120f2a", purple="#BF91F3", pink="#FF5FA2",
         mint="#5EF2D6", blue="#70A5FD", text="#E6E1FF", dim="#8B86B3", line="#2a2550")


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------------ hero
def hero():
    W, H, T = 1000, 340, 16.0  # T = typing cycle (s)
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Jyotishman Das: i teach machines to see, hear, and forget">')
    o.append(f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['bg0']}"/><stop offset="1" stop-color="{C['bg1']}"/></linearGradient>
  <radialGradient id="vig" cx="0.5" cy="0.5" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.55"/></radialGradient>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" fill-opacity="0.035"/></pattern>
  <linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{C['mint']}" stop-opacity="0.30"/><stop offset="1" stop-color="{C['mint']}" stop-opacity="0"/></linearGradient>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="bigglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="floorclip"><rect x="0" y="262" width="{W}" height="{H-262}"/></clipPath>""")

    # terminal text lines + typing clips
    lines = [  # (text, kind)  kind: cmd (typed) / out (appears)
        ("$ whoami", "cmd"),
        ("jyotishman das", "out-name"),
        ("$ cat about.txt", "cmd"),
        ("i teach machines to see, hear, and forget.", "out"),
        ("$ ls ~/rabbit-holes", "cmd"),
        ("vision/  audio/  unlearning/  why_is_loss_nan/", "out-blue"),
        ("$ ", "prompt"),
    ]
    starts = [0.5, 1.3, 2.0, 3.2, 4.0, 5.2, 5.8]
    clear = 14.6
    cw, x0, y0, step = 9.7, 58, 92, 26
    for i, ((txt, kind), st) in enumerate(zip(lines, starts)):
        n = len(txt)
        full = 520
        if kind == "cmd":
            vals, keys = [0], [0]
            for k in range(1, n + 1):
                vals.append(k * cw + 4)
                keys.append((st + (k - 1) * 0.07) / T)
            vals[-1] = full
        else:
            vals, keys = [0, full], [0, st / T]
        vals.append(0); keys.append(clear / T)
        o.append(f'  <clipPath id="t{i}"><rect x="{x0-4}" y="{y0+i*step-19}" height="26" width="0">'
                 f'<animate attributeName="width" dur="{fmt(T)}s" repeatCount="indefinite" calcMode="discrete" '
                 f'values="{";".join(fmt(v) for v in vals)}" keyTimes="{";".join(f"{k:.4f}" for k in keys)}"/></rect></clipPath>')
    o.append("</defs>")

    o.append(f'<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>')
    # synthwave floor
    o.append('<g clip-path="url(#floorclip)" opacity="0.9">')
    vx, vy = 500, 240
    for bx in range(-600, 1601, 100):
        o.append(f'<line x1="{vx}" y1="{vy}" x2="{bx}" y2="{H}" stroke="{C["purple"]}" stroke-opacity="0.22" stroke-width="1"/>')
    for k in range(7):
        b = -k * 4.0 / 7
        o.append(f'<line x1="0" x2="{W}" y1="262" y2="262" stroke="{C["pink"]}" stroke-width="1.2" stroke-opacity="0.45">'
                 f'<animate attributeName="y1" values="262;{H}" dur="4s" begin="{fmt(b)}s" repeatCount="indefinite" calcMode="spline" keySplines="0.55 0 1 1" keyTimes="0;1"/>'
                 f'<animate attributeName="y2" values="262;{H}" dur="4s" begin="{fmt(b)}s" repeatCount="indefinite" calcMode="spline" keySplines="0.55 0 1 1" keyTimes="0;1"/></line>')
    o.append(f'<line x1="0" x2="{W}" y1="262" y2="262" stroke="{C["pink"]}" stroke-opacity="0.8" filter="url(#glow)"/>')
    o.append("</g>")

    # corner meta
    o.append(f'<text x="40" y="324" font-family="{MONO}" font-size="12" fill="{C["dim"]}" letter-spacing="1">ahmedabad, in · utc+5:30 · v.2026</text>')

    # terminal window
    o.append('<g>')
    o.append('<animate attributeName="opacity" values="1;1;0.93;1;0.97;1" keyTimes="0;0.86;0.88;0.9;0.93;1" dur="7s" repeatCount="indefinite"/>')
    o.append(f'<rect x="36" y="34" width="540" height="236" rx="12" fill="{C["panel"]}" fill-opacity="0.92" stroke="{C["purple"]}" stroke-opacity="0.55"/>')
    o.append(f'<path d="M36 64 H576" stroke="{C["purple"]}" stroke-opacity="0.35"/>')
    for cx, col in ((58, "#FF5F57"), (78, "#FEBC2E"), (98, "#28C840")):
        o.append(f'<circle cx="{cx}" cy="49" r="6" fill="{col}"/>')
    o.append(f'<text x="306" y="54" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{C["dim"]}">jyotishman@night-shift: ~</text>')
    colors = {"cmd": C["text"], "prompt": C["text"], "out": C["text"], "out-name": C["pink"], "out-blue": C["blue"]}
    for i, (txt, kind) in enumerate(lines):
        y = y0 + i * step
        g = [f'<g clip-path="url(#t{i})" font-family="{MONO}" font-size="16">']
        if txt.startswith("$"):
            g.append(f'<text x="{x0}" y="{y}" fill="{C["mint"]}" xml:space="preserve">$<tspan fill="{colors[kind]}">{escape(txt[1:])}</tspan></text>')
        else:
            weight = ' font-weight="700"' if kind == "out-name" else ""
            filt = ' filter="url(#glow)"' if kind == "out-name" else ""
            g.append(f'<text x="{x0}" y="{y}" fill="{colors[kind]}"{weight}{filt} xml:space="preserve">{escape(txt)}</text>')
        if kind == "prompt":
            g.append(f'<rect x="{x0 + 2*cw}" y="{y-14}" width="9" height="18" fill="{C["mint"]}">'
                     f'<animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>')
        g.append("</g>")
        o.append("".join(g))
    o.append("</g>")

    # hologram
    cx, cy, R = 790, 150, 86
    o.append(f'<polygon points="{cx-30},300 {cx+30},300 {cx+120},64 {cx-120},64" fill="url(#beam)"/>')
    o.append(f'<ellipse cx="{cx}" cy="300" rx="62" ry="11" fill="{C["mint"]}" fill-opacity="0.18" stroke="{C["mint"]}" stroke-opacity="0.7" filter="url(#glow)"/>')
    for k in range(2):
        o.append(f'<ellipse cx="{cx}" cy="300" rx="40" ry="7" fill="none" stroke="{C["mint"]}" stroke-width="1.5">'
                 f'<animate attributeName="rx" values="40;110" dur="3s" begin="{k*1.5}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="ry" values="7;19" dur="3s" begin="{k*1.5}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-opacity" values="0.8;0" dur="3s" begin="{k*1.5}s" repeatCount="indefinite"/></ellipse>')

    import itertools
    verts = [v for v in itertools.product((-1, 1), repeat=4)]
    edges = [(i, j) for i in range(16) for j in range(i + 1, 16) if sum(a != b for a, b in zip(verts[i], verts[j])) == 1]
    N = 60
    def proj(v, a):
        x, y, z, w = v
        x, w = x * math.cos(a) - w * math.sin(a), x * math.sin(a) + w * math.cos(a)        # XW plane
        z, w = z * math.cos(a) - w * math.sin(a), z * math.sin(a) + w * math.cos(a)        # ZW plane
        k = 2.6 / (2.6 - w); x, y, z = x * k, y * k, z * k                                  # 4D -> 3D
        t1, t2 = math.radians(22), math.radians(-28) + a / 2                                # 3D tilt + slow spin
        y, z = y * math.cos(t1) - z * math.sin(t1), y * math.sin(t1) + z * math.cos(t1)
        x, z = x * math.cos(t2) + z * math.sin(t2), -x * math.sin(t2) + z * math.cos(t2)
        m = 5.0 / (5.0 - z)                                                                  # 3D -> 2D
        return x * m, y * m
    frames = [[proj(v, 2 * math.pi * f / N) for v in verts] for f in range(N + 1)]
    ext = max(max(abs(px), abs(py)) for fr in frames for px, py in fr)
    S = 92 / ext
    P = lambda f, i: (cx + S * frames[f][i][0], cy + S * frames[f][i][1])
    def series(i, axis):
        return ";".join(fmt(P(f, i)[axis]) for f in range(N + 1))
    o.append('<defs>'
             '<filter id="tpink"><feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 0.37  0 0 0 0 0.64  0 0 0 1 0"/></filter>'
             '<filter id="tcyan"><feColorMatrix type="matrix" values="0 0 0 0 0.31  0 0 0 0 0.76  0 0 0 0 1  0 0 0 1 0"/></filter>'
             '</defs>')
    tg = ['<g id="tess" fill="none" stroke-width="1.6" stroke-linecap="round">']
    for i, j in edges:
        wi, wj = verts[i][3], verts[j][3]
        col = C["mint"] if wi == wj == -1 else C["pink"] if wi == wj == 1 else "#CFFFF6"
        (x1, y1), (x2, y2) = P(0, i), P(0, j)
        tg.append(f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" stroke="{col}">'
                  f'<animate attributeName="x1" dur="14s" repeatCount="indefinite" values="{series(i,0)}"/>'
                  f'<animate attributeName="y1" dur="14s" repeatCount="indefinite" values="{series(i,1)}"/>'
                  f'<animate attributeName="x2" dur="14s" repeatCount="indefinite" values="{series(j,0)}"/>'
                  f'<animate attributeName="y2" dur="14s" repeatCount="indefinite" values="{series(j,1)}"/></line>')
    for i in range(16):
        x, y = P(0, i)
        tg.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="2.6" fill="#ffffff">'
                  f'<animate attributeName="cx" dur="14s" repeatCount="indefinite" values="{series(i,0)}"/>'
                  f'<animate attributeName="cy" dur="14s" repeatCount="indefinite" values="{series(i,1)}"/></circle>')
    tg.append("</g>")
    o.append('<g>')
    o.append('<animateTransform attributeName="transform" type="translate" values="0 0;0 0;5 0;-4 0;0 0;0 0" keyTimes="0;0.9;0.92;0.94;0.96;1" dur="5s" repeatCount="indefinite"/>')
    o.append('<animate attributeName="opacity" values="0.95;1;0.85;1;0.95" dur="2.3s" repeatCount="indefinite"/>')
    o.append('<g opacity="0.55" filter="url(#tpink)" transform="translate(-2.5 0)"><use href="#tess"/></g>')
    o.append('<g opacity="0.55" filter="url(#tcyan)" transform="translate(2.5 0)"><use href="#tess"/></g>')
    o.append('<g filter="url(#glow)">' + "".join(tg) + "</g>")
    for rot, rx, ry, dur, col in ((-18, 128, 30, 5, C["mint"]), (22, 118, 26, 7, C["pink"])):
        path = f"M{cx-rx},{cy} a{rx},{ry} 0 1,0 {2*rx},0 a{rx},{ry} 0 1,0 {-2*rx},0"
        o.append(f'<g transform="rotate({rot} {cx} {cy})"><path d="{path}" fill="none" stroke="{col}" stroke-opacity="0.3" stroke-dasharray="3 5"/>'
                 f'<circle r="4" fill="{col}" filter="url(#bigglow)"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}"/></circle></g>')
    o.append("</g>")
    import random
    rnd = random.Random(7)
    for k in range(12):
        px = cx + rnd.uniform(-34, 34)
        d = rnd.uniform(3.5, 6)
        b = fmt(rnd.uniform(0, d))
        o.append(f'<circle cx="{fmt(px)}" cy="290" r="{fmt(rnd.uniform(1, 2.2))}" fill="{C["mint"]}" opacity="0">'
                 f'<animate attributeName="cy" values="292;70" dur="{fmt(d)}s" begin="-{b}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cx" values="{fmt(px)};{fmt(cx + (px - cx) * 2.6)}" dur="{fmt(d)}s" begin="-{b}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0.9;0" dur="{fmt(d)}s" begin="-{b}s" repeatCount="indefinite"/></circle>')
    o.append(f'<text x="{cx}" y="44" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{C["mint"]}" letter-spacing="3" filter="url(#glow)">HOLO // 4D TESSERACT</text>')
    o.append(f'<text x="{cx}" y="328" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{C["dim"]}" letter-spacing="1">status: rotating through 4 dimensions<tspan fill="{C["mint"]}">_<animate attributeName="opacity" values="1;0" dur="0.8s" calcMode="discrete" repeatCount="indefinite"/></tspan></text>')

    # CRT overlays
    o.append(f'<rect width="{W}" height="{H}" rx="18" fill="url(#scan)"/>')
    o.append(f'<rect x="0" y="-60" width="{W}" height="60" fill="url(#sweep)"><animateTransform attributeName="transform" type="translate" values="0 0;0 {H+60}" dur="6s" repeatCount="indefinite"/></rect>')
    o.append(f'<rect width="{W}" height="{H}" rx="18" fill="url(#vig)"/>')
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{C["purple"]}" stroke-opacity="0.35"/>')
    o.append("</svg>")
    return "\n".join(o)


# ------------------------------------------------------------------ hud
def hud():
    W, H = 1000, 150
    stats = [
        ("01:17", "peak productivity hour", "the gif is a documentary", C["mint"]),
        ("∞", "arxiv tabs open", "reading list: ambitious", C["pink"]),
        ("NaN", "losses survived", "and counting, somehow", C["blue"]),
        ("3", "things i teach machines", "see · hear · forget", C["purple"]),
    ]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Stats nobody asked for: peak productivity at 01:17, infinite arxiv tabs, NaN losses survived, 3 things i teach machines: see, hear, forget">',
         f"""<defs><linearGradient id="hb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C['bg0']}"/><stop offset="1" stop-color="{C['bg1']}"/></linearGradient>
<linearGradient id="hs" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="{C['mint']}" stop-opacity="0.18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<filter id="g" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="sc" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" fill-opacity="0.03"/></pattern></defs>""",
         f'<rect width="{W}" height="{H}" rx="16" fill="url(#hb)" stroke="{C["purple"]}" stroke-opacity="0.35"/>']
    pw, gap, x = 226, 16, 24
    for i, (num, l1, l2, col) in enumerate(stats):
        px = x + i * (pw + gap)
        b = 0.15 + i * 0.25
        o.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{fmt(b)}s" dur="0.6s" fill="freeze"/>')
        L = 14
        for (ax, ay, sx, sy) in ((px, 22, 1, 1), (px + pw, 22, -1, 1), (px, H - 22, 1, -1), (px + pw, H - 22, -1, -1)):
            o.append(f'<path d="M{ax} {ay + sy*L} V{ay} H{ax + sx*L}" fill="none" stroke="{col}" stroke-width="2" stroke-opacity="0.85"/>')
        big = num == "∞"  # the infinity glyph is tiny in monospace fonts
        o.append(f'<text x="{px + 18}" y="{80 if big else 78}" font-family="{MONO}" font-size="{60 if big else 38}" font-weight="700" fill="{col}" filter="url(#g)">{escape(num)}'
                 f'<animate attributeName="fill-opacity" values="1;0.75;1" dur="{3 + i*0.4}s" repeatCount="indefinite"/></text>')
        o.append(f'<text x="{px + 18}" y="104" font-family="{MONO}" font-size="12.5" fill="{C["text"]}">{escape(l1)}</text>')
        o.append(f'<text x="{px + 18}" y="122" font-family="{MONO}" font-size="12.5" fill="{C["dim"]}">{escape(l2)}</text>')
        if i == 0:
            o.append(f'<circle cx="{px + pw - 22}" cy="40" r="4" fill="{C["mint"]}"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/></circle>'
                     f'<text x="{px + pw - 32}" y="44" text-anchor="end" font-family="{MONO}" font-size="10" fill="{C["mint"]}" letter-spacing="1.5">LIVE</text>')
        o.append("</g>")
    o.append(f'<rect x="-200" y="0" width="200" height="{H}" fill="url(#hs)"><animateTransform attributeName="transform" type="translate" values="0 0;{W+200} 0" dur="5s" repeatCount="indefinite"/></rect>')
    o.append(f'<rect width="{W}" height="{H}" rx="16" fill="url(#sc)"/>')
    o.append("</svg>")
    return "\n".join(o)


# ------------------------------------------------------------------ divider
def divider():
    W, H = 1000, 24
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="">
<defs><linearGradient id="p" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['pink']}" stop-opacity="0"/><stop offset="0.5" stop-color="{C['mint']}"/><stop offset="1" stop-color="{C['pink']}" stop-opacity="0"/></linearGradient>
<filter id="g" x="-10%" y="-200%" width="120%" height="500%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<line x1="0" y1="12" x2="{W}" y2="12" stroke="{C['purple']}" stroke-opacity="0.35" stroke-dasharray="2 6"/>
<rect x="-160" y="10.5" width="160" height="3" rx="1.5" fill="url(#p)" filter="url(#g)"><animateTransform attributeName="transform" type="translate" values="0 0;{W+160} 0" dur="3.5s" repeatCount="indefinite"/></rect>
<rect x="{W/2-5}" y="7" width="10" height="10" transform="rotate(45 {W/2} 12)" fill="{C['bg0']}" stroke="{C['mint']}"/>
</svg>"""


# ------------------------------------------------------------------ cards
CARDS = [
    ("qpaudioeraser", "QPAudioEraser", "speech unlearning · demo",
     ["makes a model forget your voice,", "without forgetting how to listen."],
     ["unlearning", "voice biometrics", "demo"], C["mint"]),
    ("hallucidetect", "HalluciDetect", "llm evaluation",
     ["catches llms making things up.", "with receipts: embeddings + fact-checks."],
     ["flask", "sentence-transformers", "plotly"], C["pink"]),
    ("personvlm", "PersonVLM", "vision-language · tiny",
     ["a vlm small enough to fit in your pocket.", "describes people in ~25 ms. no vibes, just facts."],
     ["mobilevit", "distilgpt-2", "pytorch"], C["blue"]),
    ("aerial-guardian", "The Aerial Guardian", "tracking from the sky",
     ["finds tiny humans in drone footage.", "190+ fps. hide and seek is cancelled."],
     ["yolov8", "bytetrack", "visdrone"], C["purple"]),
    ("swift-llm", "swift-llm", "llm inference",
     ["llm calls, but cheaper and faster.", "asked before? already cached. 74% of the time."],
     ["faiss", "groq", "openai"], C["mint"]),
    ("tradl", "Tradl AI", "hackathon winner · agents",
     ["agents that read the news", "so traders don't have to. (we won.)"],
     ["langgraph", "agents", "nlp"], C["pink"]),
]


def card(i, slug, title, label, desc, tags, col):
    W, H = 480, 168
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(title)}: {escape(" ".join(desc))}">',
         f"""<defs><linearGradient id="bd" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">
<stop offset="0" stop-color="{C['pink']}"/><stop offset="0.35" stop-color="{C['purple']}"/><stop offset="0.65" stop-color="{C['mint']}"/><stop offset="1" stop-color="{C['blue']}"/>
<animateTransform attributeName="gradientTransform" type="rotate" values="0 {W/2} {H/2};360 {W/2} {H/2}" dur="6s" begin="-{i}s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="cb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C['bg0']}"/><stop offset="1" stop-color="{C['bg1']}"/></linearGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="cl"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14"/></clipPath>
<filter id="g" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>""",
         f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="url(#cb)"/>',
         f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="none" stroke="url(#bd)" stroke-width="2.2"/>',
         f'<g clip-path="url(#cl)"><rect x="-200" y="0" width="160" height="{H}" fill="url(#sh)" transform="skewX(-20)"><animateTransform attributeName="transform" type="translate" values="0 0;{W+400} 0" dur="7s" begin="{1.2*i}s" repeatCount="indefinite"/></rect></g>',
         f'<circle cx="26" cy="30" r="4" fill="{col}"><animate attributeName="opacity" values="1;0.25;1" dur="2s" begin="-{0.3*i}s" repeatCount="indefinite"/></circle>',
         f'<text x="38" y="34" font-family="{MONO}" font-size="11.5" fill="{col}" letter-spacing="1.2">{escape(label)}</text>',
         f'<text x="{W-24}" y="36" text-anchor="end" font-family="{MONO}" font-size="18" fill="{C["dim"]}">↗</text>',
         f'<text x="22" y="66" font-family="{MONO}" font-size="21" font-weight="700" fill="{C["text"]}" filter="url(#g)">{escape(title)}</text>']
    for k, ln in enumerate(desc):
        o.append(f'<text x="22" y="{92 + k*19}" font-family="{MONO}" font-size="13" fill="#B9B3E0">{escape(ln)}</text>')
    x = 22
    for t in tags:
        w = len(t) * 7.4 + 18
        o.append(f'<rect x="{fmt(x)}" y="{H-36}" width="{fmt(w)}" height="22" rx="11" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-opacity="0.55"/>'
                 f'<text x="{fmt(x + w/2)}" y="{H-21}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{col}">{escape(t)}</text>')
        x += w + 8
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "hero.svg").write_text(hero())
(OUT / "hud.svg").write_text(hud())
(OUT / "divider.svg").write_text(divider())
(OUT / "cards").mkdir(exist_ok=True)
for i, c in enumerate(CARDS):
    (OUT / "cards" / f"{c[0]}.svg").write_text(card(i, *c))
print("built", sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*.svg")))
