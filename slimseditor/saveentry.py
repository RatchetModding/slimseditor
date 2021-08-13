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
    min = 0
    max = 100

    def __init__(self, name='', pos=0, max=max, min=min):
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


class UnsignedInteger(Integer):
    struct_type = 'I'


class Char(Integer):
    struct_type = 'b'


class UnsignedChar(Integer):
    struct_type = 'B'


class Short(Integer):
    struct_type = 'h'


class UnsignedShort(Integer):
    struct_type = 'H'


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


class BitField(AbstractSaveEntry):
    struct_type = 'B'
    python_type = int
    bitmap = dict()
    bitmap_values = dict()

    def __init__(self, name='', pos=0, bitmap=None):
        super(BitField, self).__init__(name, pos)
        if bitmap is not None:
            self.bitmap = bitmap
        else:
            self.bitmap = dict()

        self.bitmap_values = dict()

    def _test_bit(self, offset):
        mask = 1 << offset
        return (self._value & mask)

    def _set_bit(self, offset):
        mask = 1 << offset
        self._value = (self._value | mask)

    def _clear_bit(self, offset):
        mask = ~(1 << offset)
        self._value = (self._value & mask)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val[0]
        for key, pos in self.bitmap.items():
            self.bitmap_values[key] = bimpy.Bool(self._test_bit(pos))

    def render_widget(self):
        for key, pos in self.bitmap.items():
            if bimpy.checkbox(key, self.bitmap_values[key]):
                if self.bitmap_values[key]:
                    self._set_bit(pos)
                else:
                    self._clear_bit(pos)
