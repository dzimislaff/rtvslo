#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

# import requests
from lxml import html
import os
import sys
import rtvslo.rtv
import rtvslo.nastavitve

# povezava_do_podcasta = "https://ars.rtvslo.si/odprta-knjiga/"


def pridobi_seznam_povezav(povezava_do_podcasta: str):
    r = rtvslo.rtv.Posnetek.pridobi_spletno_stran(povezava_do_podcasta)
    stran = html.fromstring(r.content)
    konci_povezav = stran.xpath(
        '//h3[@class="post-excerpt__body__title"]/a//@href')
    povezave = [f"https://ars.rtvslo.si{i}" for i in konci_povezav]
    return povezave


def main(povezava_do_podcasta: str):
    nastavitve = rtvslo.nastavitve.naloži_nastavitve()
    cwd = os.getcwd()
    povezave = pridobi_seznam_povezav(povezava_do_podcasta)
    for povezava in povezave:
        posnetek = rtvslo.rtv.Posnetek(povezava, nastavitve)
        posnetek.shrani(cwd)


if __name__ == '__main__':
    main(sys.argv[1])
