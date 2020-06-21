from slimseditor.reloadmagic import autoreload
from slimseditor.saveentry import RangedShort, Boolean, Integer


@autoreload
def get_uya_items():
    return {
        "Bolt counts": [
            Integer("Number of Bolts", 0x24),
        ],
        "Item Unlocks": [
            Boolean("Heli Pack", 0x4aa),
            Boolean("Thruster Pack", 0x4ab),
            Boolean("Hydro Pack", 0x4ac),
            Boolean("Map-o-matic", 0x4ad),
            Boolean("Commando Suit", 0x4ae),
            Boolean("Bolt Grabber v2", 0x4af),
            Boolean("Levitator", 0x4b0),
            Boolean("Omniwrench", 0x4b1),
            Boolean("Hypershot", 0x4b3),
            Boolean("Gravity Boots", 0x4b5),
            Boolean("Plasma Coil", 0x4b8),
            Boolean("Lava Gun", 0x4b9),
            Boolean("Refractor", 0x4ba),
            Boolean("Bouncer", 0x4bb),
            Boolean("The Hacker", 0x4bc),
            Boolean("Miniturret", 0x4bd),
            Boolean("Shield Charger", 0x4be),
            Boolean("Charge Boots", 0x4c5),
            Boolean("Thyrra Guise", 0x4c6),
            Boolean("Warp Pad", 0x4c7),
            Boolean("Nano Pak", 0x4c8),
            Boolean("Star Map", 0x4ca),
            Boolean("Master Plan", 0x4cb),
            Boolean("PDA", 0x4cc),
            Boolean("Third Person Mode", 0x4cc),
            Boolean("First Person Mode", 0x4cd),
            Boolean("Lock-Strafe Mode", 0x4ce),
        ],
        "Weapon Ammo": [
            Integer("Shock Blaster", 0x2cc),
            Integer("N60 Storm", 0x2ec),
            Integer("Infector", 0x30c),
            Integer("Annihilator", 0x32c),
            Integer("Spitting Hydra", 0x34c),
            Integer("Disc Blade Gun", 0x36c),
            Integer("Agents of Doom", 0x38c),
            Integer("Rift Inducer", 0x3ac),
            Integer("Holoshield", 0x3cc),
            Integer("Flux Rifle", 0x3ec),
            Integer("Nitro Launcher", 0x40c),
            Integer("Plasma Whip", 0x42c),
            Integer("Quack-O-Ray", 0x46c),
            Integer("R3YNO", 0x48c),
        ],
        "Weapon EXP": [
            Integer("Shock Blaster", 0x68c),
            Integer("N60 Storm", 0x6ac),
            Integer("Infector", 0x6cc),
            Integer("Annihilator", 0x6ec),
            Integer("Spitting Hydra", 0x70c),
            Integer("Disc Blade Gun", 0x72c),
            Integer("Agents of Doom", 0x74c),
            Integer("Rift Inducer", 0x76c),
            Integer("Holoshield", 0x78c),
            Integer("Flux Rifle", 0x7ac),
            Integer("Nitro Launcher", 0x7cc),
            Integer("Plasma Whip", 0x7ec),
            Integer("Quack-O-Ray", 0x80c),
            Integer("R3YNO", 0x84c),
        ],
        "Weapon Unlocks": [
            Boolean("Shock Blaster V1", 0x4cf),
            Boolean("N60 Storm V1", 0x4d7),
            Boolean("Infector V1", 0x4df),
            Boolean("Annihilator V1", 0x4e7),
            Boolean("Spitting Hydra V1", 0x4ef),
            Boolean("Disc Blade Gun V1", 0x4f7),
            Boolean("Agents of Doom V1", 0x4ff),
            Boolean("Rift Inducer V1", 0x507),
            Boolean("Holoshield V1", 0x50f),
            Boolean("Flux Rifle V1", 0x517),
            Boolean("Nitro Launcher V1", 0x51f),
            Boolean("Plasma Whip V1", 0x527),
            Boolean("Quack-O-Ray V1", 0x52f),
            Boolean("R3YNO V1", 0x53f),
        ],
        "Misc": [
            Boolean("Enable Quick Select Pause", 0x2c26),
        ],
    }
