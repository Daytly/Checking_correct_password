import os

import img2pdf

dirname = "/"
imgs = []
for r, _, f in os.walk(dirname):
    for fname in f:
        if not fname.endswith(".png"):
            continue
        imgs.append(os.path.join(r, fname))
with open("name.pdf", "wb") as f:
    f.write(img2pdf.convert(imgs))
