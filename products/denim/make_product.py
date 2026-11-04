# Cuts the denim jacket out of the model photo as a product shot on warm white (run from the project root, needs Pillow):
#   python products/denim/make_product.py
#   in : products/denim/model.webp    (1460×1947, the model in the jacket and jeans)
#   out: products/denim/product.webp  (1200×1500, the jacket alone, centred on #F8F7F5)
# The outline (photo pixels) follows the jacket and the V where its fronts part, so the jeans below and the hands
# stay out. Inside it the studio wall and skin are dropped by colour, enclosed gaps are filled, and the hair lying
# over the right shoulder is painted over from the surrounding denim.
import colorsys

from PIL import Image, ImageDraw, ImageFilter

SRC = 'products/denim/model.webp'
OUT = 'products/denim/product.webp'
BG = (248, 247, 245)
SIZE = (1200, 1500)
FILL = .84  # share of the canvas height the jacket takes
SS = 4

JACKET = [
    (667, 300), (760, 318), (850, 362), (874, 480), (880, 730), (892, 880), (930, 975), (874, 985), (867, 880),
    (867, 860), (845, 845), (724, 722), (710, 716), (696, 722), (580, 842), (520, 855),
    (530, 900), (542, 930), (542, 970), (467, 970), (455, 930), (449, 730), (455, 480), (505, 342), (600, 315)]


HAIR_X = 780  # warm pixels right of this are hair over the shoulder; left of it, skin
# Where the hair lies over the jacket (photo pixels): dark hair over the shoulder top, blond hair down the sleeve.
# Anything there that isn't denim blue is repainted from the denim around it.
HAIR = [(760, 280, 845, 385), (838, 280, 884, 645)]
# Mirror the left shoulder into the hidden one: (placket x, squeeze). Right edge 880 maps to the left edge 455.
MIRROR = (700, 245 / 180)


def hsl(r, g, b):
    h, s, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return h, s, .299 * r + .587 * g + .114 * b


def wall(r, g, b):
    """Could be the studio wall: very pale and faintly violet. Sun-faded denim can match it, so only wall-like
    pixels connected to the outside are removed (see below)."""
    h, s, lum = hsl(r, g, b)
    return lum >= 205 and .012 < s < .03 and h > .57


def warm(r, g, b):
    h, s, _ = hsl(r, g, b)
    return h < .16 and s > .18


def blue(r, g, b):
    """Denim blue (not the grey-violet wall, not brown or near-black hair)."""
    h, s, lum = hsl(r, g, b)
    return .40 < h < .64 and s > .04 and lum > 60


def fill_holes(m):
    """Fill every gap the mask fully encloses (anything the outside can't reach)."""
    b = Image.new('L', (m.width + 2, m.height + 2), 0)
    b.paste(m.point(lambda v: 255 if v > 127 else 0), (1, 1))
    ImageDraw.floodfill(b, (0, 0), 128)
    holes = b.point(lambda v: 255 if v == 0 else 0).crop((1, 1, m.width + 1, m.height + 1))
    return Image.composite(Image.new('L', m.size, 255), m, holes)


im = Image.open(SRC).convert('RGB')
outline = Image.new('L', (im.width * SS, im.height * SS), 0)
ImageDraw.Draw(outline).polygon([(x * SS, y * SS) for x, y in JACKET], fill=255)
outline = outline.resize(im.size, Image.LANCZOS)

px, op = im.load(), outline.load()
x0, y0, x1, y1 = outline.getbbox()
# Wall: flood from outside the outline through wall-like pixels, so pale denim enclosed by jacket is never taken
open_ = Image.new('L', (im.width + 2, im.height + 2), 0)
wp = open_.load()
for y in range(im.height):
    for x in range(im.width):
        if op[x, y] < 128 or wall(*px[x, y]):
            wp[x + 1, y + 1] = 255
ImageDraw.floodfill(open_, (0, 0), 128)
outside = open_.crop((1, 1, im.width + 1, im.height + 1)).load()

mask = Image.new('L', im.size, 0)
repaint = Image.new('L', im.size, 0)
mp, rp = mask.load(), repaint.load()
for y in range(y0, y1):
    for x in range(x0, x1):
        if not op[x, y]:
            continue
        c = px[x, y]
        under_hair = any(a <= x < c2 and b <= y < d for a, b, c2, d in HAIR)
        if under_hair and not blue(*c):
            rp[x, y] = 255          # hair (and the wall seen through it): repaint from denim, keep as jacket
            mp[x, y] = op[x, y]
        elif outside[x, y] == 128 or (warm(*c) and x <= HAIR_X):
            continue                # the wall reached from outside, or skin
        else:
            mp[x, y] = op[x, y]
# close stitching and rivet pinholes, fill enclosed gaps, keep the edge soft
mask = fill_holes(mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))).filter(ImageFilter.GaussianBlur(.9))

# Repaint the hair with real denim: mirror the left shoulder and yoke across the button placket (squeezed, as the
# model's turn makes the right side narrower), then match its colour to the more faded denim around the hair.
spot = repaint.filter(ImageFilter.MaxFilter(5))
mirror = im.transform(im.size, Image.AFFINE, (-MIRROR[1], 0, MIRROR[0] * (1 + MIRROR[1]), 0, 1, 0), Image.BICUBIC)
sp, mr = spot.load(), mirror.load()
near = [px[x, y] for y in range(280, 700, 3) for x in range(740, 905, 3)
        if mp[x, y] > 200 and not rp[x, y] and blue(*px[x, y])]
copied = [mr[x, y] for y in range(280, 650, 3) for x in range(740, 905, 3) if sp[x, y]]
gain = [sum(c[i] for c in near) / len(near) / max(1, sum(c[i] for c in copied) / len(copied)) for i in range(3)]
mirror = Image.merge('RGB', [ch.point(lambda v, g=g: min(255, int(v * g))) for ch, g in zip(mirror.split(), gain)])
im = Image.composite(mirror, im, spot.filter(ImageFilter.GaussianBlur(4)))

box = mask.getbbox()
jacket, mask = im.crop(box), mask.crop(box)
scale = SIZE[1] * FILL / jacket.height
size = (round(jacket.width * scale), round(jacket.height * scale))
jacket, mask = jacket.resize(size, Image.LANCZOS), mask.resize(size, Image.LANCZOS)
canvas = Image.new('RGB', SIZE, BG)
canvas.paste(jacket, ((SIZE[0] - size[0]) // 2, (SIZE[1] - size[1]) // 2), mask)
canvas.filter(ImageFilter.UnsharpMask(radius=1, percent=40, threshold=2)).save(OUT, quality=90, method=6)
print('jacket', box, '->', size)
