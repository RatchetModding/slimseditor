import bimpy


class AbstractSaveEntry:
    struct_type = 'i'
    python_type = int
    bimpy_type = bimpy.Int

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.bimpy_name = '{0}##{1}'.format(name, pos)
        self._value = self.python_type()
        self._bimpy_value = self.bimpy_type()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._bimpy_value.value = self.python_type(val)

    def render_widget(self):
        pass


class RangedShort(AbstractSaveEntry):
    struct_type = 'H'
    python_type = int
    bimpy_type = bimpy.Int

    def __init__(self, name, pos, max=100, min=0):
        super(RangedShort, self).__init__(name, pos)
        self.min = min
        self.max = max

    def render_widget(self):
        if bimpy.slider_int(self.bimpy_name, self._bimpy_value, self.min, self.max):
            self._value = self._bimpy_value.value


class Boolean(AbstractSaveEntry):
    struct_type = '?'
    python_type = bool
    bimpy_type = bimpy.Bool

    def render_widget(self):
        if bimpy.checkbox(self.bimpy_name, self._bimpy_value):
            self._value = self._bimpy_value.value


class Integer(AbstractSaveEntry):
    struct_type = 'i'
    python_type = int
    bimpy_type = bimpy.Int

    def render_widget(self):
        if bimpy.input_int(self.bimpy_name, self._bimpy_value):
            self._value = int(self._bimpy_value.value)
