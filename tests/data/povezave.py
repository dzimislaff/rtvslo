#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import pytest

delujoče = [
    'https://4d.rtvslo.si/arhiv/sedmi-dan/174681705',
    'https://4d.rtvslo.si/arhiv/pogled-na/174574657',
    'https://4d.rtvslo.si/arhiv/dokumentarni-filmi-in-oddaje-kulturno-umetniski-program/174615520',
    'https://4d.rtvslo.si/arhiv/dokumentarni-filmi-in-oddaje-kulturno-umetniski-program/174369897',
    'https://4d.rtvslo.si/arhiv/prvi-na-maturi/174688153',
    'https://4d.rtvslo.si/arhiv/meje-mojega-jezika-niso-meje-mojega-sveta/109826798',
    'https://radioprvi.rtvslo.si/2020/05/eppur-si-muove-in-vendar-se-vrti-213/',
    'https://val202.rtvslo.si/2020/05/koncert-doma-zmelkoow/',
    'https://365.rtvslo.si/arhiv/jezero/174660165',
    'https://365.rtvslo.si/arhiv/sport/174841952',
    'https://ars.rtvslo.si/2021/09/druga-jutranja-kronika-708/',
    'https://ars.rtvslo.si/2021/11/oder-342/',

    #
    # nedelujoče
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
