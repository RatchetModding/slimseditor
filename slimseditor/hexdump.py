#!/usr/bin/env python3

"""
Hexdump by 7hrrAm from https://gist.github.com/7h3rAm/5603718
Based in part on sbz version from https://gist.github.com/sbz/1080258
Modified by maikelwever to make ascii printing optional.
"""

def hexdump(src, length=16, sep='.', print_ascii=True):
  """
  >>> print(hexdump('\x01\x02\x03\x04AAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBB'))
  00000000:  01 02 03 04 41 41 41 41  41 41 41 41 41 41 41 41  |....AAAAAAAAAAAA|
  00000010:  41 41 41 41 41 41 41 41  41 41 41 41 41 41 42 42  |AAAAAAAAAAAAAABB|
  00000020:  42 42 42 42 42 42 42 42  42 42 42 42 42 42 42 42  |BBBBBBBBBBBBBBBB|
  00000030:  42 42 42 42 42 42 42 42                           |BBBBBBBB|
  >>>
  >>> print(hexdump(b'\x01\x02\x03\x04AAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBB'))
  00000000:  01 02 03 04 41 41 41 41  41 41 41 41 41 41 41 41  |....AAAAAAAAAAAA|
  00000010:  41 41 41 41 41 41 41 41  41 41 41 41 41 41 42 42  |AAAAAAAAAAAAAABB|
  00000020:  42 42 42 42 42 42 42 42  42 42 42 42 42 42 42 42  |BBBBBBBBBBBBBBBB|
  00000030:  42 42 42 42 42 42 42 42                           |BBBBBBBB|
  """
  FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256)])
  lines = []
  for c in range(0, len(src), length):
    chars = src[c:c+length]
    hexstr = ' '.join(["%02x" % ord(x) for x in chars]) if type(chars) is str else ' '.join(['{:02x}'.format(x) for x in chars])
    if len(hexstr) > 24:
      hexstr = "%s %s" % (hexstr[:24], hexstr[24:])
    if print_ascii:
      printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or sep) for x in chars]) if type(chars) is str else ''.join(['{}'.format((x <= 127 and FILTER[x]) or sep) for x in chars])
      lines.append("%08x:  %-*s  |%s|" % (c, length*3, hexstr, printable))
    else:
      lines.append("%08x:  %-*s" % (c, length * 3, hexstr))
  return '\n'.join(lines)

if __name__ == "__main__":
  print(hexdump('\x01\x02\x03\x04AAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBB'))
  print(hexdump(b'\x01\x02\x03\x04AAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBB'))
