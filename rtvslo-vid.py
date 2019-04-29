#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

from rtvslo import pridobi_api, pridobi_json, info_json
import pyperclip
import subprocess


def main():
    povezava_do_html = pyperclip.paste().lower()
    povezava_do_api = pridobi_api(povezava_do_html)[0]
    informacije = info_json(pridobi_json(povezava_do_api))
    povezava = informacije[0]
    subprocess.call(['mpv', povezava, '--force-window'])

if __name__ == '__main__':
    main()
