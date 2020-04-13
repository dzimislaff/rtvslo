#! python3
# -*- coding: 'UTF-8' -*-

import configparser
import os


client_id = '82013fb3a531d5414f478747c1aca622'
session_id = '5cc765368952d4.22094713.245769764'


def ustvari_nastavitve(config, ime_datoteke='nastavitve.ini'):
    lokacija = os.getcwd()
    client_id = input('Vnesite identifikacijsko številko uporabnika.\n')
    session_id = input('Vnesite identifikacijsko število seje.\n')
    naslov = input('Vnesite lokacijo shrambe.\n')
    predvajalnik = input('Vnestite ime predvajalnika (npr.: mpv).')
    možnosti = input(
        'Vnesite dodatne možnosti za predvajalnik (npr.: --force-window)')

    config['PROGRAM'] = {'lokacija': lokacija}

    config['DOSTOP'] = {'client_id': client_id,
                        'session_id': session_id}

    config['SHRAMBA'] = {'naslov': naslov}

    # nastavek za predvajanje posnetka
    # config['PREDVAJANJE'] = {'predvajalnik': predvajalnik,
    #                          'možnosti': možnosti_predvajalnika}

    with open(ime_datoteke, 'w') as f:
        config.write(f)


def naloži_nastavitve(ime_datoteke='nastavitve.ini'):
    config = configparser.ConfigParser()
    config.read(ime_datoteke)

    nastavitve = {}

    for i in config.sections():
        nastavitve.update(dict(config[i]))

    return nastavitve


def main():
    ime_datoteke = 'nastavitve.ini'
    config = configparser.ConfigParser()

    if not os.path.exists(ime_datoteke):
        print('Nisem našel nastavitev. Morate jih ustvariti.')
        ustvari_nastavitve(config)

    else:
        print(f'''Upoštevam obstoječe nastavitve v datoteki \
{os.getcwd()}/{ime_datoteke}.\nČe želite ustvariti novo datoteko z \
nastavitvami, najprej izbrišite obstoječo datoteko z ukazom: \n\trm \
{os.getcwd()}/{ime_datoteke} \nNato ponovno zaženite program.
            ''')


if __name__ == '__main__':
    main()
