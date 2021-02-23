#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import argparse
import rtvslo.beležka
import rtvslo.nastavitve
import rtvslo.rtv
import os


IME_PROGRAMA = 'rtvslo'

OPIS = f'''
Preprost program, ki dostopa do posnetkov na spletnem portalu rtvslo.si.

Možnosti:
  shrani        shrani posnetek v mapo, v kateri je bil program zagnan
  predvajaj     predvaja posnetek v predvajalniku
  -i, --id      ID številka posnetka
  --pomoč       izpiše to sporočilo - pomoč
Primer rabe:
- predvajaj posnetek
  {IME_PROGRAMA} -p https://4d.rtvslo.si/arhiv/zrcalo-dneva/174612420

  {IME_PROGRAMA} -p --id 174612420

- shrani posnetek
  {IME_PROGRAMA} -s
'''

POMOČ = f'{IME_PROGRAMA} [-h] (-p [PREDVAJAJ] | -s [SHRANI]) [-i ID]'

PRAVICE = 'Vse pravice zaščitene © Nejc 2021'


def ukazi():
    parser = argparse.ArgumentParser(
        prog=IME_PROGRAMA,
        usage=POMOČ,
        description=OPIS,
        epilog=PRAVICE,
        formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers(dest="ukaz")
    subparsers.required = True

    parser_predvajaj = subparsers.add_parser("predvajaj")
    parser_predvajaj.add_argument("povezava", nargs="?", default=None)
    parser_predvajaj.add_argument("--id", action="store", type=int)

    parser_shrani = subparsers.add_parser("shrani")
    parser_shrani.add_argument("povezava", nargs="?", default=None)
    parser_shrani.add_argument("--id", action="store", type=int)

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
    posnetek = rtvslo.rtv.Posnetek(povezava_do_html=ukaz.povezava,
                                   nastavitve=nastavitve,
                                   številka=ukaz.id)

    if ukaz.ukaz == "predvajaj":
        posnetek.predvajaj()
    elif ukaz.ukaz == "shrani":
        # za zaganjanje programa izven domače mape
        CWD = os.getcwd()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))  # je to nujno?

        posnetek.shrani(CWD)


if __name__ == '__main__':
    ukaznavrstica()
