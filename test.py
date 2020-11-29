import glob
import json
import os
import sys

from slimseditor import backends
from slimseditor.game import Game


ALL_OK = True


def test_savegame(testfile_data):
    global ALL_OK

    data_path = testfile_data.pop('_path')
    if not data_path:
        print(f'Could not find path of file to examine :( ')
        return

    data_path = os.path.abspath(os.path.join('testdata', data_path))
    backend = testfile_data.pop('_backend')
    game = testfile_data.pop('_game')

    backend_class = getattr(backends, backend)
    if not backend_class:
        print(f'Could not load backend class: {backend_class}')

    game_enum = getattr(Game, game)
    backend_instance = backend_class(data_path, game=game_enum)
    backend_items = backend_instance.get_items()

    for section_name, section_items in backend_items.items():
        test_section = testfile_data.get(section_name)
        if test_section:
            for item in section_items:
                test_value = test_section.get(item.name)
                if test_value:
                    if test_value != item._value:
                        print(f'Test value {test_value} does not equal actual value {item._value}. '
                              f'Section {section_name}, file: {data_path}')
                        ALL_OK = False


def main():
    testdata = os.path.realpath("testdata")
    if not os.path.exists(testdata):
        raise Exception("Could not find 'testdata' folder.")

    json_testfiles = glob.glob(os.path.join(testdata, '*.json'))
    for testfile in json_testfiles:
        with open(testfile, 'r') as f:
            data = json.load(f)

        test_savegame(data)

    global ALL_OK
    if not ALL_OK:
        print(f'Return with exitcode, because some items failed to compare.')
        sys.exit(1)
    else:
        print('All tests OK!')


if __name__ == "__main__":
    main()
