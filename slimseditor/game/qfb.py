from reloadr import autoreload

from slimseditor.saveentry import RangedShort, Boolean, Integer


@autoreload
def get_qfb_items():
    return {
        "Bolt counts": [
            Integer("Number of Bolts", 0x247),
        ],
    }
