import json
import os
import pkgutil
import sys

from enum import Enum

from slimseditor.saveentry import RangedInteger, Integer, Boolean, DateTime, UnsignedInteger, UnsignedShort, \
    UnsignedChar, Char, Short, BitField, Combo

ITEM_CLASSES = {
    'RangedInteger': RangedInteger,
    'Integer': Integer,
    'UnsignedInteger': UnsignedInteger,
    'Char': Char,
    'UnsignedChar': UnsignedChar,
    'Short': Short,
    'UnsignedShort': UnsignedShort,
    'Boolean': Boolean,
    'DateTime': DateTime,
    'BitField': BitField,
    'Combo': Combo,
}

if getattr(sys, 'frozen', False):
    APP_PATH = sys._MEIPASS
else:
    APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
        return get_game_items(self)


def get_game_file(game: Game):
    game_filename = '{0}.json'.format(str(game.name).lower())
    possible_game_folder = os.path.join(APP_PATH, 'game')
    if os.path.exists(possible_game_folder) and os.path.isdir(possible_game_folder):
        possible_filename = os.path.join(possible_game_folder, game_filename)
        if os.path.exists(possible_filename):
            with open(possible_filename, 'r') as f:
                return f.read()

    return pkgutil.get_data('slimseditor.game', game_filename).decode('utf-8')


def get_game_items(game: Game):
    json_data = get_game_file(game)
    parsed_data = json.loads(json_data)
    items = dict()
    for key, value in parsed_data.items():
        item_list = []
        for item in value:
            copied_item = item
            item_type = copied_item.pop('type')
            item_list.append(ITEM_CLASSES[item_type](**copied_item))

        items[key] = item_list

    return items
