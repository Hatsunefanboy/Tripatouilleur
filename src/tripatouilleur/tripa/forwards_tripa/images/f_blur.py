import sys
import struct
from PIL import Image, ImageEnhance, ImageOps,ImageFilter
import io
from pathlib import Path
from tkinter import messagebox

in1 = Path(sys.argv[1])
in2 = Path(sys.argv[2])
out = Path(sys.argv[3])

im  = Image.open(in1).convert("RGBA")
im1 = Image.open(in2).convert("RGBA")
im1 = im1.resize(im.size)

b1 = im.filter(ImageFilter.GaussianBlur(3))
b2 = im1.filter(ImageFilter.GaussianBlur(3))

c1=ImageEnhance.Sharpness(b1)
c2=ImageEnhance.Sharpness(b2)

b1=c1.enhance(50)
b2=c2.enhance(50)

final = Image.blend(b1,b2,0.7)

final.save(out, format="BMP")
