import sys
import struct
from PIL import Image, ImageEnhance, ImageOps
import io
from pathlib import Path
from tkinter import messagebox

in1 = Path(sys.argv[1])
in2 = Path(sys.argv[2])
out = Path(sys.argv[3])

im  = Image.open(in1).convert("RGBA")
im1 = Image.open(in2).convert("RGBA")
im1 = im1.resize(im.size)

r, g, b, a = im.split()
inv = ImageOps.invert(Image.merge("RGB", (r, g, b))).convert("RGBA")

final = Image.blend(inv, im1, alpha=0.45)
final = ImageEnhance.Color(final).enhance(2.5)

final.save(out, format="BMP")
