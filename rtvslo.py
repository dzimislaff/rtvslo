#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import json
import re
import pyperclip
import requests
import sys


def pridobi_api(povezava_do_html):
    '''
    vhod: povezava spletne strani, na kateri je video
    izhod: povezava do API, id videa [tuple]
    '''
    stran = re.compile(r'\d+$')
    številka = stran.search(povezava_do_html).group()
    povezava_do_api = f'https://api.rtvslo.si/ava/getRecording/{številka}?client_id=82013fb3a531d5414f478747c1aca622'
    return (povezava_do_api, številka)


def pridobi_json(povezava_do_api):
    '''
    vhod: povezava do API
    izhod: JSON s podatki o videu
    funkcija pridobi informacije v obliki JSON o videu z api.rtvslo.si
    '''
    r = requests.get(povezava_do_api)
    return json.loads(r.text)['response']


def info_json(džejsn):
    '''
    vhod: JSON s podatki o videu
    izhod: informacije o videu: povezava do videa, ime, opis [tuple]
    '''
    streamer = džejsn['mediaFiles'][1]['streamers']['http'].rstrip('/')
    filename = džejsn['mediaFiles'][1]['filename']
    povezava_do_videa = streamer + filename

    ime_videa = džejsn['title'].replace(' ', '-').lower()

    opis_videa = džejsn['showDescription']

    return (povezava_do_videa, ime_videa, opis_videa)


def prenesi_video(informacije):
    '''
    vhod: informacije o videu: povezava do videa, ime, opis [tuple]
    izhod: videodatoteka
    '''
    r = requests.get(informacije[0])
    with open(f'{informacije[1][:21]}.mp4', 'w+b') as f:
        f.write(r.content)


def main():
    try:
        povezava_do_html = sys.argv[1].lower()
    except IndexError:
        povezava_do_html = pyperclip.paste().lower()
    finally:
        try:
            povezava_do_api = pridobi_api(povezava_do_html)[0]
            informacije = info_json(pridobi_json(povezava_do_api))
            prenesi_video(informacije)
        except AttributeError:
            print('Neveljavna povezava.')


if __name__ == '__main__':
    main()
