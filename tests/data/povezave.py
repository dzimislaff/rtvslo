#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import pytest

delujoče = [
    'https://365.rtvslo.si/arhiv/sedmi-dan/174993355',
    'https://365.rtvslo.si/arhiv/utrip/175000441',
    'https://365.rtvslo.si/arhiv/dokumentarni-portret/174379175',
    'https://365.rtvslo.si/arhiv/prvi-na-maturi/174868122',
    'https://365.rtvslo.si/arhiv/aktualna-tema/174933146',
    'https://365.rtvslo.si/arhiv/jezero/174660165',
    'https://365.rtvslo.si/arhiv/sport/174841952',
    'https://365.rtvslo.si/arhiv/dolina-roz/174845696',
    # radijske povezave
    'https://prvi.rtvslo.si/podkast/eppur-si-muove-in-vendar-se-vrti/2688377/174695499',
    'https://ars.rtvslo.si/podkast/ocene/173250873/174883150',
    'https://val202.rtvslo.si/2020/05/koncert-doma-zmelkoow/',
    # v živo: TV
    'https://365.rtvslo.si/vzivo/tvs1',
    'https://365.rtvslo.si/vzivo/tvs2',
    'https://365.rtvslo.si/vzivo/tvs3',
    'https://365.rtvslo.si/vzivo/tvmb',
    'https://365.rtvslo.si/vzivo/tvkp',
    'https://365.rtvslo.si/vzivo/tvmmc',
    # v živo: radio
    'https://365.rtvslo.si/vzivo/prvi',
    'https://365.rtvslo.si/vzivo/val202',
    'https://365.rtvslo.si/vzivo/ars',
    'https://365.rtvslo.si/vzivo/ramb',
    'https://365.rtvslo.si/vzivo/rakp',
    'https://365.rtvslo.si/vzivo/capo',
    'https://365.rtvslo.si/vzivo/mmr',
    'https://365.rtvslo.si/vzivo/sport202',
    'https://365.rtvslo.si/vzivo/raz',

    #
    # nedelujoče
    # 'https://ars.rtvslo.si/2021/11/oder-342/',
    # 'https://ars.rtvslo.si/2021/09/druga-jutranja-kronika-708/',
    # 'https://radioprvi.rtvslo.si/2020/05/eppur-si-muove-in-vendar-se-vrti-213/',
    # ('https://4d.rtvslo.si/arhiv/slovenski-film/60911866'),
    # ('https://ars.rtvslo.si/2020/05/esej-na-radiu-200/'),
    #
    # opis: assert type(info.opis) == str (test_pridobi_informacije)
    # ('https://4d.rtvslo.si/arhiv/res-je/117736682'),
    #
    # naslov: assert type(info.naslov) == str (test_pridobi_informacije)
    # ('https://4d.rtvslo.si/arhiv/dokumentarni-portret/6828'),
    #
    # posnetek: assert type(posnetek.povezava_do_posnetka) (test_pridobi_posnetek)
    # ('https://4d.rtvslo.si/arhiv/intervju-tv/155534620'),
]

nedelujoče = [
    ""
]

neustrezne = [
    "https://fran.si/iskanje?View=1&Query=validacija",
    "https://www.theguardian.com/football",
    "https://docs.pytest.org/en/latest/example/parametrize.html",
    "https://realpython.com/pytest-python-testing/",
]


napačne = [
    None,
    1,
    794854152,
    0,
    (),
    [],
    {},
]

napačne_fail = [
    pytest.param(None, marks=pytest.mark.xfail),
    pytest.param(1, marks=pytest.mark.xfail),
    pytest.param(794854152, marks=pytest.mark.xfail),
    pytest.param(0, marks=pytest.mark.xfail),
    pytest.param((), marks=pytest.mark.xfail),
    pytest.param([], marks=pytest.mark.xfail),
    pytest.param({}, marks=pytest.mark.xfail),
]
