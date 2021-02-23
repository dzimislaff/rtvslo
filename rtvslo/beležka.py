#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import subprocess


def beležka():
    return subprocess.run(
        ["wl-paste"], capture_output=True, text=True).stdout.strip("\n")
