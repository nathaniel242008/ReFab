"""
ReFab Simulated Condition Classifier
-------------------------------------
A rule-of-thumb stand-in for a trained "garment condition" model.
Uses image sharpness and contrast as a rough proxy: a crisp,
high-contrast photo is treated as showing a garment in "Good"
condition; a soft, low-contrast, flat-looking photo is treated as
"Damaged".

This is a simplification made for demo purposes -- a real system
would be trained on labeled photos of worn/torn vs. intact garments,
or would use the material classifier's own confidence as a signal.
Swap this out later; the rest of the app does not need to change.
"""

import numpy as np
from PIL import Image, ImageFilter


def classify_condition(image: Image.Image):
    """
    Returns (condition: str, confidence: int 0-100)
    """
    gray = image.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_arr = np.array(edges, dtype=np.float32)
    gray_arr = np.array(gray, dtype=np.float32)

    sharpness = float(edge_arr.std())
    contrast = float(gray_arr.std())

    score = sharpness * 0.6 + contrast * 0.4

    if score > 40:
        condition = "Good"
        confidence = int(min(95, 55 + (score - 40) * 0.8))
    else:
        condition = "Damaged"
        confidence = int(min(95, 55 + (40 - score) * 0.8))

    confidence = max(35, min(confidence, 95))
    return condition, confidence
