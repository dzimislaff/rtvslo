#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import pyperclip
import rtvslo.nastavitve
import rtvslo.rtv
import argparse


# za zaganjanje programa izven domače mape
import os
CWD = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))


IME_PROGRAMA = 'rtvslo'

OPIS = f'''
Preprost program, ki dostopa do posnetkov na spletnem portalu rtvslo.si.

Možnosti:
  -s, --shrani      shrani posnetek v mapo, v kateri je bil program zagnan
  -p, --predvajaj   predvaja posnetek v predvajalniku
  -i, --id          ID številka posnetka
  --pomoč           izpiše to sporočilo - pomoč
Primer rabe:
- predvajaj posnetek
  {IME_PROGRAMA} -p https://4d.rtvslo.si/arhiv/zrcalo-dneva/174612420

  {IME_PROGRAMA} -p --id 174612420

- shrani posnetek
  {IME_PROGRAMA} -s
'''

POMOČ = f'{IME_PROGRAMA} [-h] (-p [PREDVAJAJ] | -s [SHRANI]) [-i ID]'

PRAVICE = 'Vse pravice zaščitene © Nejc 2020'


def ukazi():
    parser = argparse.ArgumentParser(
        prog=IME_PROGRAMA,
        usage=POMOČ,
        description=OPIS,
        epilog=PRAVICE,
        formatter_class=argparse.RawTextHelpFormatter)

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-p', '--predvajaj',
                       action='store',
                       type=str,
                       nargs='?',
                       const=1)
    group.add_argument('-s', '--shrani',
                       action='store',
                       type=str,
                       nargs='?',
                       const=1)
    parser.add_argument('-i', '--id',
                        action='store',
                        type=int)
    return parser.parse_args()


def ukaz_razberi(args):
    if args.predvajaj:
        return (rtvslo.rtv.predvajaj_posnetek, args.predvajaj)
    elif args.shrani:
        return (rtvslo.rtv.shrani_posnetek, args. shrani)


def main():
    args = ukazi()
    n = rtvslo.nastavitve.naloži_nastavitve()

    številka = args.id
    povezava_do_html = None

    ukaz = ukaz_razberi(args)

    if ((type(ukaz[1]) == str) and številka):
        raise Exception("Hkrati sta bila podana ID posnetka in povezava.")
    elif type(ukaz[1]) == str:
        povezava_do_html = ukaz[1]
    elif ((ukaz[1] == 1) and not številka):
        povezava_do_html = pyperclip.paste().lower()

    informacije = rtvslo.rtv.pridobi_posnetek(povezava_do_html, n, številka)
    ukaz[0](informacije, n, CWD)


if __name__ == '__main__':
    main()
