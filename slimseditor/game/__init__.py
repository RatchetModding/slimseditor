from enum import Enum

from slimseditor.game.rac import get_rac_items


class Game(Enum):
    ERROR = "Game version could not be properly detected."
    RAC = "Ratchet and Clank"
    GC = "Ratchet and Clank 2 : Going Commando"
    UYA = "Ratchet and Clank 3 : Up Your Arsenal"
    DL = "Ratchet : Deadlocked / Gladiator"
    TOD = "Ratchet and Clank Future : Tools of Destruction"
    QFB = "Ratchet and Clank Future : Quest for Booty"
    ACIT = "Ratchet and Clank Future : A Crack in Time"
    NEXUS = "Ratchet and Clank : Into the Nexus"


ITEMS = {
    Game.RAC: get_rac_items,
}

