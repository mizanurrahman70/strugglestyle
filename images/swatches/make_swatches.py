# Generates photo-style fabric swatches for the Swatch Studio (run from the project root, needs Pillow):
#   python images/swatches/make_swatches.py
# Reads each fabric's code and colourways from the SWATCHES list in index.html and writes
#   images/swatches/{code}-{colour}.webp      e.g. ss-d01-indigo.webp (800px, card and loupe)
#   images/swatches/{code}-{colour}-sm.webp   240px, picker and kit tray
# Each fabric's yarn structure is drawn, lit from the top left, given soft folds, then dyed per colourway.
import ast, re
from math import cos, pi, sin
import random
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageMath

OUT = 800        # output size: sharp under the 3x loupe
PAD = 16         # rendered margin, cropped off so lighting offsets never wrap around the edges
N = OUT + 2 * PAD
S = 2            # supersampling for drawn structures
random.seed(7)


def canvas(v=0):
    im = Image.new('L', (N * S, N * S), v)
    return im, ImageDraw.Draw(im)


def finish(im, blur=1.0):
    return im.filter(ImageFilter.GaussianBlur(blur * S)).resize((N, N), Image.LANCZOS)


def fold_map():
    """Long soft diagonal folds, like a swatch that has been handled."""
    n = Image.effect_noise((12, 3), 60).resize((int(N * 1.6), int(N * 1.6)), Image.BICUBIC).rotate(28, resample=Image.BICUBIC)
    c = (n.width - N) // 2
    return n.crop((c, c, c + N, c + N)).filter(ImageFilter.GaussianBlur(12))


def streaks(sigma=40):
    """Thin vertical slubs, as uneven warp yarns give."""
    return Image.effect_noise((N, 5), sigma).resize((N, N), Image.BICUBIC)


def fibre(sigma=30):
    return Image.effect_noise((N, N), sigma).filter(ImageFilter.GaussianBlur(.6))


def mix(a, b, wa):
    """wa/10 of a + the rest of b."""
    return ImageMath.lambda_eval(lambda x: x['convert']((x['a'] * wa + x['b'] * (10 - wa)) / 10, 'L'), a=a, b=b)


# ---- yarn structures: each returns (height, cover); cover 255 = face yarn, 0 = second colour shows

