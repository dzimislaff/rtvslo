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

    štiride = re.compile(r"https?://(4d|365)\.rtvslo\.si/\S+/(\d{4,11})")
    erteve = re.compile(r"https?://(ars|radioprvi|val202)\.rtvslo\.si/.+")

    def __init__(self,
                 povezava_do_html: str,
                 nastavitve: dict = None,
                 številka: int = None,
                 api_info: dict = None,
                 povezava_do_posnetka: str = None,
                 jwt: str = None,
                 html: str = None,
                 naslov: str = None
                 ):
        self.povezava_do_html = povezava_do_html
        self.nastavitve = nastavitve
        self.številka = številka
        self.api_info = api_info
        self.povezava_do_posnetka = povezava_do_posnetka
        self.jwt = jwt
        self.html = html
        self.naslov = naslov

    def validacija_povezave(self):
        povezava = self.preveri_html_povezavo(self.povezava_do_html)
        if not self.številka and not povezava:
            raise NeveljavnaPovezava

    @staticmethod
    def preveri_html_povezavo(povezava_do_html: str
                              ) -> bool:
        try:
            assert type(povezava_do_html) == str
        except AssertionError:
            return  # TODO logging

        if Posnetek.štiride.search(povezava_do_html):
            return True
        elif Posnetek.erteve.search(povezava_do_html):
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
        if ujemanje := self.štiride.search(self.povezava_do_html):
            return ujemanje.group(2)
        else:  # erteve
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
        povezava = self.json_povezava(self.pridobi_json(
            self.pridobi_spletno_stran(self.povezava_api_posnetek()).text))
        if not self.validacija_povezave_do_posnetka(povezava):
            self.povezava_do_posnetka = povezava
        else:
            self.povezava_do_posnetka = self.poišči_povezavo_v_htmlju()

    @staticmethod
    def json_povezava(džejsn: dict
                      ) -> str:
        try:
            izbire = džejsn["mediaFiles"]
        except KeyError:
            return  # TODO logging
        if len(izbire) > 1:
            # seznam ločljivosti
            vrednosti = [izbira["height"] for izbira in izbire]
            # najde pozicijo posnetka z najvišjo ločljivostjo
            # TODO izbira ločljivosti
            pozicija = vrednosti.index(max(vrednosti))
            if izbire[pozicija]["streams"]["hls_sec"]:
                return izbire[pozicija]["streams"]["hls_sec"]
            elif izbire[pozicija]["streams"]["hls"]:
                return izbire[pozicija]["streams"]["hls"]
        else:
            try:
                return izbire[0]["streams"]["https"]
            except KeyError:
                try:
                    return izbire[0]["streams"]["http"]
                except KeyError:
                    return  # TODO logging

    @staticmethod
    def validacija_povezave_do_posnetka(povezava: str
                                        ) -> bool:
        napačni = ("expired", "dummy")
        if any(i in povezava for i in napačni):
            return True

    def poišči_povezavo_v_htmlju(self
                                 ) -> str:
        mp3 = re.compile(r"mp3\\\":\\\"(\S+mp3)")
        try:
            return mp3.search(self.html).group(1)
        except AttributeError:
            raise NeveljavnaPovezava("nekaj")

    def povezava_api_posnetek(self
                              ) -> str:
        return (f"https://api.rtvslo.si/ava/getMedia/{self.številka}"
                f"?client_id={self.nastavitve['client_id']}&jwt={self.jwt}")

    def pridobi_naslov(self
                       ) -> str:
        """
        razbere naslov posnetka iz JSON-a
        """
        try:
            self.naslov = self.odstrani_znake(
                self.api_info['title'].lower(),
                self.nastavitve['znaki'].split(','))
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
            assert type(beseda) == str
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
        self.pridobi_jwt()
        self.pridobi_povezavo()

    def predvajaj(self):
        self.start()
        self.predvajaj_posnetek()

    def shrani(self, cwd):
        self.start()
        self.pridobi_naslov()
        self.shrani_posnetek(cwd)
