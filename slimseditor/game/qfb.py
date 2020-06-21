from slimseditor.reloadmagic import autoreload
from slimseditor.saveentry import Boolean, Integer


@autoreload
def get_qfb_items():
    return {
        "Bolt counts": [
            Integer("Number of Bolts", 0x247),
        ],
    }