def denim():
    im, d = canvas()
    for k in range(-N * S, 2 * N * S, 7 * S):           # 3x1 right-hand twill lines
        d.line([(k, N * S), (k + N * S / 2, 0)], fill=255, width=5 * S)
    ridges = finish(im, 1.1)
    h = mix(ridges, streaks(), 8)
    cover = ridges.point(lambda v: 95 + v * 160 // 255)  # white weft peeks through between ridges
    return mix(h, fibre(), 8), cover


def stitches(cols=None, w=9, h=7, fill=255):
    """Knit V stitches in wales; `cols` filters which wale indices are knitted."""
    im, d = canvas()
    cw, rh = w * S, h * S
    for i, x in enumerate(range(0, N * S + cw, cw)):
        if cols and not cols(i):
            continue
        for y in range(-rh, N * S + rh, rh):
            for x0 in (x, x + cw):
                d.line([(x0, y), (x + cw / 2, y + rh * 1.35)], fill=fill, width=int(3.4 * S))
    return finish(im, .9)


def jersey():
    return mix(stitches(), fibre(), 8), Image.new('L', (N, N), 255)


def rib():
    knit = stitches(cols=lambda i: i % 4 < 2)
    depth = Image.new('L', (N, 1))
    period = 36
    depth.putdata([int(150 + 105 * cos(2 * pi * (x + 9) / period)) for x in range(N)])
    depth = depth.resize((N, N))
    purl, d = canvas(0)
    for y in range(0, N * S, 5 * S):                      # purl bumps in the recessed wales
        d.line([(0, y), (N * S, y)], fill=110, width=2 * S)
    h = ImageChops.lighter(ImageChops.multiply(knit, depth), ImageChops.multiply(finish(purl, 1), depth))
    return mix(mix(h, depth, 7), fibre(), 8), Image.new('L', (N, N), 255)


def lace():
    im, d = canvas()
    g = 11 * S
    for k in range(-2 * N * S, 3 * N * S, g):             # hexagonal tulle net
        d.line([(k, 0), (k + N * S * .58, N * S)], fill=150, width=int(1.1 * S))
        d.line([(k, 0), (k - N * S * .58, N * S)], fill=150, width=int(1.1 * S))
    for y in range(0, N * S, g):
        d.line([(0, y), (N * S, y)], fill=110, width=S)
    m = 120 * S
    for row, y in enumerate(range(-m, N * S + m, m)):    # flower motifs on a staggered grid
        for x in range(-m + (m // 2 if row % 2 else 0), N * S + m, m):
            for a in range(8):
                ang = a * pi / 4
                cx, cy = x + cos(ang) * 27 * S, y + sin(ang) * 27 * S
                d.ellipse([cx - 14 * S, cy - 14 * S, cx + 14 * S, cy + 14 * S], outline=255, width=int(3.2 * S))
            d.ellipse([x - 11 * S, y - 11 * S, x + 11 * S, y + 11 * S], fill=255)
            d.ellipse([x - 50 * S, y - 50 * S, x + 50 * S, y + 50 * S], outline=235, width=int(2.4 * S))
            for a in range(20):                           # picot dots around the cordonnet
                ang = a * pi / 10
                cx, cy = x + cos(ang) * 57 * S, y + sin(ang) * 57 * S
                d.ellipse([cx - 3 * S, cy - 3 * S, cx + 3 * S, cy + 3 * S], fill=235)
    yarn = finish(im, .7)
    return mix(yarn, fibre(), 8), yarn.point(lambda v: min(255, v * 2))


def terry():
    im, d = canvas()
    g = 6 * S
    for y in range(0, N * S, g):                          # loop-back: a field of small irregular loops
        for x in range(0, N * S, g):
            jx, jy, r = x + random.uniform(-2, 2) * S, y + random.uniform(-2, 2) * S, random.uniform(2.2, 3.3) * S
            d.ellipse([jx - r, jy - r, jx + r, jy + r], outline=255, width=int(1.4 * S))
    loops = finish(im, .8)
    heather = fibre(70).point(lambda v: 255 if v > 150 else 0 if v < 110 else (v - 110) * 255 // 40)
    return mix(loops, fibre(), 7), heather


def poplin():
    im, d = canvas()
    g = 4 * S
    for y in range(0, N * S, g):                          # plain weave: warp and weft alternate over/under
        for x in range(0, N * S, g):
            if (x // g + y // g) % 2:
                d.rectangle([x, y + S // 2, x + g, y + g - S // 2], fill=225)
            else:
                d.rectangle([x + S // 2, y, x + g - S // 2, y + g], fill=200)
    return mix(finish(im, .8), fibre(), 7), Image.new('L', (N, N), 255)


def satin():
    im, d = canvas(128)
    for k in range(-N * S, 2 * N * S, 5 * S):             # long satin floats, barely visible
        d.line([(k, N * S), (k + N * S / 6, 0)], fill=150, width=2 * S)
    return mix(finish(im, 1.2), fibre(12), 8), Image.new('L', (N, N), 255)


def cable():
    purl, d = canvas(40)
    for y in range(0, N * S, 6 * S):                      # moss-stitch background
        for x in range((y // (6 * S)) % 2 * 3 * S, N * S, 6 * S):
            d.ellipse([x, y, x + 4 * S, y + 3 * S], fill=120)
    ropes, d = canvas(0)
    colw, wl, amp, sw = 170 * S, 150 * S, 22 * S, 30 * S
    for cx in range(colw // 2, N * S + colw, colw):
        for side in (-1, 1):                              # knit columns framing each cable
            d.line([(cx + side * 62 * S, 0), (cx + side * 62 * S, N * S)], fill=200, width=10 * S)
        strand = lambda ph, y0, y1: [(cx + sin(2 * pi * y / wl + ph) * amp, y) for y in range(int(y0), int(y1) + S, S)]
        for k in range(-1, N * S // (wl // 2) + 2):      # strands cross; the one on top alternates
            y0, y1 = k * wl / 2, (k + 1) * wl / 2
            for ph in ((0, pi) if k % 2 else (pi, 0)):
                d.line(strand(ph, y0, y1), fill=20, width=sw + 8 * S)
                d.line(strand(ph, y0, y1), fill=255, width=sw)
    ropes = finish(ropes, 2.2)
    knit = stitches(w=7, h=6).point(lambda v: 150 + v * 105 // 255)
    h = ImageChops.lighter(finish(purl, 1.2), ImageChops.multiply(ropes, knit))
    return mix(h, fibre(), 8), Image.new('L', (N, N), 255)


# ---- light and dye

def shade(h, relief, folds, sheen=0):
    """Light from the top left: yarn relief + ambient depth + broad folds + gentle falloff (neutral = 200)."""
    f = fold_map()
    falloff = Image.linear_gradient('L').rotate(-45, expand=False).resize((N, N)).filter(ImageFilter.GaussianBlur(40))
    out = ImageMath.lambda_eval(lambda x: x['convert'](
        200 + (x['h'] - x['hs']) * relief / 10 + (x['h'] - 128) * 3 / 10
        + (x['f'] - x['fs']) * folds / 5 + (x['f'] - 128) * folds / 40 - (x['g'] - 128) / 8, 'L'),
        h=h, hs=ImageChops.offset(h, 1, 1), f=f, fs=ImageChops.offset(f, 6, 6), g=falloff)
    spec = f.point(lambda v: max(0, v - 140) * sheen // 10) if sheen else None
    return out, spec


def rgb(hex_):
    return tuple(int(hex_[i:i + 2], 16) for i in (1, 3, 5))


def dye(h, cover, light, spec, face, back):
    base = Image.composite(Image.new('RGB', (N, N), face), Image.new('RGB', (N, N), back), cover)
    lit = ImageChops.multiply(base, Image.merge('RGB', [light] * 3)).point(lambda v: min(255, v * 255 // 200))
    return ImageChops.screen(lit, Image.merge('RGB', [spec] * 3)) if spec else lit


def lighten(c, t):
    return tuple(int(v + (255 - v) * t) for v in c)


FABRICS = {  # code: (structure, relief, folds, sheen, second colour from (face, backing))
    'SS-D01': (denim, 9, 5, 0, lambda f, b: (231, 226, 214)),
    'SS-J02': (jersey, 7, 6, 0, lambda f, b: f),
    'SS-R03': (rib, 8, 5, 0, lambda f, b: f),
    'SS-L04': (lace, 8, 4, 0, lambda f, b: b),
    'SS-T05': (terry, 7, 6, 0, lambda f, b: lighten(f, .3)),
    'SS-W06': (poplin, 5, 7, 0, lambda f, b: f),
    'SS-S07': (satin, 2, 11, 9, lambda f, b: f),
    'SS-K08': (cable, 12, 3, 0, lambda f, b: f),
}

src = open('index.html', encoding='utf-8').read()
for code, colors in re.findall(r"code: '(SS-\w+)'.*?colors: (\[\[.*?\]\])\}", src, re.S):
    build, relief, folds, sheen, second = FABRICS[code]
    h, cover = build()
    light, spec = shade(h, relief, folds, sheen)
    for c in ast.literal_eval(colors):
        face = rgb(c[1])
        back = rgb(c[2]) if len(c) > 2 else face
        name = re.sub(r'[^a-z0-9]+', '-', c[0].lower())
        im = dye(h, cover, light, spec, face, second(face, back)).crop((PAD, PAD, PAD + OUT, PAD + OUT))
        im.save(f'images/swatches/{code.lower()}-{name}.webp', quality=82, method=6)
        # small copy for the picker and kit tray
        im.resize((240, 240), Image.LANCZOS).save(f'images/swatches/{code.lower()}-{name}-sm.webp', quality=80, method=6)
    print(code, len(ast.literal_eval(colors)), 'colourways')
