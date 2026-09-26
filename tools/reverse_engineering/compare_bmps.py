import os
from PIL import Image

jpeg_opening = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\jpeg\opening"

im1 = Image.open(os.path.join(jpeg_opening, "01.bmp"))
im2 = Image.open(os.path.join(jpeg_opening, "02.bmp"))
im3 = Image.open(os.path.join(jpeg_opening, "03.bmp"))

# Let's inspect the bounding box of the center cutout in 01.bmp
# Where is the white box or transparent box in 01.bmp?
w, h = im1.size
white_pixels = []
for y in range(0, h, 5):
    for x in range(0, w, 5):
        r, g, b = im1.getpixel((x, y))
        if r > 240 and g > 240 and b > 240:
            white_pixels.append((x, y))

if white_pixels:
    min_x = min(x for x, y in white_pixels)
    max_x = max(x for x, y in white_pixels)
    min_y = min(y for x, y in white_pixels)
    max_y = max(y for x, y in white_pixels)
    print(f"01.bmp center box bounds: x=({min_x}, {max_x}), y=({min_y}, {max_y}), width={max_x - min_x}, height={max_y - min_y}")

# Compare 01 and 02
diff_01_02 = 0
for y in range(0, h, 10):
    for x in range(0, w, 10):
        if im1.getpixel((x, y)) != im2.getpixel((x, y)):
            diff_01_02 += 1
print(f"Diff samples between 01.bmp and 02.bmp: {diff_01_02}")

# Compare 01 and 03
diff_01_03 = 0
for y in range(0, h, 10):
    for x in range(0, w, 10):
        if im1.getpixel((x, y)) != im3.getpixel((x, y)):
            diff_01_03 += 1
print(f"Diff samples between 01.bmp and 03.bmp: {diff_01_03}")
