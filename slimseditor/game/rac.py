from slimseditor.reloadmagic import autoreload
from slimseditor.saveentry import RangedShort, Boolean, Integer


@autoreload
def get_rac_items():
    return {
        "Weapon Ammo": [
            RangedShort("Bomb Glove", 0x147, 40),
            RangedShort("Blaster", 0x15b, 200),
            RangedShort("Visibomb", 0x153, 20),
            RangedShort("Devastator", 0x14b, 20),
            RangedShort("Gold Glove of Doom", 0x16f, 10),
            RangedShort("R.Y.N.O.", 0x17b, 50),
            RangedShort("Drone", 0x17f, 10),
            RangedShort("Pyrociter", 0x15f, 240),
            RangedShort("Mine Glove", 0x163, 50),
            RangedShort("Tesla Claw", 0x16b, 240),
            RangedShort("Decoy Glove", 0x183, 20),
        ],
        "Weapon Unlocks": [
            Boolean("Bomb Glove", 0x1c2),
            Boolean("Pyrocitor", 0x1c8),
            Boolean("Blaster", 0x1c7),
            Boolean("Glove of Doom", 0x1cc),
            Boolean("Mine Glove", 0x1c9),
            Boolean("Taunter", 0x1c6),
            Boolean("Suck Cannon", 0x1c1),
            Boolean("Devastator", 0x1c3),
            Boolean("Walloper", 0x1ca),
            Boolean("Visibomb Gun", 0x1c5),
            Boolean("Decoy Glove", 0x1d1),
            Boolean("Drone Device", 0x1d0),
            Boolean("Tesla Claw", 0x1cb),
            Boolean("Morph-o-ray", 0x1cd),
            Boolean("R.Y.N.O.", 0x1cf),
        ],
        "Gadget unlocks": [
            Boolean("Trespasser", 0x1d2),
            Boolean("Hydrodisplacer", 0x1ce),
            Boolean("Swingshot", 0x1c4),
            Boolean("Gadgetron PDA", 0x1d8),
            Boolean("Metal Detector", 0x1d3),
            Boolean("Hologuise", 0x1d7),

            Boolean("Heli-Pack", 0x1ba),
            Boolean("Thruster-Pack", 0x1bb),
            Boolean("Hydro-Pack", 0x1bc),

            Boolean("O2 Mask", 0x1be),
            Boolean("Sonic Summoner", 0x1bd),
            Boolean("Pilot's Helmet", 0x1bf),

            Boolean("Grindboots", 0x1d5),
            Boolean("Magneboots", 0x1d4),
        ],
        "Item unlocks": [
            Boolean("Hoverboard", 0x1d6),
            Boolean("Persuader", 0x1db),
            Boolean("Bolt Grabber", 0x1da),
            Boolean("Map-o-matic", 0x1d9),
        ],
        "Bolt counts": [
            Integer("Number of Bolts", 0x24),
            Integer("Total Bolts Collected", 0x48),
        ],
        "Quick Select": [
            Integer("Slot 1", 0x22c),
            Integer("Slot 2", 0x230),
            Integer("Slot 3", 0x234),
            Integer("Slot 4", 0x238),
            Integer("Slot 5", 0x23c),
            Integer("Slot 6", 0x240),
            Integer("Slot 7", 0x244),
            Integer("Slot 8", 0x248),
        ]
    }
