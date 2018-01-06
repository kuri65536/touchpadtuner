TouchPad Tuning tool for Lxde (xinput)
===============================================================================
Sometime, I face the problem of TouchPad configuration in Lubuntu.
My laptop have too sensitive TouchPad.

This tool configure the touchpad through xinput with GUI,
and no need to gnome or another heavy environment/dependencies.


Requirement
-----------------------------------------
### In lubuntu

for Python3

```
$ sudo apt intall python3
$ sudo apt intall python3-tk
$ sudo apt intall xf86-input-synaptics
```

for Python2

```
$ sudo apt intall python
$ sudo apt intall python-tk
$ sudo apt intall xf86-input-synaptics
```


How to use
-----------------------------------------
```
$ git clone https://github.com/kuri65536/touchpadtuner.git
$ cd touchpadtuner
$ python touchpadtuner2.py
```


TODO
-----------------------------------------
- Write down or modify file: `/usr/share/X11/xorg.conf.d/70-synaptic.conf`,
    to make the changes to permanent.
- Made GUI for some missing params. (
    I solved the sensitive touchpad with FingerLow and FingerHigh parameters.
    I don't use another params.
    )
- (my touchpad problem) Incorrect scroll up/down in typing.
- (my touchpad problem) Syndaemon stop with two finger scroll.


Development Environment
-----------------------------------------

| term | description   |
|:----:|:--------------|
| OS   | Lubuntu 17.10 |
| Xorg | 1.19.5        |
| lang | Python 3.6.2, Python 2.7.14  |
| tool | xinput 1.6.2 (XI server 2.3) |
| tool | tkinter       |

I really don't know and don't have wayland environment.


Hardwares
-----------------------------------------

| term        | description   |
|:-----------:|:--------------|
| ASUS E203NA | as development machine |


Reference
-----------------------------------------
- https://wiki.archlinux.org/index.php/Touchpad_Synaptics
- https://help.ubuntu.com/community/SynapticsTouchpad


License
-----------------------------------------
see the top of source code, it is Modified BSD.


Screenshot
-----------------------------------------
![screen shot](https://github.com/kuri65536/touchpadtuner/blob/document-resources/screenshot-1.png)

<!--
vi: ft=markdown:et:fdm=syntax
-->
