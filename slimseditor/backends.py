import os
import struct

import slimscbindings

from slimseditor.game import Game


class AbstractBackend:
    def __init__(self, path):
        self.data = bytearray()
        self.path = path
        self.game = Game.ERROR

    def get_friendly_name(self):
        return self.path

    def get_items(self):
        items = self.game.get_items()
        for section, section_items in items.items():
            for item in section_items:
                self.read_item(item)

        return items

    def read_data(self):
        pass

    def write_data(self):
        pass

    def write_all_items(self, items):
        for section, section_items in items.items():
            for item in section_items:
                self.write_item(item)

    def read_item(self, item):
        pass

    def write_item(self, item):
        pass


class SingleLittleEndianFileMixin:
    def read_data(self):
        with open(self.path, 'rb') as f:
            self.data = bytearray(f.read())

    def write_data(self):
        with open(self.path, 'wb') as f:
            f.write(self.data)

    def read_item(self, item):
        struct_def = '<{0}'.format(item.struct_type)
        item.value, = struct.unpack_from(struct_def, self.data, item.pos)

    def write_item(self, item):
        struct_def = '<{0}'.format(item.struct_type)
        struct.pack_into(struct_def, self.data, item.pos, item.value)


PS2_GAME_IDS = {
    Game.RAC: ["SCES-50916", "SCUS-97199", "SCAJ-20001", "SCKA-20120", "SCKA-15037", "SCKA-19211", "SCKA-19316"],
    Game.GC: ["SCES-51607", "SCUS-97268", "SCUS-97513", "SCKA-20011", "SCPS-15056", "SCPS-19302", "SCPS-19317"],
    Game.UYA: ["SCES-52456", "SCUS-97353", "SCUS-97518", "SCAJ-20109", "SCKA-20037", "SCPS-19309", "SCPS-15084"],
    Game.DL: ["SCES-53285", "SCUS-97465", "SCAJ-20157", "SCKA-20060", "SCPS-15100", "SCPS-15099",
              "SCPS-19321", "SCPS-19328"]
}


class PS2BinBackend(SingleLittleEndianFileMixin, AbstractBackend):
    def __init__(self, path):
        super(PS2BinBackend, self).__init__(path)
        self.detect_game()
        self.read_data()

    def write_data(self):
        self.calculate_checksum()
        super(PS2BinBackend, self).write_data()

    def calculate_checksum(self):
        result = slimscbindings.calculate_checksum(self.data)
        self.data = result

    def detect_game(self):
        dirname = os.path.basename(os.path.dirname(self.path))
        game_id = dirname[2:12]
        for game, game_ids in PS2_GAME_IDS.items():
            if game_id in game_ids:
                self.game = game
                return


class PS2WrappedBinBackend(PS2BinBackend):
    def __init__(self, path, wrapper):
        self.wrapper = wrapper
        self.name = '{0} in {1}'.format(path, wrapper.name)
        super(PS2WrappedBinBackend, self).__init__(path)

    def get_friendly_name(self):
        return self.name

    def read_data(self):
        card_file = self.wrapper.card.open(self.path, 'rb')
        self.data = bytearray(card_file.read())
        card_file.close()

    def write_data(self):
        self.calculate_checksum()
        card_file = self.wrapper.card.open(self.path, 'wb')
        card_file.write(self.data)
        card_file.close()
        self.wrapper.write_card_data()


class PSVitaDecryptedBackend(SingleLittleEndianFileMixin, AbstractBackend):
    def __init__(self, path):
        super(PSVitaDecryptedBackend, self).__init__(path)
        self.detect_game()
        self.read_data()

    def detect_game(self):
        filename = os.path.basename(self.path)
        if filename.startswith("RC1_"):
            self.game = Game.RAC
        elif filename.startswith("RC2_"):
            self.game = Game.GC
        elif filename.startswith("RC3_"):
            self.game = Game.UYA


PS3_GAME_IDS = {
    Game.RAC: ["NPEA00385", "NPUA80643", "NPJA40001"],
    Game.GC: ["NPEA00386", "NPUA80644", "NPJA40002"],
    Game.UYA: ["NPEA00387", "NPUA80645", "NPJA40003"],
    Game.DL: ["NPEA00423"],
    Game.TOD: [
        "BCAS20045", "BCES00052", "NPUA98153",
        "BCJS30014", "BCJS70004", "BCJS70012",
        "BCKS10016", "BCKS10054", "BCUS98127",
        "NPEA90017", "NPHA20002", "NPJA90035",
    ],
    Game.QFB: [
        "BCUS98187", "NPUA80145", "BLES00301",
        "NPEA00088", "BCES00301"
    ],
    Game.ACIT: [
        "BCUS98124", "BCES00142", "BCES00511", "BCES00748",
        "BCES00726", "BCJS30038", "BCKS10087", "BCAS20098",
    ],
    Game.NEXUS: [
        "XCES00008", "BCES01908", "BCUS99245", "BCES01949", "NPEA00457",
    ],
}


def get_ps3_key(game):
    if game == Game.RAC:
        return '01020304050607FACB0A0B0C0D0E0F10'
    elif game == Game.GC:
        return 'C0A3B3641C2AD1EF23153A48A3E12FE8'
    elif game == Game.UYA:
        return 'C0A3B3641C2AD1EF23153A48A3E12FE7'
    else:
        return 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'


USR_DATA_GAMES = [Game.RAC, Game.GC, Game.UYA, Game.DL]


class PS3DecryptedBackend(AbstractBackend):
    def __init__(self, path):
        super(PS3DecryptedBackend, self).__init__(path)
        self.detect_game()
        self.read_data()

    def read_data(self):
        data_file = os.path.join(self.path, self.get_filename())
        with open(data_file, 'rb') as f:
            self.data = bytearray(f.read())

    def read_item(self, item):
        struct_def = '>{0}'.format(item.struct_type)
        item.value, = struct.unpack_from(struct_def, self.data, item.pos)

    def write_item(self, item):
        struct_def = '>{0}'.format(item.struct_type)
        struct.pack_into(struct_def, self.data, item.pos, item.value)

    def get_filename(self):
        if self.game in USR_DATA_GAMES:
            return 'USR-DATA'
        return 'GAME.SAV'

    def match_region_to_game(self, region):
        for game, game_ids in PS3_GAME_IDS.items():
            if region in game_ids:
                self.game = game
                return

    def detect_game(self):
        dirname = os.path.basename(self.path)
        try:
            region = dirname.split('_')[0]
            self.match_region_to_game(region)
        except IndexError:
            pass

        if self.game == Game.ERROR:
            with open(os.path.join(self.path, 'PARAM.SFO'), 'rb') as f:
                f.seek(0x968)
                region_sfo = f.read(9).decode('ascii')

            self.match_region_to_game(region_sfo)
