import bimpy


class AbstractSaveEntry:
    struct_type = 'i'
    python_type = int
    bimpy_type = bimpy.Int

    def __init__(self, name='', pos=0):
        self.name = name
        self.pos = pos
        self.bimpy_name = '{0}##{1}'.format(name, pos)
        self._value = self.python_type()
        self._bimpy_value = self.bimpy_type()

    @property
    def value(self):
        return self._value

    @property
    def export_value(self):
        return (self._value,)

    @value.setter
    def value(self, val):
        self._value = val[0]
        self._bimpy_value.value = self.python_type(val[0])

    def render_widget(self):
        pass


class RangedInteger(AbstractSaveEntry):
    struct_type = 'i'
    python_type = int
    bimpy_type = bimpy.Int

    def __init__(self, name='', pos=0, max=100, min=0):
        super(RangedInteger, self).__init__(name=name, pos=pos)
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


class DateTime(AbstractSaveEntry):
    struct_type = 'BBBBBBBB'
    python_type = tuple
    bimpy_type = bimpy.String

    @property
    def value(self):
        _, s, i, h, _, d, m, y = self._value
        return f'{y:02X}-{m:02X}-{d:02X} {h:02X}:{i:02X}:{s:02X}'

    @property
    def export_value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._bimpy_value.value = self.value

    def render_widget(self):
        if bimpy.input_text(self.bimpy_name, self._bimpy_value, 20):
            t = self._bimpy_value.value
            his, ymd = t.split(' ')
            h, i, s = his.split(':')
            y, m, d = ymd.split('-')
            self._value = (0, int(s), int(i), int(h), 0, int(d), int(m), int(y))
