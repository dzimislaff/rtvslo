#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

from rtvslo import pridobi_api, pridobi_json, info_json
import pyperclip
import subprocess
import nastavitve


def main():
    n = nastavitve.naloži_nastavitve()
    povezava_do_html = pyperclip.paste().lower()
    povezava_do_api = pridobi_api(povezava_do_html, n)[0]
    informacije = info_json(pridobi_json(povezava_do_api, n))
    povezava = informacije[0]
    subprocess.call(['mpv', povezava, '--force-window'])


if __name__ == '__main__':
    main()
