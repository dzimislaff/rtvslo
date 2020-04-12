#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

from sys import argv
import pyperclip
import nastavitve
import rtvslo

# za zaganjanje programa izven domače mape
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


IME_PROGRAMA = 'rtvslo.py'


def ukazna_vrstica():
    '''
    vhod: (sys.)argv
    izhod: povezava do spletne strani in uporabnikov vnos v ukazni vrstici
    ukaz analizira uporabnikov vnos v ukazni vrstici; v primeru neustreznega
    ukaza izpiše sporočilo o rabi programa
    '''
    sporočilo_raba = f'''
    Uporaba: {IME_PROGRAMA} [izbira] [povezava]

    Za pomoč vtipkaj: {IME_PROGRAMA} --pomoč
    '''

    sporočilo_pomoč = f'''
    Preprost program, ki dostopa do posnetkov na spletnem portalu rtvslo.si.

    Možnosti:
      -s, --shrani      shrani posnetek v mapo, v kateri je bil program zagnan
      -p, --predvajaj   predvaja posnetek v predvajalniku
      --pomoč           izpiše to sporočilo - pomoč

    Primer rabe:
    - predvajaj posnetek
      {IME_PROGRAMA} -p https://4d.rtvslo.si/arhiv/zrcalo-dneva/174612420

    - shrani posnetek
      {IME_PROGRAMA}
    '''
    pomoč = ['-h', '--help', 'pomoč', '--pomoč']
    povezava_do_html = None
    ukaz = rtvslo.shrani_posnetek
    if (len(argv) == 1):
        povezava_do_html = pyperclip.paste().lower()
    elif (len(argv) == 2) and ('-p' in argv[1] or '-s' in argv[1]):
        povezava_do_html = pyperclip.paste().lower()
        if argv[1] == '-p':
            ukaz = rtvslo.predvajaj_posnetek
    elif argv[1] == '-p' and len(argv) == 3:
        povezava_do_html = argv[2]
        ukaz = rtvslo.predvajaj_posnetek
    elif argv[1] == '-s' and len(argv) == 3:
        povezava_do_html = argv[2]
        ukaz = rtvslo.shrani_posnetek
    elif len(argv) == 2 and argv[1].lower() in pomoč:
        print(sporočilo_raba + sporočilo_pomoč)
    else:
        print(sporočilo_raba)
    return (povezava_do_html, ukaz)


def main():
    n = nastavitve.naloži_nastavitve()
    ukaz = ukazna_vrstica()
    povezava_do_html = ukaz[0]
    if povezava_do_html:
        informacije = rtvslo.pridobi_posnetek(povezava_do_html, n)
        ukaz[1](informacije, n)


if __name__ == '__main__':
    main()
