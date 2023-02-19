#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import json
import re
import requests
import subprocess


class NeveljavnaPovezava(Exception):  # TODO premakni v exceptions.py
    """ neveljavna HTML-povezava """
    pass


class BrezNastavitev(Exception):  # TODO premakni v exceptions.py
    """ manjkajo nastavitve """
    pass


class Posnetek:

    štiride = re.compile(
        r"https?:\/\/(4d|365|www)\.rtvslo\.si\/\S+\/(\d{4,11})")
    radio = re.compile(r"https?:\/\/(ars|prvi|val202)\.rtvslo\.si\/.+")
    v_živo = re.compile(r"https?:\/\/365\.rtvslo\.si\/vzivo\/(\w{3,8})")
    seznam_v_živo = {"tvs1": ("tv", "slo1"),
                     "tvs2": ("tv", "slo2"),
                     "tvs3": ("tv", "slo3"),
                     "tvmb": ("tv", "mb1"),
                     "tvkp": ("tv", "kp1"),
                     "tvmmc": ("tv", "mmctv"),
                     "prvi": ("ra", "a1"),
                     "val202": ("ra", "val202"),
                     "ars": ("ra", "ars"),
                     "rsi": ("ra", "rsi"),
                     "ramb": ("ra", "mb1"),
                     "rakp": ("ra", "kp"),
                     "capo": ("ra", "capo"),
                     "mmr": ("ra", "mmr"),
                     "sport202": ("ra", "sport202"),
                     "raz": ("ra", "raz"),
                     }

    def __init__(self,
                 povezava_do_html: str,
                 nastavitve: dict = None,
                 številka: int = None,  # oz. ID, npr. 174890078 oz. tvs1
                 api_info: dict = None,
                 povezava_do_posnetka: str = None,
                 jwt: str = None,
                 html: str = None,
                 naslov: str = None,
                 možnosti: list = [],
                 ):
        self.povezava_do_html = povezava_do_html
        self.nastavitve = nastavitve
        self.številka = številka
        self.api_info = api_info
        self.povezava_do_posnetka = povezava_do_posnetka
        self.jwt = jwt
        self.html = html
        self.naslov = naslov
        self.možnosti = možnosti

    def validacija_povezave(self):
        povezava = self.preveri_html_povezavo(self.povezava_do_html)
        if not self.številka and not povezava:
            raise NeveljavnaPovezava

    @staticmethod
    def preveri_html_povezavo(povezava_do_html: str
                              ) -> bool:
        try:
            assert isinstance(povezava_do_html, str)
        except AssertionError:
            return  # TODO logging

        if any((Posnetek.štiride.search(povezava_do_html),
                Posnetek.radio.search(povezava_do_html),
                Posnetek.v_živo.search(povezava_do_html),
                )):
            return True

    def preveri_nastavitve(self):
        if not self.nastavitve:
            raise BrezNastavitev

    @ staticmethod
    def pridobi_spletno_stran(naslov: str
                              ) -> requests.models.Response:
        try:
            return requests.get(naslov)
        except requests.exceptions.ConnectionError:
            return  # TODO logging

    def pridobi_številko(self):
        if not self.številka:
            self.številka = self.razberi_številko()

    def razberi_številko(self):
        """
        razbere številko oz. ID iz spletne povezave oz. iz HTML-ja
        """
        if ujemanje := self.štiride.search(self.povezava_do_html):
            return ujemanje.group(2)
        elif ujemanje := self.v_živo.search(self.povezava_do_html):
            return ujemanje.group(1)
        else:  # radio, brez številke oz. ID-ja v spletni povezavi
            self.html = self.pridobi_spletno_stran(self.povezava_do_html).text
            try:
                return self.štiride.search(self.html).group(2)
            except AttributeError:
                return  # TODO logging

    def pridobi_api_info(self):
        if not self.api_info:
            self.api_info = self.pridobi_json(self.pridobi_spletno_stran(
                self.povezava_api_info()).text)

    def povezava_api_info(self
                          ) -> str:
        return (f"https://api.rtvslo.si/ava/getRecordingDrm/{self.številka}"
                f"?client_id={self.nastavitve['client_id']}")

    @staticmethod
    def pridobi_json(stran: str,
                     kazalo: str = "response"
                     ) -> dict:
        return json.loads(stran)[kazalo]

    def pridobi_jwt(self):
        self.pridobi_api_info()
        self.jwt = self.json_jwt()

    def json_jwt(self
                 ) -> str:
        try:
            return self.api_info["jwt"]
        except KeyError:
            return  # TODO logging

    def pridobi_povezavo(self):
        if self.jwt:
            ukaz = self.povezava_api_posnetek()
        else:
            ukaz = self.povezava_api_v_živo()
        povezava = self.json_povezava(self.pridobi_json(
            self.pridobi_spletno_stran(ukaz).text))

        if not self.validacija_povezave_do_posnetka(povezava):
            self.povezava_do_posnetka = povezava
        else:
            self.povezava_do_posnetka = self.poišči_povezavo_v_htmlju()
            if "mp3" not in self.povezava_do_posnetka:
                self.številka = self.povezava_do_posnetka
                self.pridobi_povezavo()

    @staticmethod
    def json_povezava(džejsn: dict
                      ) -> str:
        """
        iz JSON-a, pretvorjenega v slovar, razbere povezavo do posnetka
        če je na voljo več ločljivosti, izbere najvišjo
        TODO izbira ločljivosti
        """
        def v_živo(izbire):
            return izbire[0]["streamer"] + izbire[0]["file"]

        def arhivski_posnetek(izbire):
            if len(izbire) > 1:
                # seznam ločljivosti
                vrednosti = [izbira["height"] for izbira in izbire]
                # najde pozicijo posnetka z najvišjo ločljivostjo
                pozicija = vrednosti.index(max(vrednosti))
                if izbire[pozicija]["streams"]["hls_sec"]:  # https
                    return izbire[pozicija]["streams"]["hls_sec"]
                elif izbire[pozicija]["streams"]["hls"]:  # http
                    return izbire[pozicija]["streams"]["hls"]
            else:
                try:
                    return izbire[0]["streams"]["https"]
                except KeyError:
                    try:
                        return izbire[0]["streams"]["http"]
                    except KeyError:
                        return  # TODO logging

        try:
            izbire = džejsn["mediaFiles"]
        except KeyError:
            return  # TODO logging

        try:
            assert džejsn["category"] == "live"
        except KeyError:
            return arhivski_posnetek(izbire)
        else:
            return v_živo(izbire)

    @staticmethod
    def validacija_povezave_do_posnetka(povezava: str
                                        ) -> bool:
        '''
        vrne True, če je povezava do posnetka neustrezna
        '''
        napačni = ("expired", "dummy")
        if not povezava:
            return True
        elif any(i in povezava for i in napačni):
            return True

    def poišči_povezavo_v_htmlju(self
                                 ) -> str:
        if not self.html:
            self.html = self.pridobi_spletno_stran(self.povezava_do_html).text
        mp3 = re.compile(r"mp3\\\":\\\"(\S+mp3)")
        mmc = re.compile(r"data-recording=\"(\d{4,11})\"")
        if niz := mp3.search(self.html):
            return niz.group(1)
        elif niz := mmc.search(self.html):
            return niz.group(1)

    def povezava_api_posnetek(self
                              ) -> str:
        return (f"https://api.rtvslo.si/ava/getMedia/{self.številka}"
                f"?client_id={self.nastavitve['client_id']}&jwt={self.jwt}")

    def povezava_api_v_živo(self):
        return (f"https://api.rtvslo.si/ava/getLiveStream/"
                f"{self.seznam_v_živo[self.številka][0]}."
                f"{self.seznam_v_živo[self.številka][1]}"
                f"?client_id={self.nastavitve['client_id']}")

    def pridobi_naslov(self
                       ) -> str:
        """
        razbere naslov posnetka iz JSON-a
        """

        def naslov_za_arhiv(api: dict,
                            nastavitve: dict):
            """
            v-telovadnici(.mp4)
            """
            return Posnetek.odstrani_znake(
                api['title'].lower(),
                nastavitve['znaki'].split(','))

        def pravi_naslov(api: dict):
            """
            Pujsa Pepa - V telovadnici(.mp4)
            """
            return f"{api['showName']} - {api['title']}"

        if "pravi-naslov" in self.možnosti:
            naslov = pravi_naslov(self.api_info)
        else:
            naslov = naslov_za_arhiv(self.api_info, self.nastavitve)
        try:
            self.naslov = naslov
        except (KeyError, TypeError):
            return  # TODO logging

    @staticmethod
    def odstrani_znake(beseda: str,
                       nedovoljeni_znaki: list
                       ) -> str:
        """
        odstrani nedovoljene znake iz niza znakov
        """
        try:
            assert isinstance(beseda, str)
        except AssertionError:
            return  # TODO logging

        beseda = beseda.replace(" ", "-")
        nedovoljeni_znaki.append(",")
        for i in nedovoljeni_znaki:
            beseda = beseda.replace(i, "").replace("–", "-")
        while "--" in beseda:
            beseda = beseda.replace("--", "-")
        beseda = beseda.lstrip("-").rstrip("-")
        return beseda

    def zapiši_info(self, cwd: str):
        with open(f"{cwd}/{self.naslov}.json", "w") as datoteka:
            json.dump(self.api_info, datoteka, indent=4, ensure_ascii=False)

    def zapiši_posnetek(self, cwd):
        subprocess.call([self.nastavitve["shranjevalnik"],
                         "-o",
                         f"{self.naslov}.%(ext)s",
                         self.povezava_do_posnetka],
                        cwd=cwd)

    def shrani_posnetek(self, cwd):
        if not self.povezava_do_posnetka:
            print("Posnetek ni na voljo.")
        else:
            self.zapiši_posnetek(cwd)
            self.zapiši_info(cwd)

    def predvajaj_posnetek(self):
        subprocess.call([self.nastavitve["predvajalnik"],
                         self.povezava_do_posnetka,
                         self.nastavitve["možnosti"]])

    def start(self):
        self.validacija_povezave()
        self.preveri_nastavitve()
        self.pridobi_številko()
        if self.številka not in self.seznam_v_živo.keys():
            self.pridobi_jwt()
            self.pridobi_povezavo()
        else:
            self.pridobi_povezavo()

    def predvajaj(self):
        self.start()
        self.predvajaj_posnetek()

    def shrani(self, cwd):
        self.start()
        self.pridobi_naslov()
        self.shrani_posnetek(cwd)
