from reloadr import autoreload

import bimpy


class AbstractSaveEntry:
    struct_type = 'i'

    def render_widget(self):
        pass


@autoreload
class RangedShort(AbstractSaveEntry):
    struct_type = 'H'

    def __init__(self, name, pos, max=100, min=0):
        self.name = name
        self.pos = pos
        self.value = 0
        self.min = min
        self.max = max


@autoreload
class Boolean(AbstractSaveEntry):
    struct_type = '?'

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self._value = False
        self._bimpy_value = bimpy.Bool(False)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._bimpy_value.value = bool(val)

    def render_widget(self):
        bimpy.checkbox(self.name, self._bimpy_value)


@autoreload
class Integer(AbstractSaveEntry):
    struct_type = 'i'

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.value = 0
