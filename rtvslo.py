#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import json
import re
import requests
import subprocess
from typing import NamedTuple
import nastavitve


class Posnetek(NamedTuple):
    številka: str
    jwt: str
    povezava_do_posnetka: str
    client_id: str


class Info(NamedTuple):
    naslov: str
    mediatype: str
    povezava_do_posnetka: str
    opis: str
    džejsn: dict


def pridobi_spletno_stran(naslov):
    '''
    vhod: URL-povezava (niz)
    izhod: spletna stran (requests.models.Response)
    zahteve: requests
    '''
    try:
        return requests.get(naslov)
    except requests.exceptions.ConnectionError:
        return None


def pridobi_json(povezava):
    '''
    vhod: URL-povezava (niz)
    izhod: JSON (dict)
    zahteve: json
    pridobi informacije v obliki JSON o posnetku z api.rtvslo.si
    '''
    r = pridobi_spletno_stran(povezava)
    if r:
        return json.loads(r.text)
    else:
        return None


def razberi_id(povezava_do_html):
    '''
    vhod: URL-povezava (niz)
    izhod: številka, tj. ID-posnetka (niz)
    zahteve: re
    rezbere številko posnetka z URL-povezave
    '''
    štiride = re.compile(r'https?://4d\.rtvslo\.si/arhiv/\S+/\d{7,11}')
    cifra = re.compile(r'\d{7,11}')
    if štiride.search(povezava_do_html):
        return cifra.search(povezava_do_html).group()
    else:
        return None


def povezava_api_drm(povezava_do_html, številka, client_id):
    '''
    vhod: URL-povezava, številka, client ID (vsi niz)
    izhod: URL-povezava (niz)
    vrne URL-povezavo do getRecordingDrm
    '''
    povezava = (f"https://api.rtvslo.si/ava/getRecordingDrm/{številka}"
                f"?client_id={client_id}")
    return povezava


def povezava_api_posnetek(številka, client_id, jwt):
    povezava = (f"https://api.rtvslo.si/ava/getMedia/{številka}"
                f"?client_id={client_id}&jwt={jwt}")
    return povezava


def povezava_api_info(posnetek):
    '''
    vhod: posnetek (namedtuple)
    izhod: URL-povezava (niz)
    vrne URL-povezavo do API getRecording
    '''
    if posnetek.številka:
        povezava = (f"https://api.rtvslo.si/ava/getRecording/"
                    f"{posnetek.številka}?client_id={posnetek.client_id}")
    else:
        povezava = None
    return povezava


def json_jwt(džejsn):
    '''
    vhod: JSON (dict)
    izhod: jwt (niz)
    '''
    return džejsn['response']['jwt']


def json_povezava(džejsn):
    '''
    vhod: JSON (dict)
    izhod: URL-povezava (niz)
    izlušči URL-povezavo do posnetka iz JSON-a
    '''
    izbire = džejsn['response']['mediaFiles']
    if len(izbire) == 2:
        if izbire[0]['height'] > izbire[1]['height']:
            return izbire[0]['streams']['http']
        else:
            return izbire[1]['streams']['http']


def odstrani_znake(beseda, nedovoljeni_znaki):
    '''
    vhod: naslov posnetka (niz) in seznam znakov
    izhod: naslov posnetka (niz) z odstranjenimi znaki
    '''
    nedovoljeni_znaki.append(',')
    for i in nedovoljeni_znaki:
        beseda = beseda.replace(i, '')
    return beseda


def json_info(džejsn, povezava_do_posnetka, n):
    '''
    vhod: JSON (dict), URL-povezava (niz), nastavitve
    izhod: informacije (namedtuple)
    '''
    try:
        naslov = džejsn['response']['title'].replace(' ', '-').lower()
        naslov = odstrani_znake(naslov, n['znaki'].split(','))
    except (KeyError, TypeError):
        naslov = None

    try:
        mediatype = džejsn['response']['mediaFiles'][0]['mediaType'].lower()
    except (KeyError, TypeError):
        mediatype = None

    try:
        opis = džejsn['description']
    except KeyError as e:
        opis = None
    else:
        print(opis)

    return Info(naslov=naslov,
                mediatype=mediatype,
                povezava_do_posnetka=povezava_do_posnetka,
                opis=opis,
                džejsn=džejsn)


def pridobi_posnetek(url, n):
    '''
    vhod: URL-povezava
    izhod: informacije o posnetku (namedtuple)
    gre za metaukaz
    '''
    številka = razberi_id(url)
    client_id = n['client_id']
    jwt = json_jwt(pridobi_json(povezava_api_drm(url, številka, client_id)))
    povezava_do_posnetka = json_povezava(
        pridobi_json(povezava_api_posnetek(številka, client_id, jwt)))
    return Posnetek(številka=številka,
                    jwt=jwt,
                    povezava_do_posnetka=povezava_do_posnetka,
                    client_id=client_id)


def zapiši_posnetek(info):
    '''
    vhod: informacije (namedtuple)
    izhod: /
    v datoteko zapiše posnetek
    '''
    r = pridobi_spletno_stran(info.povezava_do_posnetka)
    with open(f'{info.naslov}.{info.mediatype}', 'w+b') as f:
        f.write(r.content)


def zapiši_info(info):
    '''
    vhod: informacije (namedtuple)
    izhod: /
    zahteve: json
    v datoteko zapiđe informacije (JSON)
    '''
    with open(f'{info.naslov}.json', 'w') as datoteka:
        json.dump(info.džejsn, datoteka, indent=4, ensure_ascii=False)


def shrani_posnetek(posnetek, n):
    '''
    vhod: informacije o posnetku (namedtuple)
    izhod: /
    gre za metaukaz
    '''
    info = json_info(pridobi_json(povezava_api_info(posnetek)),
                     posnetek.povezava_do_posnetka,
                     n)
    zapiši_info(info)
    zapiši_posnetek(info)


def predvajaj_posnetek(posnetek, n):
    '''
    vhod: informacije o posnetku (namedtuple), nastavitve
    izhod: /
    zahteve: subprocces
    v zunanjem predvajalniku predvaja posnetek
    '''
    subprocess.call([n['predvajalnik'],
                     posnetek.povezava_do_posnetka,
                     n['možnosti']])
