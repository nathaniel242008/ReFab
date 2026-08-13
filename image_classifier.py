"""
ReFab Simulated Material Classifier
------------------------------------
A lightweight, rule-based stand-in for a trained AI image classifier.
It reads real, measurable features from the uploaded photo -- average
color, color saturation, and surface texture (edge density) -- and
maps those features to a plausible fabric category with a confidence
score.

Why this instead of a trained model? Training a real classifier needs
a labeled photo dataset and time you likely don't have during a
hackathon. This module lets you demo the FULL pipeline (image ->
material -> condition -> treatment) honestly and it behaves like a
real classifier would: different photos give different answers,
ambiguous photos give low confidence and trigger manual review.

To upgrade later: swap the body of classify_material() for a call to
a trained model (e.g. a fine-tuned MobileNet). Nothing else in the
app needs to change, because the function signature stays the same.
"""

import numpy as np
from PIL import Image, ImageFilter

MATERIALS = ["Cotton", "Polyester", "Nylon", "Linen", "Mixed", "Acrylic", "Unknown"]


def _texture_score(image: Image.Image) -> float:
    """Rough edge-density measure. Woven/knit fabrics show more edges."""
    edges = image.convert("L").filter(ImageFilter.FIND_EDGES)
    arr = np.array(edges, dtype=np.float32)
    return float(arr.mean())


def _color_features(image: Image.Image):
    small = image.convert("RGB").resize((64, 64))
    arr = np.array(small, dtype=np.float32) / 255.0
    mx, mn = arr.max(axis=2), arr.min(axis=2)
    saturation = float((mx - mn).mean())
    brightness = float(arr.mean())
    return saturation, brightness


def classify_material(image: Image.Image):
    """
    Returns (material: str, confidence: int 0-100, features: dict)
    """
    texture = _texture_score(image)
    saturation, brightness = _color_features(image)

    scores = {m: 0.3 for m in MATERIALS}  # small baseline so nothing is ever 0

    # Smooth + saturated -> synthetic (polyester / nylon)
    if saturation > 0.25 and texture < 18:
        scores["Polyester"] += 2.0
        scores["Nylon"] += 1.2

    # Textured + muted color -> natural woven fibre
    if saturation < 0.18 and texture >= 18:
        scores["Cotton"] += 2.0
        scores["Linen"] += 1.0

    # In-between on both axes -> could well be a blend
    if 0.18 <= saturation <= 0.28 and 14 <= texture <= 24:
        scores["Mixed"] += 1.5

    # Very bright + very saturated -> often synthetic activewear
    if brightness > 0.6 and saturation > 0.3:
        scores["Nylon"] += 1.5

    # Heavy fuzzy texture -> acrylic / wool-like
    if texture > 30:
        scores["Acrylic"] += 1.0

    total = sum(scores.values())
    best = max(scores, key=scores.get)
    top_share = scores[best] / total

    if top_share < 0.22:
        # Nothing stood out clearly from the others
        return "Unknown", 42, {
            "texture": round(texture, 1),
            "saturation": round(saturation, 3),
            "brightness": round(brightness, 3),
        }

    confidence = int(min(97, max(35, top_share * 100 + 25)))

    return best, confidence, {
        "texture": round(texture, 1),
        "saturation": round(saturation, 3),
        "brightness": round(brightness, 3),
    }
