#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import json
import re
import requests
import subprocess


class NeveljavnaPovezava(Exception):  # TODO premakni v exceptions.py
    """ neveljavna HTML-povezava """
    pass


class Posnetek:

    štiride = re.compile(r"https?://4d\.rtvslo\.si/arhiv/\S+/(\d{4,11})")
    erteve = re.compile(r"https?://(ars|radioprvi|val202)\.rtvslo\.si/.+")

    def __init__(self,
                 povezava_do_html: str,
                 nastavitve: dict,
                 številka: int = None,
                 api_info: dict = None,
                 povezava_do_posnetka = None,
                 jwt = None,
                 html = None,
                 naslov = None
                 ):
        self.povezava_do_html = povezava_do_html
        self.nastavitve = nastavitve
        self.številka = številka
        self.api_info = api_info
        self.povezava_do_posnetka = povezava_do_posnetka
        self.jwt = jwt
        self.html = html
        self.naslov = naslov
        if not self.številka and not self.preveri_html_povezavo(povezava_do_html):
            raise NeveljavnaPovezava

    def preveri_html_povezavo(self,
                              povezava_do_html: str
                              ) -> bool:
        try:
            assert type(povezava_do_html) == str
        except AssertionError:
            return  # TODO logging

        if self.štiride.search(povezava_do_html):
            return True
        elif self.erteve.search(povezava_do_html):
            return True

    @staticmethod
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
        if self.štiride.search(self.povezava_do_html):
            return self.štiride.search(self.povezava_do_html).group(1)
        elif self.erteve.search(self.povezava_do_html):
            self.html = self.pridobi_spletno_stran(self.povezava_do_html).text
            try:
                return self.štiride.search(self.html).group(1)
            except AttributeError:
                return  # TODO logging

    def pridobi_api_info(self):
        if not self.api_info:
            self.api_info = self.pridobi_json(self.pridobi_spletno_stran(
                self.povezava_api_info()))

    def povezava_api_info(self
                          ) -> str:
        return (f"https://api.rtvslo.si/ava/getRecordingDrm/{self.številka}"
                f"?client_id={self.nastavitve['client_id']}")

    @staticmethod
    def pridobi_json(stran
                     ) -> dict:
        return json.loads(stran.text)["response"]

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
            self.pridobi_spletno_stran(self.povezava_api_posnetek())))
        self.povezava_do_posnetka = self.validacija_povezave(povezava)

    @staticmethod
    def json_povezava(džejsn: dict
                      ) -> str:
        try:
            izbire = džejsn["mediaFiles"]
        except KeyError:
            return  # TODO logging
        if len(izbire) == 2:
            if izbire[0]["bitrate"] > izbire[1]["bitrate"]:
                return izbire[0]["streams"]["hls_sec"]
            else:
                return izbire[1]["streams"]["hls"]
        else:
            try:
                return izbire[0]["streams"]["https"]
            except KeyError:
                try:
                    return izbire[0]["streams"]["http"]
                except KeyError:
                    return  # TODO logging

    def validacija_povezave(self,
                            povezava: str
                            ) -> str:
        def test_povezave(url: str
                          ) -> bool:
            if "dummy" in url:
                return True

        if test_povezave(povezava):
            mp3 = re.compile(r"mp3\\\":\\\"(\S+mp3)")
            try:
                return mp3.search(self.html).group(1)
            except AttributeError:
                raise NeveljavnaPovezava("nekaj")
        else:
            return povezava

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
