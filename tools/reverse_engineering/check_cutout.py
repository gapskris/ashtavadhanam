import os
from PIL import Image

jpeg_opening = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\jpeg\opening"
im1 = Image.open(os.path.join(jpeg_opening, "01.bmp"))
im2 = Image.open(os.path.join(jpeg_opening, "02.bmp"))
im3 = Image.open(os.path.join(jpeg_opening, "03.bmp"))

# Let's find contiguous pure white block in 01.bmp
w, h = im1.size
# Check pixels at center (400, 300)
print("Pixel at (400, 300) in 01.bmp:", im1.getpixel((400, 300)))
print("Pixel at (400, 300) in 02.bmp:", im2.getpixel((400, 300)))
print("Pixel at (400, 300) in 03.bmp:", im3.getpixel((400, 300)))

# Find horizontal span of pure white (255, 255, 255) around center
mid_y = 300
white_xs = [x for x in range(w) if im1.getpixel((x, mid_y)) == (255, 255, 255)]
print(f"Row {mid_y} pure white range: min={min(white_xs)}, max={max(white_xs)}, width={max(white_xs)-min(white_xs)+1}")

mid_x = 400
white_ys = [y for y in range(h) if im1.getpixel((mid_x, y)) == (255, 255, 255)]
print(f"Col {mid_x} pure white range: min={min(white_ys)}, max={max(white_ys)}, height={max(white_ys)-min(white_ys)+1}")

# Check 02.bmp center
print("Row 300 in 02.bmp pure white range:", len([x for x in range(w) if im2.getpixel((x, mid_y)) == (255, 255, 255)]))
