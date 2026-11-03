# Builds the woven product page looks from the white single-garment renders + the woven swatches.
# Run from the project root (needs Pillow):  python products/woven/compose_woven.py
#   in : outfits/garments/{id}.webp            (same avatar, same pose, one white garment each)
#        images/swatches/{code}-{colour}.webp  (flat 800px fabric swatches)
#   out: products/woven/looks/{first}-{second}-{code}-{colour}.webp   at SCALE x the render size
# Re-run after adding a garment or colourway; keep WOVEN in products/woven.html in step with it.
import os
import sys

from PIL import Image, ImageFilter, ImageStat

sys.path.insert(0, 'outfits')
from compose_outfits import garment_mask, lambda_eval, layer, tint  # noqa: E402

FULL, TOPS, BOTTOMS = ['dress'], ['shirt', 'blazer'], ['pants', 'skirt']
# fabric code: (weave strength 0-10, colourways)
FABRICS = {
    'ss-w06': (5, ['white', 'sage', 'sky', 'black']),          # linen-cotton: visible slub
    'ss-s07': (1, ['champagne', 'emerald', 'lilac', 'black']),  # satin: smooth
}
SCALE = 1.5  # 820x1260 -> 1230x1890, sharp at 2x on the page's ~600px image column
OUT = 'products/woven/looks'


def swatch_tone(path):
    """Median colour of the swatch and a tileable weave map (128 = neutral) at full resolution."""
    sw = Image.open(path).convert('RGB')
    color = tuple(int(c) for c in ImageStat.Stat(sw).median)
    w, h = sw.size
    lum = sw.crop((w // 4, h // 4, w // 4 + 192, h // 4 + 192)).convert('L')
    detail = lambda_eval(lambda a: a['convert'](a['a'] * 128 / (a['b'] + 1), 'L'),
                         a=lum, b=lum.filter(ImageFilter.GaussianBlur(4)))
    tw, th = detail.size
    tile = Image.new('L', (tw * 2, th * 2))
    tile.paste(detail, (0, 0)); tile.paste(detail.transpose(Image.FLIP_LEFT_RIGHT), (tw, 0))
    tile.paste(detail.transpose(Image.FLIP_TOP_BOTTOM), (0, th)); tile.paste(detail.rotate(180), (tw, th))
    return color, tile


def load(g):
    im = Image.open(f'outfits/garments/{g}.webp').convert('RGBA')
    return im.resize((round(im.width * SCALE), round(im.height * SCALE)), Image.LANCZOS)


os.makedirs(OUT, exist_ok=True)
src = {g: load(g) for g in FULL + TOPS + BOTTOMS}
masks = {g: garment_mask(im) for g, im in src.items()}
for code, (strength, colours) in FABRICS.items():
    for colour in colours:
        color, weave = swatch_tone(f'images/swatches/{code}-{colour}.webp')
        dyed = {g: tint(src[g], masks[g], color, weave, strength) for g in src}
        jobs = {f'{g}-none': dyed[g] for g in FULL + TOPS}
        jobs.update({f'none-{b}': dyed[b] for b in BOTTOMS})
        jobs.update({f'{t}-{b}': layer(dyed[t], masks[t], dyed[b], masks[b]) for t in TOPS for b in BOTTOMS})
        for name, im in jobs.items():
            im.save(f'{OUT}/{name}-{code}-{colour}.webp', quality=86, method=6)
        print(code, colour, color, len(jobs), 'looks')
