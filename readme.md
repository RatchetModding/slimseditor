Slim's Editor
=============

A savegame editor for the Ratchet and Clank games, written in Python.

Currently under heavy development, **backup** your savegames before loading them into Slim's Editor.


About
-----

A more extended written description will be put here soon (tm).


Installation
------------

For Windows, get the prebuilt versions from the Releases tab on GitHub.
Simply unzip the release, and run `slimseditor.exe`.

For Linux (package names are for Debian/Ubuntu):

Install `python3 python3-dev python3-venv build-essential`. 
Install `zenity` (or `kdialog` if you are on KDE).

```bash
git clone https://github.com/maikelwever/slimseditor
cd slimseditor
python -m venv env
env/bin/pip install -r requirements.txt
env/bin/python setup.py develop
env/bin/python -m slimseditor
```
