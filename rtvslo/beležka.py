#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import sys


def prepoznaj_operacijski_sistem() -> bool:
    """
    smatram, da je na linuxu waylandova seja, sicer bi bil pyperclip dovolj
    """
    if sys.platform == "linux":
        return True


def beležka():
    if prepoznaj_operacijski_sistem():
        import subprocess
        return subprocess.run(
            ["wl-paste"], capture_output=True, text=True).stdout.strip("\n")
    else:
        import pyperclip
        return pyperclip.paste()
