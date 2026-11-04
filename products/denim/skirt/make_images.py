# Builds the gallery images for the denim page's second variant (rib vest & maxi skirt) from its model photo.
# Run from the project root (needs Pillow):  python products/denim/skirt/make_images.py
#   in : products/denim/skirt/model.webp   (1460×1947)
#   out: products/denim/skirt/{name}.webp  (4:5 crops) and product.webp (the vest cut out on warm white)
# Boxes are (left, top, width, height) in photo pixels; small crops are enlarged with Lanczos and a light sharpen.
import colorsys

from PIL import Image, ImageDraw, ImageFilter

DIR = 'products/denim/skirt/'
MAX_H = 1500
CROPS = {
    'half':   (340, 30, 700, 875),     # head to hip
    'vest':   (520, 300, 380, 475),    # rib knit, zip, flap pocket
    'skirt':  (300, 760, 740, 925),    # the maxi skirt, waist to hem
    'belt':   (540, 760, 320, 400),    # western belt buckle, waistband and pockets
    'hem':    (470, 1440, 400, 500),   # raw hem and denim mules
    'panels': (470, 1050, 400, 500),   # seamed panels and the vintage wash
}

# The vest for the product shot: outline in photo pixels; inside it, denim blue is kept and arms, hair and wall dropped
VEST = [(680, 310), (752, 312), (754, 358), (800, 428), (852, 458), (858, 600), (850, 650), (843, 738),
        (700, 742), (560, 740), (527, 736), (527, 690), (540, 620), (555, 560), (565, 500), (570, 450), (585, 410),
        (600, 378), (678, 372)]
BG, SIZE, FILL, SS = (248, 247, 245), (1200, 1500), .7, 4
# Hair covers the right yoke, so the outline cuts below it on a clean diagonal; nothing is repainted
HAIR = (0, 0, 0, 0)


def denim(r, g, b):
    h, s, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    lum = .299 * r + .587 * g + .114 * b
    hair = h < .16 and s > .2
    return (.5 < h < .72 and s > .12) or (lum < 45 and not hair)


def fill_holes(m):
    """Fill every gap the mask fully encloses (the brass zip, the pocket snap)."""
    b = Image.new('L', (m.width + 2, m.height + 2), 0)
    b.paste(m.point(lambda v: 255 if v > 127 else 0), (1, 1))
    ImageDraw.floodfill(b, (0, 0), 128)
    holes = b.point(lambda v: 255 if v == 0 else 0).crop((1, 1, m.width + 1, m.height + 1))
    return Image.composite(Image.new('L', m.size, 255), m, holes)


im = Image.open(DIR + 'model.webp').convert('RGB')
for name, (x, y, w, h) in CROPS.items():
    c = im.crop((x, y, x + w, y + h))
    target = min(MAX_H, h * 2)
    if target > h:
        c = c.resize((round(w * target / h), target), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    c.save(DIR + f'{name}.webp', quality=86, method=6)
    print(name, c.size)

outline = Image.new('L', (im.width * SS, im.height * SS), 0)
ImageDraw.Draw(outline).polygon([(x * SS, y * SS) for x, y in VEST], fill=255)
outline = outline.resize(im.size, Image.LANCZOS)
px, op = im.load(), outline.load()
mask = Image.new('L', im.size, 0)
repaint = Image.new('L', im.size, 0)
mp, rp = mask.load(), repaint.load()
x0, y0, x1, y1 = outline.getbbox()
for y in range(y0, y1):
    for x in range(x0, x1):
        if not op[x, y]:
            continue
        if HAIR[0] <= x < HAIR[2] and HAIR[1] <= y < HAIR[3]:
            mp[x, y] = op[x, y]
            if not denim(*px[x, y]) or .299 * px[x, y][0] + .587 * px[x, y][1] + .114 * px[x, y][2] > 120:
                rp[x, y] = 255
        elif denim(*px[x, y]):
            mp[x, y] = op[x, y]
mask = fill_holes(mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))).filter(ImageFilter.GaussianBlur(.9))
# Repaint the hair: start at the average of the plain right panel, diffuse the denim around in, add a little grain
spot = repaint.filter(ImageFilter.MaxFilter(7))
unknown = Image.composite(Image.new('L', im.size, 255), spot, mask.point(lambda v: 255 if v < 64 else 0))
near = [px[x, y] for y in range(440, 640, 3) for x in range(770, 840, 3)]
avg = tuple(sum(c[i] for c in near) // len(near) for i in range(3))
filled = Image.composite(Image.new('RGB', im.size, avg), im, unknown)
for radius in (8, 4, 2):
    for _ in range(20):
        filled = Image.composite(filled.filter(ImageFilter.GaussianBlur(radius)), im, unknown)
grain = Image.merge('RGB', [Image.effect_noise(im.size, 22)] * 3)
filled = Image.blend(filled, Image.blend(filled, grain, .5), .1)
im = Image.composite(filled, im, spot.filter(ImageFilter.GaussianBlur(1.5)))
box = mask.getbbox()
vest, mask = im.crop(box), mask.crop(box)
scale = SIZE[1] * FILL / vest.height
size = (round(vest.width * scale), round(vest.height * scale))
vest, mask = vest.resize(size, Image.LANCZOS), mask.resize(size, Image.LANCZOS)
canvas = Image.new('RGB', SIZE, BG)
canvas.paste(vest, ((SIZE[0] - size[0]) // 2, (SIZE[1] - size[1]) // 2), mask)
canvas.filter(ImageFilter.UnsharpMask(radius=1, percent=40, threshold=2)).save(DIR + 'product.webp', quality=90, method=6)
print('product', box, '->', size)
