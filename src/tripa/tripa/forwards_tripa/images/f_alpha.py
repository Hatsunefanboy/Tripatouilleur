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

# extraction luminosité
gray = ImageOps.grayscale(im1)
mask = ImageEnhance.Contrast(gray).enhance(2.0)

final = Image.composite(im, im1, mask)

final = ImageEnhance.Color(final).enhance(1.6)

final.save(out, format="BMP")