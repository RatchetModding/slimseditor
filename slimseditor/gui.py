import os
import sys

from collections import defaultdict

import bimpy
import crossfiledialog

from slimseditor.backends import PS2BinBackend, PS3Backend
from slimseditor.reloadmagic import autoreload
from slimseditor.frames import FrameBase, SaveGameFrame, PS2MCFrame

click_states = defaultdict(bimpy.Bool)
open_frames = []  # type: List[FrameBase]


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


def open_savegame(backend, *args, **kwargs):
    try:
        new_savegame = SaveGameFrame(backend, *args, **kwargs)
        open_frames.append(new_savegame)
        return new_savegame
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        print(e)


@autoreload
def process_menu_bar_events():
    if click_states['open_ps2_bin'].value:
        path = crossfiledialog.open_file()
        if path:
            open_savegame(PS2BinBackend, path)

        click_states['open_ps2_bin'].value = False


def process_envvars():
    ps2_bin = os.environ.get('OPEN_PS2BIN', '')
    if ps2_bin:
        for path in ps2_bin.split(':'):
            open_savegame(PS2BinBackend, path)

    ps2_mc = os.environ.get('OPEN_PS2MC', '')
    if ps2_mc:
        for path in ps2_mc.split(':'):
            try:
                open_frames.append(PS2MCFrame(path))
            except KeyboardInterrupt as e:
                raise e

    ps3_savegames = os.environ.get('OPEN_PS3', '')
    if ps3_savegames:
        for path in ps3_savegames.split(':'):
            open_savegame(PS3Backend, path)


def main():
    process_envvars()
    ctx = bimpy.Context()
    ctx.init(600, 800, "Slim's Editor")

    while not ctx.should_close():
        with ctx:
            render_menu_bar()

            for frame in open_frames:
                frame.render()

        process_menu_bar_events()
        for frame in open_frames:
            frame.process_events()

        open_frames_to_close = []
        for i, frame in enumerate(open_frames):
            if not frame.opened.value:
                open_frames_to_close.append(i)

        for i in sorted(open_frames_to_close, reverse=True):
            del open_frames[i]


if __name__ == "__main__":
    main()
