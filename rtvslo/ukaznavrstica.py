#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import argparse
import rtvslo.beležka
import rtvslo.nastavitve
import rtvslo.rtv
import os
from __version__ import __version__


IME_PROGRAMA = "rtvslo"

OPIS = f"""
Preprost program, ki dostopa do posnetkov na spletnem portalu rtvslo.si.

Možnosti:
  shrani        shrani posnetek v mapo, v kateri je bil program zagnan
  predvajaj     predvaja posnetek v predvajalniku
  --id          ID številka posnetka
  --pomoč       izpiše to sporočilo – pomoč

Primer rabe:
– predvajaj posnetek
  {IME_PROGRAMA} predvajaj https://4d.rtvslo.si/arhiv/zrcalo-dneva/174612420

  {IME_PROGRAMA} predvajaj --id 174612420

– shrani posnetek
  {IME_PROGRAMA} shrani
"""

POMOČ = f"{IME_PROGRAMA} [-h] [--verzija] predvajaj/shrani [--id]"

PRAVICE = "Vse pravice zaščitene © Nejc 2021"


def ukazi():
    parser = argparse.ArgumentParser(
        prog=IME_PROGRAMA,
        usage=POMOČ,
        description=OPIS,
        epilog=PRAVICE,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--verzija", action="version",
                        version="%(prog)s {version}".format(version=__version__))

    subparsers = parser.add_subparsers(dest="ukaz")
    subparsers.required = True

    parser_predvajaj = subparsers.add_parser("predvajaj")
    parser_predvajaj.add_argument("povezava", nargs="?", default=None)
    parser_predvajaj.add_argument("--id", action="store", type=int)

    parser_shrani = subparsers.add_parser("shrani")
    parser_shrani.add_argument("povezava", nargs="?", default=None)
    parser_shrani.add_argument("--id", action="store", type=int)

    parser_izpiši = subparsers.add_parser("izpiši")
    parser_izpiši.add_argument("povezava", nargs="?", default=None)
    parser_izpiši.add_argument("--id", action="store", type=int)

    return (parser.parse_args(),  # ukaz
            parser)               # parser


def ukaznavrstica():
    izbrani_ukazi = ukazi()
    ukaz = izbrani_ukazi[0]
    parser = izbrani_ukazi[1]

    if not ukaz.povezava and not ukaz.id:
        ukaz.povezava = rtvslo.beležka.beležka()
    elif ukaz.povezava and ukaz.id:
        parser.error("Hkrati sta bila podana povezava in ID posnetka.")

    nastavitve = rtvslo.nastavitve.naloži_nastavitve()
    try:
        posnetek = rtvslo.rtv.Posnetek(povezava_do_html=ukaz.povezava,
                                       nastavitve=nastavitve,
                                       številka=ukaz.id)
    except rtvslo.rtv.NeveljavnaPovezava:
        print("Povezava je neveljavna.")
    else:
        if ukaz.ukaz == "predvajaj":
            try:
                posnetek.predvajaj()
            except rtvslo.rtv.NeveljavnaPovezava:
                print("Povezava je neveljavna.")
        elif ukaz.ukaz == "shrani":
            # za zaganjanje programa izven domače mape
            cwd = os.getcwd()
            # je to nujno?
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
            try:
                posnetek.shrani(cwd)
            except rtvslo.rtv.NeveljavnaPovezava:
                print("Povezava je neveljavna.")
        elif ukaz.ukaz == "izpiši":
            try:
                posnetek.start()
                print(posnetek.povezava_do_posnetka)
            except rtvslo.rtv.NeveljavnaPovezava:
                print("Povezava je neveljavna.")


if __name__ == '__main__':
    ukaznavrstica()
