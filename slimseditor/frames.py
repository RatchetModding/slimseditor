from collections import defaultdict
from io import BytesIO

import bimpy
import crossfiledialog

from mymcplus import ps2mc

from slimseditor.backends import AbstractBackend, PS2WrappedBinBackend
from slimseditor.reloadmagic import autoreload

counter = 0


def get_next_count():
    global counter
    value, counter = counter, counter + 1
    return value


class FrameBase:
    def __init__(self):
        self._size = None
        self.opened = bimpy.Bool(True)
        self.click_states = defaultdict(bimpy.Bool)

    def render(self):
        if not self._size:
            self._size = bimpy.Vec2(400, 600)
            bimpy.set_next_window_size(self._size)

    def process_events(self):
        pass


class SaveGameFrame(FrameBase):
    def __init__(self, backend_class, *backend_args, **backend_kwargs):
        super(SaveGameFrame, self).__init__()
        self.backend_class = backend_class
        self.backend_args = backend_args
        self.backend_kwargs = backend_kwargs
        self.load_backend()

        self.name = '{0}##{1}'.format(self.backend.get_friendly_name(), get_next_count())

    def load_backend(self):
        self.backend = self.backend_class(*self.backend_args, **self.backend_kwargs)  # type: AbstractBackend
        try:
            self.items = self.backend.get_items()
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            self.items = dict()
            print(str(e))

    def render(self):
        super(SaveGameFrame, self).render()
        if bimpy.begin(self.name, self.opened,
                       flags=bimpy.WindowFlags.NoCollapse | bimpy.WindowFlags.MenuBar):

            if bimpy.begin_menu_bar():
                bimpy.menu_item('Save', 'Cmd+S', self.click_states['save'])
                bimpy.menu_item('Reload', 'Cmd+R', self.click_states['reload'])
                bimpy.menu_item('Export', 'Cmd+E', self.click_states['export'])
                bimpy.end_menu_bar()

            bimpy.text('Game: ')
            bimpy.same_line()
            bimpy.text(self.backend.game.value)

            for section_name, section_items in self.items.items():
                if bimpy.collapsing_header(section_name):
                    for item in section_items:
                        item.render_widget()

            bimpy.end()

    def process_events(self):
        if self.click_states['save'].value:
            self.backend.write_all_items(self.items)
            self.backend.write_data()
            self.click_states['save'].value = False

        if self.click_states['reload'].value:
            self.load_backend()
            self.click_states['reload'].value = False

        if self.click_states['export'].value:
            filename = crossfiledialog.save_file()
            if filename:
                with open(filename, 'wb') as f:
                    f.write(self.backend.data)

            self.click_states['export'].value = False


@autoreload
class PS2MCFrame(FrameBase):
    NAME_EXCLUSIONS = [b'.', b'..']

    def __init__(self, path):
        self._size = None
        self.opened = bimpy.Bool(True)
        self.click_states = defaultdict(bimpy.Bool)

        self.path = path
        self.name = '{0}##{1}'.format(path, get_next_count())
        self.child_frames = []
        self.tree = dict()
        self.load_card_data()

    def load_card_data(self):
        with open(self.path, 'rb') as f:
            self.data = BytesIO(f.read())

        self.card = ps2mc.ps2mc(self.data)
        self.tree = dict()
        root_dir = self.card.dir_open('/')
        for entry in root_dir:
            if not ps2mc.mode_is_dir(entry[0]):
                continue

            if entry[-1] not in self.NAME_EXCLUSIONS:
                dirname = entry[-1].decode('ascii')
                subnames = []
                dir_files = self.card.dir_open(dirname)
                for file_entry in dir_files:
                    if file_entry[-1] in self.NAME_EXCLUSIONS:
                        continue

                    decoded_name = file_entry[-1].decode('ascii')
                    if decoded_name.endswith('bin'):
                        subnames.append((
                            decoded_name,
                            'Open##{0}/{1}'.format(dirname, decoded_name)
                        ))

                self.tree[dirname] = subnames
                dir_files.close()

        root_dir.close()

    def write_card_data(self):
        self.card.flush()
        with open(self.path, 'wb') as f:
            self.data.seek(0)
            f.write(self.data.read())

    def render(self):
        if not self._size:
            self._size = bimpy.Vec2(400, 600)
            bimpy.set_next_window_size(self._size)

        if bimpy.begin(self.name, self.opened,
                       flags=bimpy.WindowFlags.NoCollapse | bimpy.WindowFlags.MenuBar):

            if bimpy.begin_menu_bar():
                bimpy.menu_item('Reload', 'Cmd+R', self.click_states['reload'])
                bimpy.end_menu_bar()

            for folder_name, folder_files in self.tree.items():
                if bimpy.collapsing_header(folder_name):
                    for item, button_name in folder_files:
                        if bimpy.button(button_name):
                            item_path = '{0}/{1}'.format(folder_name, item)
                            try:
                                new_savegame = SaveGameFrame(
                                    PS2WrappedBinBackend, item_path, self)
                                self.child_frames.append(new_savegame)

                            except KeyboardInterrupt as e:
                                raise e
                            except Exception as e:
                                print(e)

                        bimpy.same_line()
                        bimpy.text(item)

            bimpy.end()

            for child_frame in self.child_frames:
                child_frame.render()

    def process_events(self):
        if self.click_states['reload'].value:
            self.load_card_data()
            self.click_states['reload'].value = False

        for child_frame in self.child_frames:
            child_frame.process_events()

        open_frames_to_close = []
        for i, frame in enumerate(self.child_frames):
            if not frame.opened.value:
                open_frames_to_close.append(i)

        for i in sorted(open_frames_to_close, reverse=True):
            del self.child_frames[i]
