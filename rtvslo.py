#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import json
import nastavitve
import re
import pyperclip
import requests
import sys
# import argparse
# import subprocess

# za zaganjanje programa izven domače mape
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


def pridobi_api(povezava_do_html, n={}):
    '''
    vhod: povezava spletne strani, na kateri je posnetek 
    izhod: povezava do API, id posnetka [tuple]
    '''
    # 4d.rtvslo.si
    štiride = re.compile(r'https://4d\.rtvslo\.si/arhiv/\S+/\d{9,}')
    # radioprvi.rtvslo.si, val202.rtvslo.si, ars.rtvslo.si
    ostali = re.compile(r'^https://(ars|prvi|radioprvi|val202)\.rtvslo\.si/')

    if štiride.search(povezava_do_html):
        # zadnjih 9 števk je id, morda bo treba v prihodnosti to spremeniti
        številka = štiride.search(povezava_do_html).group()[-9:]
        povezava_do_api = f"https://api.rtvslo.si/ava/getRecording/{številka}?client_id={n['client_id']}"
        return (povezava_do_api, številka)
    elif ostali.search(povezava_do_html):
        r = requests.get(povezava_do_html)
        iskanje_povezave = re.compile(
            r'https://4d\.rtvslo\.si/arhiv/\S+\d+')
        # zadnjih 9 števk je id, morda bo treba v prihodnosti to spremeniti
        številka = iskanje_povezave.search(r.text).group()[-9:]
        povezava_do_api = f"https://api.rtvslo.si/ava/getRecording/{številka}?client_id={n['client_id']}"

        return (povezava_do_api, številka)


def pridobi_json(povezava_do_api, n={}):
    '''
    vhod: povezava do API
    izhod: JSON s podatki o posnetku 
    ukaz pridobi informacije v obliki JSON o posnetku z api.rtvslo.si
    '''
    r = requests.get(povezava_do_api)
    # za posnetke, ki zahtevajo prijavo
    if 'prijava' in json.loads(r.text)['response']['mediaFiles'][0]['filename']:
        povezava_do_api += f"&session_id={n['session_id']}"
        r = requests.get(povezava_do_api)
    return json.loads(r.text)['response']


def info_json(džejsn):
    '''
    vhod: JSON s podatki o posnetku
    izhod: informacije o posnetku: povezava do posnetka, ime, opis [tuple]
    '''
    try:
        # 4d.rtvslo.si
        streamer = džejsn['mediaFiles'][1]['streamers']['http'].rstrip('/')
        filename = džejsn['mediaFiles'][1]['filename'].lstrip('/')
    except IndexError:
        # radioprvi.rtvslo.si, val202.rtvslo.si, ars.rtvslo.si
        streamer = džejsn['mediaFiles'][0]['streamers']['http'].rstrip('/')
        filename = džejsn['mediaFiles'][0]['filename'].lstrip('/')
    finally:
        povezava_do_posnetka = f'{streamer}/{filename}'

    ime_posnetka = džejsn['title'].replace(' ', '-').lower()
    try:
        opis_posnetka = džejsn['showDescription']
    except KeyError as e:
        print('Ne najdem opisa posnetka.', e)
        opis_posnetka = None
    return (povezava_do_posnetka, ime_posnetka, opis_posnetka)


def shrani_posnetek(informacije):
    '''
    vhod: informacije o posnetku: povezava do posnetka, ime, opis [tuple]
    izhod: posnetek
    '''
    r = requests.get(informacije[0])
    with open(f'{informacije[1][:21]}.mp4', 'w+b') as f:
        f.write(r.content)


def pridobi_posnetek(povezava_do_html, n):
    '''
    vhod: povezava spletne strani, na kateri je posnetek
    izhod: informacije o posnetku: povezava do posnetka, ime, opis [tuple]
    gre za metaukaz, ki veriži pridobi_api, pridobi_json in info_json
    '''
    povezava_do_api = pridobi_api(povezava_do_html, n)[0]
    informacije = info_json(pridobi_json(povezava_do_api, n))
    return informacije

# TODO
# def argumenti():
#     p = argparse.ArgumentParser(
#         description='Program, ki dostopa do posnetkov na portalu rtvslo.si\
#                     Transmission.'
#     )
#     p.add_argument('-p', '--predvajaj', type=str,
#                    help='predvajaj posnetek v predvajalniku')
#     p.add_argument('-s', '--shrani', type=str,
#                    help='predvajaj posnetek v predvajalniku')

# nastavek za predvajanje posnetka
# def predvajaj_posnetek(informacije, n):
#     subprocess.call([n['predvajalnik'], informacije[0], n['možnosti']])


def main():
    # args = argumenti()
    n = nastavitve.naloži_nastavitve()
    try:
        povezava_do_html = sys.argv[1].lower()
    except IndexError:
        povezava_do_html = pyperclip.paste().lower()
    finally:
        informacije = pridobi_posnetek(povezava_do_html, n)
        shrani_posnetek(informacije)


if __name__ == '__main__':
    main()
