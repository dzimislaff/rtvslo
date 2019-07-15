#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import json
import nastavitve
import re
import pyperclip
import requests
from sys import argv
import subprocess

# za zaganjanje programa izven domače mape
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

IME_PROGRAMA = 'rtvslo.py'


def pridobi_api(povezava_do_html, n={}):
    '''
    vhod: povezava spletne strani, na kateri je posnetek 
    izhod: povezava do API, id posnetka [tuple]
    '''
    # 4d.rtvslo.si/arhiv
    štiride = re.compile(r'https?://4d\.rtvslo\.si/arhiv/\S+/\d{7,11}')
    # 4d.rtvslo.si/zivo
    v_živo = re.compile(r'https?://4d\.rtvslo\.si/zivo/\S+')
    cifra = re.compile(r'\d{7,11}')

    if štiride.search(povezava_do_html):
        # zadnjih 9 števk je id, morda bo treba v prihodnosti to spremeniti
        številka = cifra.search(povezava_do_html).group()
        povezava_do_api = f"https://api.rtvslo.si/ava/getRecording/{številka}?client_id={n['client_id']}"
    elif v_živo.search(povezava_do_html):
        pari = {'tvs1': 'tv.slo1',
                'tvs2': 'tv.slo2',
                'tvs3': 'tv.slo3',
                'tvkp': 'tv.kp1',
                'tvmb': 'tv.mb1',
                'tvmmc': 'tv.mmctv'}
                # nedelujoče povezave
                # 'ra1': 'ra.a1',
                # 'val202': 'ra.val201',
                # 'ars': 'ra.ars',
                # 'rasi': 'ra.rsi'
        for i in pari.keys():
            if i in povezava_do_html:
                povezava_do_api = f"https://api.rtvslo.si/ava/getLiveStream/{pari[i]}?client_id={n['client_id']}"
                break
    return povezava_do_api


def pridobi_json(povezava_do_api, n):
    '''
    vhod: povezava do API
    izhod: JSON s podatki o posnetku 
    ukaz pridobi informacije v obliki JSON o posnetku z api.rtvslo.si
    '''
    r = requests.get(povezava_do_api)
    # za posnetke, ki zahtevajo prijavo – začasno umaknjeno
    # if 'prijava' in json.loads(r.text)['response']['mediaFiles'][0]['filename']:
    #     povezava_do_api += f"&session_id={n['session_id']}"
    #     r = requests.get(povezava_do_api)
    return json.loads(r.text)['response']


def odstrani_znake(beseda, nedovoljeni_znaki):
    '''
    vhod: niz, tj. naslov posnetka, in seznam znakov
    izhod: niz, tj. naslov posnetka, z odstranjenimi znaki
    '''
    nedovoljeni_znaki.append(',')
    for i in nedovoljeni_znaki:
        beseda = beseda.replace(i, '')
    if any(i in beseda for i in nedovoljeni_znaki):
        odstrani_naglase()
    return beseda


def info_json(džejsn, n):
    '''
    vhod: JSON s podatki o posnetku
    izhod: informacije o posnetku: povezava do posnetka, ime, opis [tuple]
    '''
    try:
        # arhiv
        streamer = džejsn['mediaFiles'][0]['streamers']['http'].rstrip('/')
        filename = džejsn['mediaFiles'][0]['filename'].lstrip('/')
    except (KeyError, TypeError):
        # živo
        streamer = džejsn['mediaFiles'][0]['streamer'].rstrip('/')
        filename = džejsn['mediaFiles'][0]['file'].lstrip('/').rstrip('?sub=0')
    mediatype = džejsn['mediaFiles'][0]['mediaType'].lower()
    povezava_do_posnetka = f'{streamer}/{filename}'

    ime = džejsn['title'].replace(' ', '-').lower()
    ime = odstrani_znake(ime, n['znaki'].split(','))
    opis = None
    try:
        opis = džejsn['description']
        print(opis)
    except KeyError as e:
        print('Ne najdem opisa posnetka.', e)
    return (povezava_do_posnetka, ime, mediatype, opis, džejsn)


def shrani_posnetek(informacije, n):
    '''
    vhod: informacije o posnetku: povezava do posnetka, ime, opis [tuple]
    izhod: posnetek
    '''
    if informacije[2] == 'video':   # če gre za TV oz. radio v živo
        return 0
    r = requests.get(informacije[0])
    with open(f'{informacije[1]}.json', 'w') as datoteka:
        json.dump(informacije[4], datoteka, indent=4, ensure_ascii=False)
    with open(f'{informacije[1]}.{informacije[2]}', 'w+b') as f:
        f.write(r.content)


def pridobi_posnetek(povezava_do_html, n):
    '''
    vhod: povezava spletne strani, na kateri je posnetek
    izhod: informacije o posnetku: povezava do posnetka, ime, opis [tuple]
    gre za metaukaz, ki veriži pridobi_api, pridobi_json in info_json
    '''
    povezava_do_api = pridobi_api(povezava_do_html, n)
    informacije = info_json(pridobi_json(povezava_do_api, n), n)
    return informacije


def predvajaj_posnetek(informacije, n):
    '''
    vhod: informacije o posnetku in nastavitve
    ukaz v zunanjem predvajalniku predvaja posnetek
    '''
    subprocess.call([n['predvajalnik'], informacije[0], n['možnosti']])


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
    ukaz = shrani_posnetek
    if (len(argv) == 1):
        povezava_do_html = pyperclip.paste().lower()
    elif (len(argv) == 2) and ('-p' in argv[1] or '-s' in argv[1]):
        povezava_do_html = pyperclip.paste().lower()
        if argv[1] == '-p':
            ukaz = predvajaj_posnetek
    elif argv[1] == '-p' and len(argv) == 3:
        povezava_do_html = argv[2]
        ukaz = predvajaj_posnetek
    elif argv[1] == '-s' and len(argv) == 3:
        povezava_do_html = argv[2]
        ukaz = shrani_posnetek
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
        try:
            informacije = pridobi_posnetek(povezava_do_html, n)
            ukaz[1](informacije, n)
        except (AttributeError, TypeError):
            print('Neveljavna povezava.')


if __name__ == '__main__':
    main()
