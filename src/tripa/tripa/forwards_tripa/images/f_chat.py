import sys
import struct
from PIL import Image, ImageEnhance, ImageChops, ImageOps
import io
from pathlib import Path
from tkinter import messagebox

in1 = Path(sys.argv[1])
in2 = Path(sys.argv[2])
out = Path(sys.argv[3])

im  = Image.open(in1).convert("RGBA")
im1 = Image.open(in2).convert("RGBA")
im1 = im1.resize(im.size)

# --- Génération de variantes géométriques ---
r1 = im.rotate(15, resample=Image.BICUBIC, expand=False)
r2 = im.rotate(-15, resample=Image.BICUBIC, expand=False)
m1 = ImageOps.mirror(im)
f1 = ImageOps.flip(im)

inv = ImageOps.invert(im.convert("RGB")).convert("RGBA")

# --- Accumulation translucide ---
acc = Image.blend(im, r1, alpha=0.15)
acc = Image.blend(acc, r2, alpha=0.15)
acc = Image.blend(acc, m1, alpha=0.15)
acc = Image.blend(acc, f1, alpha=0.15)
acc = Image.blend(acc, inv, alpha=0.10)

# --- Fusion avec l'autre image (mémoire croisée) ---
acc = Image.blend(acc, im1, alpha=0.25)

# --- Saturation douce (organique) ---
final = ImageEnhance.Color(acc).enhance(1.6)

final.save(out, format="BMP")



