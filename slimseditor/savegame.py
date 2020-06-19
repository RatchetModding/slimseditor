from collections import defaultdict

import bimpy

from slimseditor.backends import AbstractBackend
from slimseditor.reloadmagic import autoreload


counter = 0


def get_next_count():
    global counter
    value, counter = counter, counter + 1
    return value


@autoreload
class SaveGame:
    def __init__(self, path, backend_class=None):
        self._size = None
        self.path = path
        self.backend_class = backend_class
        self.load_backend()

        self.name = '{0}##{1}'.format(self.backend.get_friendly_name(), get_next_count())
        self.opened = bimpy.Bool(True)
        self.click_states = defaultdict(bimpy.Bool)

    def load_backend(self):
        self.backend = self.backend_class(self.path)  # type: AbstractBackend
        try:
            self.items = self.backend.get_items()
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            self.items = dict()
            print(str(e))

    def render(self):
        if not self._size:
            self._size = bimpy.Vec2(400, 600)
            bimpy.set_next_window_size(self._size)

        if bimpy.begin(self.name, self.opened,
                       flags=bimpy.WindowFlags.NoCollapse | bimpy.WindowFlags.MenuBar):

            if bimpy.begin_menu_bar():
                bimpy.menu_item('Save', 'Cmd+S', self.click_states['save'])
                bimpy.menu_item('Reload', 'Cmd+R', self.click_states['reload'])
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
