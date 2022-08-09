#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

from lxml import html
import os
import sys
import rtvslo.rtv
import rtvslo.nastavitve


def pridobi_seznam_povezav(povezava_do_podkasta: str
                           ) -> list:

    def ustvari_povezave(ujemanje: str,
                         stran: html.HtmlElement
                         ) -> list:
        # radijski_ključ = '//h3[@class="post-excerpt__body__title"]/a//@href'
        radijski_ključ = '//h4[@class="h4"]/a//@href'
        ključi = {
            "ars": radijski_ključ,
            "prvi": radijski_ključ,
            "val202": radijski_ključ,
            "365": '//h3[@class="title-cut-4-rows"]/a//@href'
        }
        konci_povezav = stran.xpath(ključi[ujemanje])
        return [f"https://{ujemanje}.rtvslo.si{i}" for i in konci_povezav]

    r = rtvslo.rtv.Posnetek.pridobi_spletno_stran(povezava_do_podkasta)
    stran = html.fromstring(r.content)

    if ujemanje := rtvslo.rtv.Posnetek.radio.search(povezava_do_podkasta):
        return ustvari_povezave(ujemanje.group(1), stran)
    elif ujemanje := rtvslo.rtv.Posnetek.štiride.search(povezava_do_podkasta):
        return ustvari_povezave(ujemanje.group(1), stran)
    return []


def main(povezava_do_podkasta: str):
    nastavitve = rtvslo.nastavitve.naloži_nastavitve()
    try:
        cwd = sys.argv[2]
    except IndexError:
        cwd = os.getcwd()
    povezave = pridobi_seznam_povezav(povezava_do_podkasta)

    if povezave:
        for povezava in povezave:
            posnetek = rtvslo.rtv.Posnetek(povezava, nastavitve)
            try:
                posnetek.shrani(cwd)
            except rtvslo.rtv.NeveljavnaPovezava:
                pass
    else:
        print("Neveljavna povezava.")


if __name__ == '__main__':
    main(sys.argv[1])
