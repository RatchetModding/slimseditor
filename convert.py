import os
import json


def convert(items, name):
    filename = os.path.join('slimseditor/game', '{0}.json'.format(name))
    c_items = dict()

    for k, v in items.items():
        c_l = []

        for i in v:
            c_l.append(dict(type=i.__class__.__name__, name=i.name, pos=i.pos))

        c_items[k]=c_l

    with open(filename, 'w') as f:
        json.dump(c_items, f, sort_keys=True, indent=4)

