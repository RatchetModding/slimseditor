Slim's Editor
=============

A savegame editor for the Ratchet and Clank games, written in Python, using Dear ImGUI via Bimpy for the frontend.

Slim's Editor allows you to read and change any (known) value of a RaC savegame. 
This can also include values that are not exposed by the game itself.

**Always backup your savegames before loading them into Slim's Editor.**

_This project is currently in a inactive and unfinished state. Since starting this, I haven't had much time to work on getting beyond the very basics of the editor._
_If Slim's Editor doesn't work for your savegame, you can try the [previous version](https://github.com/maikelwever/rac-savegame-editor) of the editor to see if that helps._
_Feel free to submit Pull requests with new features/values/fixes/etc._


Supported file formats
----------------------

Currently supported:

 - Raw PS2 save data (.bin), can be extracted with MyMC+ or uLaunchELF.
 - PCSX2 Memory Cards (.ps2)
 - Decrypted PS3 savegame data (RPCS3 or decrypted with BruteForce)
 - Decrypted PS Vita savegames from the OG Trilogy. 
   [Docs for acquiring Vita savegames](https://github.com/maikelwever/rac-savegame-editor/blob/master/docs/HOW-TO-MOVE-SAVES-FOR-VITA.md)
 
 
Supported games
---------------

Currently supported:

 - PS2, PS3, PS Vita
   - Ratchet and Clank
   - Ratchet and Clank 2 : Going Commando
   - Ratchet and Clank 3 : Up Your Arsenal
   - Ratchet: Deadlocked / Gladiator  (Not on Vita)
 - PS3
   - Ratchet and Clank : Tools of Destruction
   - Ratchet and Clank : Quest for Booty
   - Ratchet and Clank : A Crack in Time
   - Ratchet and Clank : (Into the) Nexus
   
   
Installation / Usage
--------------------

For Windows, get the prebuilt versions from the Releases tab on GitHub.
Simply unzip the release, and run `slimseditor.exe`.

For Linux (package names are for Debian/Ubuntu):

Install `python3 python3-dev python3-venv build-essential`. 
Install `zenity` (or `kdialog` if you are on KDE).

```bash
git clone https://github.com/maikelwever/slimseditor
cd slimseditor
python3 -m venv env
env/bin/pip install -r requirements.txt
env/bin/python setup.py develop
env/bin/python -m slimseditor
```


Adding savegame items
---------------------

Savegame item positions are defined by `.json` files in `slimseditor/game`.
For prebuilt editions, these files are bundled with the application data.

To submit new items, or change existing item definitions, 
simply edit the appropriate lines in the `.json` files.
The editor will re-read the `.json` files every time you open a savegame or click a `refresh` button.

If you are working with a prebuilt edition, 
you can create a folder called `game` in the directory `slimseditor.exe` is in.
The editor will then search for game files in this directory instead.
To get started with this, download the `.json` file for the game you're editing from GitHub,
and put it in your new `game` folder. 


Roadmap
-------

Wishlist of features to port from the previous editor or add new:

 - PS3 savegame decryption and proper re-encryption.


Legal stuff
-----------

This project is licensed under the GNU General Public License v3.0. Please see the LICENSE file for more details.
