import sys

from collections import defaultdict

import bimpy
import filedialog

from reloadr import autoreload

from slimseditor.backends import PS2BinBackend
from slimseditor.savegame import SaveGame


click_states = defaultdict(bimpy.Bool)
open_savegames = []  # type: List[SaveGame]


@autoreload
def render_menu_bar():
    if bimpy.begin_main_menu_bar():
        if bimpy.begin_menu('File'):
            bimpy.menu_item('Quit', 'Cmd+Q', click_states['file_quit'])
            if click_states['file_quit'].value:
                sys.exit(0)

            bimpy.end_menu()

        if bimpy.begin_menu('Open'):
            bimpy.menu_item("PS2 .bin file", '', click_states['open_ps2_bin'])

            bimpy.end_menu()

        bimpy.end_main_menu_bar()


@autoreload
def process_menu_bar_events():
    if click_states['open_ps2_bin'].value:
        path = filedialog.open_file()
        if path:
            try:
                new_savegame = SaveGame(path, PS2BinBackend)
                open_savegames.append(new_savegame)
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                print(e)

        click_states['open_ps2_bin'].value = False


def main():
    ctx = bimpy.Context()
    ctx.init(600, 600, "Slim's Editor")

    default_window_size = bimpy.Vec2(400, 300)
    with ctx:
        bimpy.set_next_window_size(default_window_size)

    while not ctx.should_close():
        with ctx:
            render_menu_bar()

            for savegame in open_savegames:
                savegame.render()

        process_menu_bar_events()
        for savegame in open_savegames:
            savegame.process_events()

        savegames_to_close = []
        for i, savegame in enumerate(open_savegames):
            if not savegame.opened.value:
                savegames_to_close.append(i)

        for i in sorted(savegames_to_close, reverse=True):
            del open_savegames[i]


if __name__ == "__main__":
    main()
