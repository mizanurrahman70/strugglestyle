# Builds every outfit image from the white single-garment renders + fabric swatches.
# Run from the project root (needs Pillow):  python outfits/compose_outfits.py
#   in : outfits/garments/{id}.webp   (same avatar, same pose, one white garment each, transparent bg)
#        outfits/fabrics/{id}.webp    (draped swatch icon)
#   out: outfits/{first}-{second}-{fabric}.webp
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageMath, ImageStat

FULL, TOPS, BOTTOMS = ['dress'], ['shirt', 'blazer', 'tee'], ['pants', 'skirt']
FABRICS = {'denim': 4, 'jersey': 2, 'silk': 1}  # fabric id: weave strength (0-10)


def garment_mask(im):
    """Soft mask of the white/grey garment pixels (the wooden avatar is saturated orange)."""
    s = im.convert('RGB').convert('HSV').getchannel('S')
    m = s.point(lambda v: 255 if v < 22 else 0 if v > 46 else int(255 * (46 - v) / 24))
    # grow by a pixel so the garment's grey anti-aliased edge is dyed too
    return ImageChops.multiply(m.filter(ImageFilter.MaxFilter(3)), im.getchannel('A')).filter(ImageFilter.GaussianBlur(.6))


def fabric_tone(fab):
    """Average colour and a tileable high-frequency weave map (128 = neutral) from the swatch."""
    sw = Image.open(f'outfits/fabrics/{fab}.webp').convert('RGBA')
    w, h = sw.size
    patch = sw.crop((int(w * .36), int(h * .2), int(w * .64), int(h * .42))).convert('RGB')
    color = tuple(int(c) for c in ImageStat.Stat(patch).median)
    lum = patch.convert('L')
    detail = ImageMath.lambda_eval(lambda a: a['convert'](a['a'] * 128 / (a['b'] + 1), 'L'),
                                   a=lum, b=lum.filter(ImageFilter.GaussianBlur(4)))
    # mirror-tile so the weave has no seams
    tw, th = detail.size
    tile = Image.new('L', (tw * 2, th * 2))
    tile.paste(detail, (0, 0)); tile.paste(detail.transpose(Image.FLIP_LEFT_RIGHT), (tw, 0))
    tile.paste(detail.transpose(Image.FLIP_TOP_BOTTOM), (0, th)); tile.paste(detail.rotate(180), (tw, th))
    return color, tile


def tint(im, mask, color, weave, strength):
    """Recolour the garment, keeping its folds: deepen the white render's shading, multiply by the fabric colour."""
    W, H = im.size
    lum = im.convert('L').point(lambda v: min(255, int(255 * (v / 255) ** 1.9 / .82)))
    tex = Image.new('L', (W, H))
    for x in range(0, W, weave.width):
        for y in range(0, H, weave.height):
            tex.paste(weave, (x, y))
    shade = ImageMath.lambda_eval(lambda a: a['convert'](a['l'] * (1280 + (a['t'] - 128) * strength) / 1280, 'L'), l=lum, t=tex)
    rgb = Image.merge('RGB', [shade.point(lambda v, c=c: min(255, v * c // 230)) for c in color])
    out = im.copy()
    out.paste(Image.composite(rgb.convert('RGBA'), im, mask), (0, 0))
    out.putalpha(im.getchannel('A'))
    return out


def waist_line(mask):
    """Top edge of a bottom garment across the torso centre."""
    W, H = mask.size
    box = mask.crop((int(W * .35), 0, int(W * .65), H)).point(lambda v: 255 if v > 128 else 0).getbbox()
    return box[1]


def layer(top, top_mask, bottom, bottom_mask):
    """The top render above the bottom garment's waistband, and wherever the top garment covers it."""
    W, H = top.size
    keep = Image.new('L', (W, H), 0)
    ImageDraw.Draw(keep).rectangle((0, 0, W, waist_line(bottom_mask)), fill=255)
    keep = ImageChops.lighter(keep, top_mask).filter(ImageFilter.GaussianBlur(1))
    return Image.composite(top, bottom, keep)


src = {g: Image.open(f'outfits/garments/{g}.webp').convert('RGBA') for g in FULL + TOPS + BOTTOMS}
masks = {g: garment_mask(im) for g, im in src.items()}
for fab, strength in FABRICS.items():
    color, weave = fabric_tone(fab)
    dyed = {g: tint(src[g], masks[g], color, weave, strength) for g in src}
    jobs = {f'{g}-none': dyed[g] for g in FULL + TOPS + BOTTOMS if g not in BOTTOMS}
    jobs.update({f'none-{b}': dyed[b] for b in BOTTOMS})
    jobs.update({f'{t}-{b}': layer(dyed[t], masks[t], dyed[b], masks[b]) for t in TOPS for b in BOTTOMS})
    for name, im in jobs.items():
        im.save(f'outfits/{name}-{fab}.webp', quality=84, method=6)
    print(fab, color, len(jobs), 'outfits')
