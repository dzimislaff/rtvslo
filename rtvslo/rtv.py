#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import json
import re
import requests
import subprocess
from typing import NamedTuple


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


def pridobi_spletno_stran(naslov: str
                          ) -> requests.models.Response:
    '''
    zahteve: requests
    '''
    try:
        return requests.get(naslov)
    except requests.exceptions.ConnectionError:
        return None


def pridobi_json(stran: requests.models.Response
                 ) -> dict:
    '''
    zahteve: json
    pridobi informacije v obliki JSON o posnetku z api.rtvslo.si
    '''
    if stran:
        return json.loads(stran.text)
    else:
        return None


def razberi_id(povezava_do_html: str
               ) -> str:
    '''
    zahteve: re
    razbere številko posnetka z URL-povezave
    '''
    try:
        assert type(povezava_do_html) == str
    except AssertionError:
        return None

    štiride = re.compile(r'https?://4d\.rtvslo\.si/arhiv/\S+/\d{4,11}')
    cifra = re.compile(r'\d{4,11}')
    if štiride.search(povezava_do_html):
        return cifra.search(povezava_do_html).group()
    else:
        return None


def povezava_api_drm(številka: str,
                     client_id: str
                     ) -> str:
    '''
    ustvari URL-povezavo do getRecordingDrm
    '''
    povezava = (f"https://api.rtvslo.si/ava/getRecordingDrm/{številka}"
                f"?client_id={client_id}")
    return povezava


def povezava_api_posnetek(številka: str,
                          client_id: str,
                          jwt: str
                          ) -> str:
    '''
    vrne URL-povezavo do getMedia
    '''
    povezava = (f"https://api.rtvslo.si/ava/getMedia/{številka}"
                f"?client_id={client_id}&jwt={jwt}")
    return povezava


def povezava_api_info(posnetek: NamedTuple
                      ) -> str:
    '''
    ustvari URL-povezavo do API getRecording
    '''
    if posnetek.številka:
        povezava = (f"https://api.rtvslo.si/ava/getRecording/"
                    f"{posnetek.številka}?client_id={posnetek.client_id}")
    else:
        povezava = None
    return povezava


def json_jwt(džejsn: dict
             ) -> str:
    '''
    razbere jwt iz JSON-a
    '''
    try:
        return džejsn['response']['jwt']
    except KeyError:
        return None


def json_povezava(džejsn: dict
                  ) -> str:
    '''
    razbere URL-povezavo do posnetka iz JSON-a
    '''
    try:
        izbire = džejsn['response']['mediaFiles']
    except KeyError:
        return None
    if len(izbire) == 2:
        if izbire[0]['height'] > izbire[1]['height']:
            return izbire[0]['streams']['http']
        else:
            return izbire[1]['streams']['http']
    else:
        try:
            return izbire[0]['streams']['https']
        except KeyError:
            try:
                return izbire[0]['streams']['http']
            except KeyError:
                return None


def odstrani_znake(beseda: str,
                   nedovoljeni_znaki: list
                   ) -> str:
    '''
    odstrani nedovoljene znake iz niza
    '''
    try:
        assert type(beseda) == str
    except AssertionError:
        return None

    beseda = beseda.replace(' ', '-')
    nedovoljeni_znaki.append(',')
    for i in nedovoljeni_znaki:
        beseda = beseda.replace(i, '')
    while '--' in beseda:
        beseda = beseda.replace('--', '-')
    beseda = beseda.lstrip('-').rstrip('-')
    return beseda


def json_info(džejsn: dict,
              povezava_do_posnetka: str,
              n: dict
              ) -> NamedTuple:
    '''
    ustvari namedtuple s informacijami o posnetku
    '''
    try:
        naslov = džejsn['response']['title'].lower()
        naslov = odstrani_znake(naslov, n['znaki'].split(','))
    except (KeyError, TypeError):
        naslov = None

    try:
        mediatype = džejsn['response']['mediaFiles'][0]['mediaType'].lower()
    except (KeyError, TypeError):
        mediatype = None

    try:
        opis = džejsn['response']['description']
    except KeyError:
        opis = None
    else:
        print(opis)

    return Info(naslov=naslov,
                mediatype=mediatype,
                povezava_do_posnetka=povezava_do_posnetka,
                opis=opis,
                džejsn=džejsn)


def pridobi_posnetek(url: str,
                     n: dict,
                     številka: str = None
                     ) -> NamedTuple:
    '''
    metaukaz, ki zbere podatke, potrebne za predvajanje, shranjevanje posnetka
    '''
    if not številka:
        številka = razberi_id(url)
    client_id = n['client_id']
    jwt = json_jwt(pridobi_json(pridobi_spletno_stran(
        povezava_api_drm(številka,
                         client_id))))
    povezava_do_posnetka = json_povezava(pridobi_json(pridobi_spletno_stran(
        povezava_api_posnetek(številka,
                              client_id,
                              jwt))))
    return Posnetek(številka=številka,
                    jwt=jwt,
                    povezava_do_posnetka=povezava_do_posnetka,
                    client_id=client_id)


def zapiši_posnetek(stran: requests.models.Response,
                    info: NamedTuple,
                    cwd: str):
    '''
    posnetek shrani v datoteko
    '''
    with open(f'{cwd}/{info.naslov}.{info.mediatype}', 'w+b') as datoteka:
        datoteka.write(stran.content)


def zapiši_info(info: NamedTuple,
                cwd: str):
    '''
    zahteve: json
    informacije o posnetku zapiše v datoteko
    '''
    with open(f'{cwd}/{info.naslov}.json', 'w') as datoteka:
        json.dump(info.džejsn, datoteka, indent=4, ensure_ascii=False)


def shrani_posnetek(posnetek: NamedTuple,
                    n: dict,
                    cwd: str):
    '''
    metaukaz, ki posnetek z informacijami shrani na disk
    '''
    info = pridobi_informacije(posnetek, n, cwd)
    zapiši_info(info, cwd)
    zapiši_posnetek((pridobi_spletno_stran(info.povezava_do_posnetka)),
                    info,
                    cwd)


def pridobi_informacije(posnetek: NamedTuple,
                        n: dict,
                        cwd: str):
    if not posnetek.povezava_do_posnetka:
        return None
    info = json_info(
        pridobi_json(pridobi_spletno_stran(povezava_api_info(posnetek))),
        posnetek.povezava_do_posnetka,
        n)
    return info


def predvajaj_posnetek(posnetek: NamedTuple,
                       n: dict,
                       cwd=None):
    '''
    zahteve: subprocces
    v zunanjem predvajalniku predvaja posnetek
    '''
    if not posnetek.povezava_do_posnetka:
        pass
    else:
        subprocess.call([n['predvajalnik'],
                         posnetek.povezava_do_posnetka,
                         n['možnosti']])
