import os, sys

mod_dir = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"
total_bytes = 0
file_count = 0
categories = {}

for root, dirs, files in os.walk(mod_dir):
    for f in files:
        fp = os.path.join(root, f)
        sz = os.path.getsize(fp)
        total_bytes += sz
        file_count += 1
        ext = os.path.splitext(f)[1].lower()
        if ext not in categories:
            categories[ext] = [0, 0]
        categories[ext][0] += 1
        categories[ext][1] += sz

print(f"Total files: {file_count}")
print(f"Total size: {total_bytes / (1024*1024):.2f} MB")
for ext, (cnt, b) in sorted(categories.items(), key=lambda x: x[1][1], reverse=True):
    print(f"  {ext:10s}: {cnt:3d} files, {b / (1024*1024):6.2f} MB")

all_files = []
for root, dirs, files in os.walk(mod_dir):
    for f in files:
        fp = os.path.join(root, f)
        all_files.append((os.path.getsize(fp), f))
all_files.sort(reverse=True)
print("\nTop 5 Largest Files:")
for sz, fn in all_files[:5]:
    print(f"  {fn:25s}: {sz / (1024*1024):6.2f} MB")
