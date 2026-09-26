import os
from PIL import Image

jpeg_opening = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\jpeg\opening"
for f in ["01.bmp", "02.bmp", "03.bmp"]:
    fpath = os.path.join(jpeg_opening, f)
    if os.path.exists(fpath):
        im = Image.open(fpath)
        print(f"{f}: size={im.size}, mode={im.mode}")

for f in [f"S0{i}.jpg" for i in range(1, 7)]:
    fpath = os.path.join(jpeg_opening, f)
    if os.path.exists(fpath):
        im = Image.open(fpath)
        print(f"{f}: size={im.size}, mode={im.mode}")
