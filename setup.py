#!/usr/bin/env python3

from setuptools import setup
from distutils.extension import Extension


slimscbindings = Extension(
    'slimscbindings',
    sources=['slimscbindings.c'],
)

setup(
    name='slimseditor',
    version='0.0.5',
    description='A savegame editor for the Ratchet and Clank games',
    author='Maikel Wever',
    author_email='maikelwever@gmail.com',
    url='https://github.com/maikelwever/slimseditor/',
    packages=['slimseditor'],
    ext_modules=[slimscbindings],
    include_package_data=True,
)
