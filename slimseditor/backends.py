import os

from copy import deepcopy
from struct import Struct

from reloadr import autoreload

from slimseditor.game import ITEMS, Game


class AbstractBackend:
    def __init__(self, path):
        self.path = path
        self.game = Game.ERROR

    def get_friendly_name(self):
        return self.path

    def get_items(self):
        return dict()


PS2_GAME_IDS = {
    Game.RAC: ["SCES-50916", "SCUS-97199", "SCAJ-20001", "SCKA-20120", "SCKA-15037", "SCKA-19211", "SCKA-19316"],
    Game.GC: ["SCES-51607", "SCUS-97268", "SCUS-97513", "SCKA-20011", "SCPS-15056", "SCPS-19302", "SCPS-19317"],
    Game.UYA: ["SCES-52456", "SCUS-97353", "SCUS-97518", "SCAJ-20109", "SCKA-20037", "SCPS-19309", "SCPS-15084"],
    Game.DL: ["SCES-53285", "SCUS-97465", "SCAJ-20157", "SCKA-20060", "SCPS-15100", "SCPS-15099",
              "SCPS-19321", "SCPS-19328"]
}


@autoreload
class PS2BinBackend(AbstractBackend):
    def __init__(self, path):
        self.path = path
        self.game = Game.ERROR
        self.detect_game()
        self.read_data()

    def read_data(self):
        with open(self.path, 'rb') as f:
            self.data = f.read()

    def detect_game(self):
        dirname = os.path.basename(os.path.dirname(self.path))
        game_id = dirname[2:12]
        for game, game_ids in PS2_GAME_IDS.items():
            if game_id in game_ids:
                self.game = game
                return

    def get_items(self):
        items = ITEMS[self.game]()
        for section, section_items in items.items():
            for item in section_items:
                self.read_item(item)

        return items

    def read_item(self, item):
        struct_def = '<{0}'.format(item.struct_type)
        struct_parser = Struct(struct_def)
        item.value, = struct_parser.unpack_from(self.data, item.pos)

    def write_item(self, item):
        pass
