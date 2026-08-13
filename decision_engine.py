from treatment_data import TREATMENTS


def get_treatment(material, condition, confidence):
    """
    Determines the recommended treatment pathway.
    Returns one entry from TREATMENTS.
    """

    # Low confidence -> manual review, no matter what the guess was
    if confidence < 70:
        return TREATMENTS["manual"]

    # Good condition -> prioritize reuse over breaking the garment down
    if condition == "Good":
        return TREATMENTS["reuse"]

    # Damaged material -> material-specific recovery
    if material in ["Cotton", "Linen"]:
        return TREATMENTS["cellulosic"]

    if material in ["Polyester", "Nylon"]:
        return TREATMENTS["synthetic"]

    if material in ["Mixed", "Acrylic", "Unknown"]:
        return TREATMENTS["mixed"]

    return TREATMENTS["manual"]
