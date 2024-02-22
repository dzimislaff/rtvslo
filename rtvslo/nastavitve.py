#! python3
# -*- coding: 'UTF-8' -*-

import configparser
import os
from pathlib import Path


def ustvari_nastavitve(config,
                       ime_datoteke: str = 'nastavitve.ini'):
    client_id = input("Vnesite identifikacijsko številko uporabnika.\n")
    predvajalnik = input("Vnesite ime predvajalnika (npr.: mpv).\n")
    možnosti_predvajalnika = input(
        "Vnesite dodatne možnosti za predvajalnik (npr.: --force-window).\n")
    ločljivost = input("Vnesite želeno ločljivost. (npr.: 1080) \n")
    shranjevalnik = input("Vnesite ime shranjevalnika (npr. yt-dlp).\n")

    config["DOSTOP"] = {"client_id": client_id}
    config["PREDVAJANJE"] = {"predvajalnik": predvajalnik,
                             "možnosti predvajalnika": možnosti_predvajalnika,
                             "ločljivost": ločljivost}
    config["SHRANJEVANJE"] = {"shranjevalnik": shranjevalnik}
    ime_datoteke = Path(__file__).parent / ime_datoteke
    with open(ime_datoteke, "w") as f:
        config.write(f)


def naloži_nastavitve(ime_datoteke="nastavitve.ini"):
    ime_datoteke = Path(__file__).parent / ime_datoteke
    config = configparser.ConfigParser()
    config.read(ime_datoteke, encoding="utf-8")

    nastavitve = {}

    for i in config.sections():
        nastavitve.update(dict(config[i]))

    return nastavitve


def main():
    ime_datoteke = Path(__file__).parent / "nastavitve.ini"
    config = configparser.ConfigParser()

    if not os.path.exists(ime_datoteke):
        print("Nisem našel nastavitev. Morate jih ustvariti.")
        ustvari_nastavitve(config)

    else:
        print(f"Upoštevam obstoječe nastavitve v datoteki {ime_datoteke}"
              ".\nČe želite ustvariti novo datoteko z nastavitvami, najprej "
              f"izbrišite obstoječo datoteko z ukazom: \n\trm {ime_datoteke} "
              "\nNato ponovno zaženite program.")


if __name__ == '__main__':
    main()
