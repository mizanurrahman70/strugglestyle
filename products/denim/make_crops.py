# Cuts the denim page's gallery shots from the model photo (run from the project root, needs Pillow):
#   python products/denim/make_crops.py
#   in : products/denim/model.webp   (1460×1947, the model in the denim jacket and jeans)
#   out: products/denim/{name}.webp  (4:5 crops for the gallery, plus a fabric chip cut from the jeans)
# Boxes are (left, top, width, height) in photo pixels. Small crops are enlarged with Lanczos and a light sharpen.
from PIL import Image, ImageFilter

SRC = 'products/denim/model.webp'
MAX_H = 1500
CROPS = {
    'half':    (330, 20, 700, 875),     # head to hip
    'placket': (560, 320, 320, 400),    # stand collar, chest pockets and button placket
    'jeans':   (290, 790, 784, 980),    # the jeans, waist to hem
    'detail':  (600, 780, 320, 400),    # scalloped hem, heart belt chain and the knee rip
    'hem':     (470, 1477, 376, 470),   # straight hems and the denim boots
    'wash':    (505, 1180, 150, 150),   # fabric chip: the jeans' vintage light wash
}

im = Image.open(SRC).convert('RGB')
for name, (x, y, w, h) in CROPS.items():
    c = im.crop((x, y, x + w, y + h))
    target = 600 if name == 'wash' else min(MAX_H, h * 2)
    if target > h:
        c = c.resize((round(w * target / h), target), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    c.save(f'products/denim/{name}.webp', quality=86, method=6)
    print(name, c.size)
