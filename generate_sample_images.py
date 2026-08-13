"""
Run this ONCE to create a handful of placeholder garment images in the
/images folder, so you have something to upload and test with right
away -- no need to hunt for real photos before your first test run.

These are simple generated shapes, not real clothing photos. Swap them
out for real garment photos any time; the app works exactly the same
either way. Real photos will actually give more varied, interesting
results from the classifier.

Run with:
    python generate_sample_images.py
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

os.makedirs("images", exist_ok=True)

rng = np.random.default_rng(11)


def noisy_image(base_rgb, noise_amount, size=400, blur_radius=0):
    """Builds a base color with per-pixel noise, so the classifier has
    real texture/contrast to measure instead of a flat block of color."""
    arr = np.ones((size, size, 3), dtype=np.float32) * np.array(base_rgb, dtype=np.float32)
    noise = rng.normal(0, noise_amount, (size, size, 3))
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)
    if blur_radius:
        img = img.filter(ImageFilter.GaussianBlur(blur_radius))
    return img


# (filename, base color, noise amount, blur radius, label)
# These values were tested against image_classifier.py / condition_classifier.py
# so the five samples land on five different ReFab pathways out of the box.
samples = [
    ("sample_reuse_good.png", (190, 170, 140), 55, 0, "Good Condition Garment"),
    ("sample_cellulosic_cotton.png", (222, 208, 185), 8, 0, "Cotton Shirt"),
    ("sample_synthetic_polyester.png", (30, 90, 200), 6, 0, "Polyester Jacket"),
    ("sample_synthetic_nylon.png", (60, 230, 190), 6, 0, "Nylon Activewear"),
    ("sample_manual_review_ambiguous.png", (150, 150, 150), 26, 12, "Ambiguous / Low Confidence"),
]

for filename, color, noise_amt, blur, label in samples:
    # No text/border drawn on top of the image on purpose -- any overlay
    # (even a thin border) skews the color/texture readings the
    # classifier depends on. The descriptive filename is the label.
    img = noisy_image(color, noise_amt, blur_radius=blur)

    path = os.path.join("images", filename)
    img.save(path)
    print(f"Created {path}  ({label})")

print("\nDone. Run the app, then upload any file from the 'images' folder to test.")
print("Tip: real garment photos will give even more varied, realistic results")
print("than these generated placeholders.")
