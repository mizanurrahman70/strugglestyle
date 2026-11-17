# Renders the hover clips for the Denim and Woven cards in "Offering a diverse range of products".
# Concepts and matching AI-video prompts: media/clips/PROMPTS.md
#   Denim  "Stitch & Reveal"  — fabric is stitched, splits open on the model, detail panels slide through, closes again
#   Woven  "3D Fitting Room"  — a scan line sweeps the 3D avatar and re-dresses it look by look
# Every frame is composed here (PIL) and piped to ffmpeg; both clips loop seamlessly.
# Needs Pillow + ffmpeg with libx264 (set FFMPEG=/path/to/ffmpeg if not on PATH; falls back to imageio-ffmpeg):
#   python media/clips/make_clips.py            # both
#   python media/clips/make_clips.py woven      # one
# out: media/clips/denim.mp4, media/clips/woven.mp4  — 720x960 (3:4, matches .cat .media), 30 fps, silent
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

FFMPEG = os.environ.get('FFMPEG') or shutil.which('ffmpeg')
if not FFMPEG:
    try:
        import imageio_ffmpeg
        FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise SystemExit('ffmpeg not found — install it, pip install imageio-ffmpeg, or set FFMPEG=/path/to/ffmpeg')

W, H, FPS = 720, 960, 30
GREEN, GREEN_D, GOLD, INDIGO = (31, 148, 87), (17, 64, 42), (232, 176, 84), (16, 32, 62)

FONTS = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'


def font(name, size, var=None):
    f = ImageFont.truetype(str(FONTS / name), size)
    if var:
        f.set_variation_by_name(var)
    return f


def serif(size):
    return font('georgiaz.ttf', size)  # Georgia bold italic, closest system match to the site's Fraunces


def sans(size, var='SemiBold'):
    return font('bahnschrift.ttf', size, var)


# ---------- easing / timing ----------
def clamp(t):
    return max(0.0, min(1.0, t))


def seg(t, a, b):
    return clamp((t - a) / (b - a))


def smooth(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def out3(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def inout(t):
    t = clamp(t)
    return 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2


# ---------- image helpers ----------
def load(path, mode='RGB'):
    return Image.open(ROOT / path).convert(mode)


def cover(im, w, h, over=1.15):
    """Scale so the image covers (w, h) with `over` headroom for zooming and drifting."""
    s = max(w * over / im.width, h * over / im.height)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def view(src, w, h, zoom=1.0, fx=.5, fy=.4):
    """A (w, h) camera onto src: zoom 1 shows the largest w:h box, fx/fy is the centre as a fraction of src."""
    bw = min(src.width, src.height * w / h) / zoom
    bh = bw * h / w
    x0 = min(max(fx * src.width - bw / 2, 0), src.width - bw)
    y0 = min(max(fy * src.height - bh / 2, 0), src.height - bh)
    box = (x0, y0, x0 + bw, y0 + bh)
    img = src.resize((w, h), Image.BICUBIC, box=box).convert('RGBA')
    to_frame = lambda px, py: ((px * src.width - x0) * w / bw, (py * src.height - y0) * h / bh)
    return img, to_frame


def layer(size=(W, H)):
    return Image.new('RGBA', size, (0, 0, 0, 0))


def shadow_text(frame, xy, txt, f, fill, alpha, anchor='mm', shadow=.35):
    if alpha <= 0:
        return
    lay = layer(frame.size)
    d = ImageDraw.Draw(lay)
    d.text((xy[0] + 2, xy[1] + 3), txt, font=f, fill=(0, 0, 0, int(255 * shadow * alpha)), anchor=anchor)
    lay = lay.filter(ImageFilter.GaussianBlur(3))
    ImageDraw.Draw(lay).text(xy, txt, font=f, fill=fill + (int(255 * alpha),), anchor=anchor)
    frame.alpha_composite(lay)


def chip(frame, x, y, text, a):
    """White label pill with a green dot; slides in from the left as `a` goes 0→1."""
    if a <= 0:
        return
    f = sans(22)
    w = int(f.getlength(text) + 58)
    h = 46
    ox = int(x - (1 - out3(a)) * 40)
    lay = layer(frame.size)
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((ox + 2, y + 5, ox + w + 2, y + h + 5), radius=h // 2, fill=(0, 0, 0, int(60 * a)))
    lay = lay.filter(ImageFilter.GaussianBlur(6))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((ox, y, ox + w, y + h), radius=h // 2, fill=(255, 255, 255, int(240 * a)))
    d.ellipse((ox + 19, y + 19, ox + 27, y + 27), fill=GREEN + (int(255 * a),))
    d.text((ox + 38, y + h / 2), text, font=f, fill=GREEN_D + (int(255 * a),), anchor='lm')
    frame.alpha_composite(lay)


def hotspot(frame, x, y, t, a):
    """Pulsing tap-point: solid dot plus two expanding rings."""
    if a <= 0:
        return
    lay = layer(frame.size)
    d = ImageDraw.Draw(lay)
    for k in (0, .5):
        p = (t * .9 + k) % 1
        r = 12 + 34 * p
        d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 255, int(220 * (1 - p) * a)), width=3)
    d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=(255, 255, 255, int(255 * a)))
    d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=GREEN + (int(255 * a),))
    frame.alpha_composite(lay)


