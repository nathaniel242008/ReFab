TREATMENTS = {
    "reuse": {
        "name": "Reuse / Repair",
        "description": "The garment appears suitable for another use. It can be cleaned, repaired and redirected to resale, donation or reuse.",
        "stream": "REUSE"
    },

    "cellulosic": {
        "name": "Cellulosic / Mechanical Recovery",
        "description": "Suitable natural or cellulosic textiles can be directed toward fibre recovery processes such as shredding and fibre opening.",
        "stream": "CELLULOSIC RECOVERY"
    },

    "synthetic": {
        "name": "Synthetic Polymer Recovery",
        "description": "Synthetic textiles such as polyester and nylon can be directed toward appropriate polymer recovery processes.",
        "stream": "SYNTHETIC RECOVERY"
    },

    "mixed": {
        "name": "Mixed-Fibre Separation",
        "description": "Complex or blended textiles should be separated or sent to a specialized recovery pathway rather than contaminating a single-material stream.",
        "stream": "MIXED / DIFFICULT"
    },

    "manual": {
        "name": "Manual Review",
        "description": "The classification confidence is too low for automatic routing. The garment should be inspected before entering a material-specific stream.",
        "stream": "MANUAL REVIEW"
    }
}

# Step-by-step pathway shown to the user after a treatment is chosen.
PATHWAYS = {
    "reuse": [
        "Collection", "Inspection", "Cleaning", "Repair", "Resale / Donation"
    ],
    "cellulosic": [
        "Sorting", "Accessory Removal", "Cutting", "Shredding",
        "Fibre Opening", "Carding", "Re-spinning", "Recycled Yarn / Nonwoven"
    ],
    "synthetic": [
        "Sorting", "Preparation", "Chemical Breakdown",
        "Purification", "Recovered Polymer", "New Fibre"
    ],
    "mixed": [
        "Sorting", "AI Blend Identification", "Fibre Separation",
        "Cotton Fraction -> Cellulosic Recovery",
        "Polyester Fraction -> Synthetic Recovery"
    ],
    "manual": [
        "Flagged for Human Inspection", "Manual Fibre Check",
        "Routed to Correct Stream"
    ]
}

# Recovery priority order shown on the dashboard.
PRIORITY_ORDER = [
    "REUSE",
    "CELLULOSIC RECOVERY",
    "SYNTHETIC RECOVERY",
    "MIXED / DIFFICULT",
    "MANUAL REVIEW",
]
