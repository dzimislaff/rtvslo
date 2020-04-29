# !/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import pytest
import rtvslo.rtv
import rtvslo.nastavitve

n = rtvslo.nastavitve.naloži_nastavitve()
znaki = n['znaki'].split(',')

pari = [
    ('', ''),
    ('a', 'a'),
    ('prežihov-voranc:-boj-na-požiralniku', 'prežihov-voranc-boj-na-požiralniku'),
    ('-judovstvo---starejši-brat-krščanstva',
     'judovstvo-starejši-brat-krščanstva'),
    ('*,",/,[,],:,;,|,=,?', ''),
    ('https4drtvslosiarhivslovenski-film60911866',
     'https4drtvslosiarhivslovenski-film60911866'),
    ('a---a-dfgsdg--sertzerwtg--setrthghrtgh----',
     'a-a-dfgsdg-sertzerwtg-setrthghrtgh'),
    (None, None),
    (4352345, None),
    ([123, 'sdf'], None),
    ({'a': 2353}, None),
    (('llk', 345435), None),
]


@pytest.mark.parametrize('beseda, beseda_brez_znakov', pari)
def test_odstrani_znake(beseda, beseda_brez_znakov):
    assert rtvslo.rtv.odstrani_znake(beseda, znaki) == beseda_brez_znakov