def soft_glow(size, rgb, alpha, blur, draw):
    """Blur only the alpha of a solid colour, so the glow fades to transparent instead of to grey."""
    m = Image.new('L', size, 0)
    draw(ImageDraw.Draw(m))
    m = m.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: v * alpha // 255)
    out = Image.new('RGBA', size, rgb + (0,))
    out.putalpha(m)
    return out


class Encoder:
    def __init__(self, name):
        self.dest = OUT / f'{name}.mp4'
        self.p = subprocess.Popen(
            [FFMPEG, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
             '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '23',
             '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(self.dest)],
            stdin=subprocess.PIPE)

    def write(self, frame):
        self.p.stdin.write(frame.convert('RGB').tobytes())

    def close(self):
        self.p.stdin.close()
        if self.p.wait():
            raise SystemExit(f'ffmpeg failed for {self.dest.name}')
        print(f'{self.dest.relative_to(ROOT)}  {self.dest.stat().st_size // 1024} KB')


# ---------- Denim: "Stitch & Reveal" ----------
def denim():
    T = 10.0
    tex = cover(load('products/denim/wash.webp'), W, H, 1.12)
    tex = Image.blend(tex, Image.new('RGB', tex.size, INDIGO), .3)
    look1 = cover(load('products/denim/model.webp'), W, H, 1.18)
    look2 = cover(load('products/denim/skirt/model.webp'), W, H, 1.18)
    PW = W // 3
    panels = [(cover(load(p), PW - 6, H, 1.15), cap) for p, cap in (
        ('products/denim/placket.webp', 'Shank buttons'),
        ('products/denim/detail.webp', 'Hand distressing'),
        ('products/denim/hem.webp', 'Raw hem'),
    )]
    f_title, f_sub, f_cap = serif(156), sans(26, 'Regular'), sans(20)

    # soft shadow cast by the edge of each fabric half as it opens
    edge = layer((48, H))
    for x in range(48):
        ImageDraw.Draw(edge).line((x, 0, x, H), fill=(0, 0, 0, int(110 * (1 - x / 48) ** 2)))

    def fabric(t, stitch, title, sub):
        # drift is periodic over T so the last frame meets the first
        img, _ = view(tex, W, H, 1.06, .5 + .06 * math.sin(2 * math.pi * t / T), .5 + .05 * math.cos(2 * math.pi * t / T))
        if stitch > 0:
            lay = layer()
            d = ImageDraw.Draw(lay)
            end = stitch * H if stitch < 1 else H
            a = min(1, stitch * 4) if stitch < 1 else 1
            d.line((W / 2, 0, W / 2, end), fill=(8, 18, 40, int(90 * a)), width=3)  # seam groove
            for x in (W / 2 - 9, W / 2 + 9):
                for y0 in range(0, int(end), 26):
                    y1 = min(y0 + 15, end)
                    d.line((x + 1.5, y0 + 2, x + 1.5, y1 + 2), fill=(0, 0, 0, 90), width=4)
                    d.line((x, y0, x, y1), fill=GOLD + (255,), width=4)
            if 0 < stitch < 1:  # needle head
                d.ellipse((W / 2 - 14, end - 14, W / 2 + 14, end + 14), fill=(255, 240, 210, 70))
                d.ellipse((W / 2 - 6, end - 6, W / 2 + 6, end + 6), fill=(255, 255, 255, 255))
            img.alpha_composite(lay)
        shadow_text(img, (W / 2, H * .42 + (1 - out3(title)) * 50), 'Denim', f_title, (255, 255, 255), clamp(title))
        shadow_text(img, (W / 2, H * .42 + 100 + (1 - out3(sub)) * 30), 'Jeans  ·  Jackets  ·  Vests', f_sub,
                    (255, 255, 255), clamp(sub))
        return img

    def split(fab, behind, open_):
        frame = behind.copy()
        dx = int(open_ * W / 2)
        frame.alpha_composite(fab.crop((0, 0, W // 2, H)), (-dx, 0))
        frame.alpha_composite(fab.crop((W // 2, 0, W, H)), (W // 2 + dx, 0))
        if 0 < open_ < 1:
            frame.alpha_composite(edge, (W // 2 - dx, 0))
            frame.alpha_composite(edge.transpose(Image.FLIP_LEFT_RIGHT), (W // 2 + dx - 48, 0))
        return frame

    def model(src, t, t0, t1, pt, label, lt):
        img, at = view(src, W, H, 1.16 - .14 * smooth(seg(t, t0, t1)), .5, .36)
        a = smooth(seg(t, lt, lt + .4)) * (1 - smooth(seg(t, t1 - .35, t1 - .05)))
        hotspot(img, *at(*pt), t, a)
        chip(img, 32, H - 96, label, a)
        return img

    enc = Encoder('denim')
    for n in range(round(T * FPS)):
        t = n / FPS
        if t < 2.0:  # stitch sews down, title rises
            frame = fabric(t, seg(t, .1, 1.2), seg(t, .6, 1.3), seg(t, .9, 1.6))
        elif t < 4.6:  # fabric splits open on look 1
            behind = model(look1, t, 2.0, 4.6, (.52, .29), 'Hand-finished vintage wash', 3.0)
            frame = split(fabric(t, 1, 1, 1), behind, inout(seg(t, 2.0, 2.8))) if t < 2.8 else behind
        elif t < 8.6:  # detail panels slide through, then away onto look 2
            behind = model(look1, t, 2.0, 4.6, (.52, .29), '', 9) if t < 6.8 else \
                model(look2, t, 6.8, 8.6, (.5, .62), 'Panelled maxi skirt  ·  12 oz', 7.5)
            frame = behind
            for i, (src, cap) in enumerate(panels):
                d = -1 if i % 2 == 0 else 1  # alternate: from top, from bottom
                pin = out3(seg(t, 4.6 + i * .1, 5.3 + i * .1))
                pout = inout(seg(t, 6.8 + i * .08, 7.5 + i * .08))
                y = int(d * (1 - pin) * H - d * pout * H)
                if abs(y) >= H:
                    continue
                img, _ = view(src, PW - 6, H, 1.12 - .08 * seg(t, 4.6, 7.6), .5, .45 + .1 * d * seg(t, 4.6, 7.6))
                tile = Image.new('RGBA', (PW, H), INDIGO + (255,))
                tile.alpha_composite(img, (3, 0))
                shadow_text(tile, (PW / 2, H - 56), cap, f_cap, (255, 255, 255), smooth(seg(t, 5.4 + i * .12, 5.8 + i * .12)), shadow=.6)
                frame.alpha_composite(tile, (i * PW, y))
        else:  # fabric closes, then stitch + title fade back to the opening frame
            behind = model(look2, t, 6.8, 8.6, (.5, .62), '', 99)
            fade = 1 - smooth(seg(t, 9.4, 9.95))
            frame = split(fabric(t, fade, fade, fade), behind, 1 - inout(seg(t, 8.6, 9.4)))
        enc.write(frame)
    enc.close()


# ---------- Woven: "3D Fitting Room" ----------
def woven():
    LOOKS = [
        ('shirt-pants-ss-w06-white-sage', 'Shirt & wide trousers', 'Cotton-linen poplin  ·  150 GSM', 'ss-w06-white'),
        ('shirt-pants-ss-w06-sky-white', 'Shirt & wide trousers', 'Cotton-linen poplin  ·  150 GSM', 'ss-w06-sky'),
        ('blazer-pants-ss-s07-champagne', 'Satin blazer suit', 'Silk-touch satin  ·  120 GSM', 'ss-s07-champagne'),
        ('blazer-pants-ss-s07-emerald', 'Satin blazer suit', 'Silk-touch satin  ·  120 GSM', 'ss-s07-emerald'),
        ('dress-none-ss-w06-sage', 'Linen maxi dress', 'Linen-cotton blend  ·  150 GSM', 'ss-w06-sage'),
        ('shirt-skirt-ss-s07-lilac', 'Satin shirt & skirt', 'Silk-touch satin  ·  120 GSM', 'ss-s07-lilac'),
    ]
    SEG, SCAN = 1.6, .8
    T = SEG * len(LOOKS)
    AH, FEET = int(H * .72), int(H * .835)

    # avatars: crop all to the union of their content so they line up, then scale to a fixed height
    raw = [load(f'products/woven/looks/{f}.webp', 'RGBA') for f, *_ in LOOKS]
    boxes = [im.getchannel('A').getbbox() for im in raw]
    ub = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
    AW = round((ub[2] - ub[0]) * AH / (ub[3] - ub[1]))
    avatars = [im.crop(ub).resize((AW, AH), Image.LANCZOS) for im in raw]
    AX, AY = (W - AW) // 2, FEET - AH

    def swatch(name, s=58):
        im = load(f'images/swatches/{name}-sm.webp')
        im = im.resize((s * 4, s * 4), Image.LANCZOS)
        m = Image.new('L', (s * 4, s * 4), 0)
        ImageDraw.Draw(m).ellipse((0, 0, s * 4 - 1, s * 4 - 1), fill=255)
        out = Image.new('RGBA', (s * 4, s * 4), (0, 0, 0, 0))
        out.paste(im, mask=m)
        ImageDraw.Draw(out).ellipse((2, 2, s * 4 - 3, s * 4 - 3), outline=(196, 212, 202, 255), width=8)
        return out.resize((s, s), Image.LANCZOS)
    swatches = [swatch(s) for *_, s in LOOKS]

    # studio: soft gradient, spotlight, perspective floor grid
    bg = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        k = y / H
        d.line((0, y, W, y), fill=(int(246 - 16 * k), int(250 - 12 * k), int(247 - 15 * k), 255))
    bg.alpha_composite(soft_glow((W, H), (255, 255, 255), 170, 70,
                                 lambda d: d.ellipse((W * .1, H * .05, W * .9, H * .85), fill=255)))
    grid = layer()
    d = ImageDraw.Draw(grid)
    hy, vx = FEET - 70, W / 2
    for k in range(1, 9):
        y = hy + (H - hy) * (k / 8) ** 1.8
        d.line((0, y, W, y), fill=GREEN + (26,), width=1)
    for k in range(-9, 10):
        d.line((vx + k * 18, hy, vx + k * 150, H), fill=GREEN + (22,), width=1)
    fade = Image.new('L', (W, H), 0)
    for y in range(int(hy), H):
        ImageDraw.Draw(fade).line((0, y, W, y), fill=int(255 * min(1, (y - hy) / 90)))
    grid.putalpha(ImageChops.multiply(grid.getchannel('A'), fade))
    bg.alpha_composite(grid)
    sh = layer()
    ImageDraw.Draw(sh).ellipse((W / 2 - 150, FEET - 22, W / 2 + 150, FEET + 22), fill=(20, 50, 35, 70))
    bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))

    # scan glow: tint the newly dressed body just above the line
    BAND = 110
    band = Image.new('L', (1, BAND))
    for y in range(BAND):
        band.putpixel((0, y), int(255 * (y / BAND) ** 2))
    band = band.resize((AW, BAND))
    glow = soft_glow((W, 40), GREEN, 200, 7, lambda d: d.line((AX - 70, 20, AX + AW + 70, 20), fill=255, width=8))

    f_name, f_fab, f_ui, f_small = serif(36), sans(21, 'Regular'), sans(20), sans(15)
    enc = Encoder('woven')
    for n in range(round(T * FPS)):
        t = n / FPS
        k = int(t // SEG) % len(LOOKS)
        prev = (k - 1) % len(LOOKS)
        lt = t - (t // SEG) * SEG
        s = inout(lt / SCAN)
        frame = bg.copy()

        # turntable ring under the feet, rotating (period divides T so it loops)
        ring = layer()
        rot = 360 * t / (T / 2)
        rx, ry = 190, 34
        dr = ImageDraw.Draw(ring)
        for j in range(30):
            a0 = j * 12 + rot
            dr.arc((W / 2 - rx, FEET - ry, W / 2 + rx, FEET + ry), a0, a0 + 6, fill=GREEN + (120,), width=3)
        frame.alpha_composite(ring)

        # avatar: new look above the scan line, previous below; gentle idle breathing
        line_y = -30 + s * (AH + 60)  # in avatar coords
        cut = int(clamp(line_y / AH) * AH)
        av = avatars[prev].copy()
        if cut > 0:
            av.paste(avatars[k].crop((0, 0, AW, cut)), (0, 0))
        if 0 < cut < AH + BAND:
            y0, y1 = max(0, cut - BAND), min(cut, AH)
            if y1 > y0:
                m = ImageChops.multiply(band.crop((0, BAND - (cut - y0), AW, BAND - (cut - y1))),
                                        avatars[k].getchannel('A').crop((0, y0, AW, y1)))
                tint = Image.new('RGBA', (AW, y1 - y0), GREEN + (0,))
                tint.putalpha(m.point(lambda v: int(v * .65)))
                av.alpha_composite(tint, (0, y0))
        b = 1 + .007 * math.sin(2 * math.pi * t / 2.4)
        bw, bh = round(AW * (1 + (b - 1) * .4)), round(AH * b)
        frame.alpha_composite(av.resize((bw, bh), Image.BILINEAR), ((W - bw) // 2, FEET - bh))

        # scan line + readout
        if 0 < lt < SCAN + .05:
            la = min(1, lt / .1, (SCAN + .05 - lt) / .12)
            ly = int(FEET - bh + line_y * b)
            g = glow.copy()
            g.putalpha(g.getchannel('A').point(lambda v: int(v * la)))
            frame.alpha_composite(g, (0, ly - 20))
            lay = layer()
            dl = ImageDraw.Draw(lay)
            dl.line((AX - 70, ly, AX + AW + 70, ly), fill=GREEN + (int(255 * la),), width=2)
            for x in (AX - 70, AX + AW + 70):
                dl.line((x, ly - 9, x, ly + 9), fill=GREEN + (int(255 * la),), width=3)
            dl.text((AX + AW + 62, ly - 14), f'SCANNING  {int(s * 100):02d}%', font=f_small,
                    fill=GREEN_D + (int(230 * la),), anchor='rs')
            frame.alpha_composite(lay)

        # HUD
        hud = layer()
        dh = ImageDraw.Draw(hud)
        dh.rounded_rectangle((24, 24, 238, 66), radius=21, fill=(255, 255, 255, 235))
        pulse = .45 + .55 * (0.5 + 0.5 * math.cos(2 * math.pi * t / .8))
        dh.ellipse((40, 39, 52, 51), fill=(*GREEN, int(255 * pulse)))
        dh.text((62, 45), '3D FITTING ROOM', font=f_ui, fill=GREEN_D + (255,), anchor='lm')
        shown = k if s > .5 else prev
        dh.text((W - 28, 45), f'LOOK {shown + 1:02d} / {len(LOOKS):02d}', font=f_ui, fill=GREEN_D + (255,), anchor='rm')
        dh.rounded_rectangle((24, H - 118, W - 24, H - 24), radius=20, fill=(255, 255, 255, 235))
        frame.alpha_composite(hud)

        # bottom label: previous slides out, new slides in once the scan passes halfway
        for idx, a, dy in ((prev, 1 - smooth(seg(lt, 0, SCAN * .45)), -1), (k, out3(seg(lt, SCAN * .3, SCAN * .3 + .45)), 1)):
            if a <= 0:
                continue
            off = int((1 - a) * 22 * dy)
            lab = layer()
            sw = swatches[idx].copy()
            sw.putalpha(sw.getchannel('A').point(lambda v: int(v * a)))
            lab.alpha_composite(sw, (46, H - 100 + off))
            dlab = ImageDraw.Draw(lab)
            dlab.text((124, H - 80 + off), LOOKS[idx][1], font=f_name, fill=GREEN_D + (int(255 * a),), anchor='lm')
            dlab.text((126, H - 46 + off), LOOKS[idx][2], font=f_fab, fill=(90, 110, 98, int(255 * a)), anchor='lm')
            box = layer()
            ImageDraw.Draw(box).rounded_rectangle((24, H - 118, W - 24, H - 24), radius=20, fill=(255, 255, 255, 255))
            lab.putalpha(ImageChops.multiply(lab.getchannel('A'), box.getchannel('A')))  # clip to the card
            frame.alpha_composite(lab)

        # progress dots along the card's right edge
        dots = layer()
        dd = ImageDraw.Draw(dots)
        for i in range(len(LOOKS)):
            x = W - 52 - (len(LOOKS) - 1 - i) * 18
            on = i == shown
            r = 5 if on else 3.5
            dd.ellipse((x - r, H - 71 - r, x + r, H - 71 + r), fill=(GREEN + (255,)) if on else (170, 190, 178, 255))
        frame.alpha_composite(dots)
        enc.write(frame)
    enc.close()


if __name__ == '__main__':
    which = sys.argv[1:] or ['denim', 'woven']
    for name in which:
        {'denim': denim, 'woven': woven}[name]()
