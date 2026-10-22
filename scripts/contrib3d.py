"""Render the last year of GitHub contributions as an animated isometric 3D "city".

Reads the public contribution calendar (no token needed) and writes a self-contained SVG.
Usage: python scripts/contrib3d.py <github-user> <output.svg> [calendar.html]
"""
import datetime as dt
import math
import re
import sys
import urllib.request

MONO = "'JetBrains Mono','Fira Code','SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
LEVEL_COLORS = {1: (94, 242, 214), 2: (112, 165, 253), 3: (191, 145, 243), 4: (255, 95, 162)}


def fetch(user):
    req = urllib.request.Request(f"https://github.com/users/{user}/contributions",
                                 headers={"User-Agent": "contrib3d (github profile readme)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def parse(html):
    days = []
    for tag in re.findall(r"<td[^>]*data-date=[^>]*>", html):
        date = re.search(r'data-date="([\d-]+)"', tag).group(1)
        level = int(re.search(r'data-level="(\d)"', tag).group(1))
        cid = re.search(r'id="([^"]+)"', tag).group(1)
        days.append([date, level, cid, 0])
    tips = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html))
    for d in days:
        m = re.match(r"(\d+) contribution", tips.get(d[2], ""))
        d[3] = int(m.group(1)) if m else 0
    if not days:
        raise SystemExit("no contribution cells found: GitHub may have changed the calendar markup")
    return sorted(days)


def shade(rgb, f):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * f))) for c in rgb)


def render(days, user):
    first = dt.date.fromisoformat(days[0][0])
    start = first - dt.timedelta(days=(first.weekday() + 1) % 7)  # back to Sunday
    cells = []
    for date, level, _, count in days:
        d = dt.date.fromisoformat(date)
        week, dow = (d - start).days // 7, (d.weekday() + 1) % 7
        cells.append((week, dow, level, count, d))
    weeks = max(c[0] for c in cells) + 1
    total = sum(c[3] for c in cells)
    peak = max(cells, key=lambda c: c[3])
    active = sum(1 for c in cells if c[3] > 0)

    W, H = 1000, 470
    s = 12.0
    # oblique projection: weeks run along a shallow axis, weekdays along a short steep one
    U = (13.2, 3.4)   # one week step
    V = (-7.0, 6.2)   # one weekday step
    xs = [w * U[0] + d * V[0] for w in (0, weeks) for d in (0, 7)]
    ys = [w * U[1] + d * V[1] for w in (0, weeks) for d in (0, 7)]
    x0 = W / 2 - (min(xs) + max(xs)) / 2
    y0 = (H + 140) / 2 - (min(ys) + max(ys)) / 2 + 10
    maxc = max(1, peak[3])

    def pt(x, y):
        return f"{x:.1f},{y:.1f}"

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
           f'aria-label="{total} GitHub contributions in the last year, drawn as a 3D city">',
           f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0a1a"/><stop offset="1" stop-color="#1a0f2e"/></linearGradient>
<radialGradient id="pool" cx="0.5" cy="0.62" r="0.5"><stop offset="0" stop-color="#5EF2D6" stop-opacity="0.16"/><stop offset="1" stop-color="#5EF2D6" stop-opacity="0"/></radialGradient>
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset="0.5" stop-color="#5EF2D6" stop-opacity="0.13"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" fill-opacity="0.03"/></pattern>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>""",
           f'<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>',
           f'<rect width="{W}" height="{H}" rx="18" fill="url(#pool)"/>',
           f'<text x="32" y="44" font-family="{MONO}" font-size="13" fill="#5EF2D6" letter-spacing="2">// COMMIT CITY</text>',
           f'<text x="32" y="74" font-family="{MONO}" font-size="24" font-weight="700" fill="#E6E1FF">{total} contributions</text>',
           f'<text x="32" y="98" font-family="{MONO}" font-size="13" fill="#8B86B3">last 12 months · {active} active days · peak {peak[3]} on {peak[4]:%b %d}</text>',
           f'<text x="{W-32}" y="44" text-anchor="end" font-family="{MONO}" font-size="12" fill="#8B86B3">@{user} · updated {dt.date.today():%Y-%m-%d}</text>',
           '<g>',
           '<animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="6s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" keyTimes="0;0.5;1"/>']

    g = 0.14  # gap between tiles, as a fraction of a cell
    def corner(week, dow, a, b):
        return (x0 + (week + a) * U[0] + (dow + b) * V[0], y0 + (week + a) * U[1] + (dow + b) * V[1])

    # back-to-front: smaller screen depth first
    for week, dow, level, count, d in sorted(cells, key=lambda c: (c[0] * U[1] + c[1] * V[1], c[0])):
        p0, p1 = corner(week, dow, g, g), corner(week, dow, 1 - g, g)
        p2, p3 = corner(week, dow, 1 - g, 1 - g), corner(week, dow, g, 1 - g)
        if count == 0:
            out.append(f'<polygon points="{pt(*p0)} {pt(*p1)} {pt(*p2)} {pt(*p3)}" fill="#15122b" stroke="#2a2550" stroke-width="0.6"/>')
            continue
        h = 6 + 64 * math.sqrt(count / maxc)
        rgb = LEVEL_COLORS.get(level, LEVEL_COLORS[1])
        up = lambda p: (p[0], p[1] - h)
        begin = 0.25 + week * 0.035
        out.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="0.5s" fill="freeze"/>'
                   + ('<g filter="url(#glow)">' if count == peak[3] else "<g>")
                   # front face (along the week axis) and right face (along the weekday axis), then the roof
                   + f'<polygon points="{pt(*p3)} {pt(*p2)} {pt(*up(p2))} {pt(*up(p3))}" fill="{shade(rgb, 0.55)}"/>'
                   f'<polygon points="{pt(*p1)} {pt(*p2)} {pt(*up(p2))} {pt(*up(p1))}" fill="{shade(rgb, 0.38)}"/>'
                   f'<polygon points="{pt(*up(p0))} {pt(*up(p1))} {pt(*up(p2))} {pt(*up(p3))}" fill="{shade(rgb, 1.0)}"/>'
                   f'</g></g>')
    out.append("</g>")
    out.append(f'<rect x="-260" y="0" width="260" height="{H}" fill="url(#sweep)"><animateTransform attributeName="transform" type="translate" values="0 0;{W+260} 0" dur="6s" repeatCount="indefinite"/></rect>')
    lx = W - 32 - 5 * 18 - 40
    out.append(f'<text x="{lx - 8}" y="{H-26}" text-anchor="end" font-family="{MONO}" font-size="11" fill="#8B86B3">less</text>')
    out.append(f'<rect x="{lx}" y="{H-36}" width="12" height="12" rx="2" fill="#15122b" stroke="#2a2550"/>')
    for i, (lv, rgb) in enumerate(sorted(LEVEL_COLORS.items()), 1):
        out.append(f'<rect x="{lx + i*18}" y="{H-36}" width="12" height="12" rx="2" fill="{shade(rgb, 1)}"/>')
    out.append(f'<text x="{lx + 5*18 + 2}" y="{H-26}" font-family="{MONO}" font-size="11" fill="#8B86B3">more</text>')
    out.append(f'<rect width="{W}" height="{H}" rx="18" fill="url(#scan)"/>')
    out.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="#BF91F3" stroke-opacity="0.35"/>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    user, path = sys.argv[1], sys.argv[2]
    html = open(sys.argv[3]).read() if len(sys.argv) > 3 else fetch(user)
    svg = render(parse(html), user)
    with open(path, "w") as f:
        f.write(svg)
    print(f"wrote {path} ({len(svg)//1024} KB)")
