from enum import Enum

from slimseditor.game.acit import get_acit_items
from slimseditor.game.dl import get_dl_items
from slimseditor.game.gc import get_gc_items
from slimseditor.game.nexus import get_nexus_items
from slimseditor.game.qfb import get_qfb_items
from slimseditor.game.rac import get_rac_items
from slimseditor.game.tod import get_tod_items
from slimseditor.game.uya import get_uya_items


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

    def get_items(self):
        if self == Game.RAC: return get_rac_items()
        if self == Game.GC: return get_gc_items()
        if self == Game.UYA: return get_uya_items()
        if self == Game.DL: return get_dl_items()
        if self == Game.TOD: return get_tod_items()
        if self == Game.QFB: return get_qfb_items()
        if self == Game.ACIT: return get_acit_items()
        if self == Game.NEXUS: return get_nexus_items()
        return dict()
