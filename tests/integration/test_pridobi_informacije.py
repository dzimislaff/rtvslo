#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import pytest
import rtvslo.rtv
import rtvslo.nastavitve
import tests.povezave

import os
CWD = os.getcwd()


n = rtvslo.nastavitve.naloži_nastavitve()


@pytest.mark.parametrize('url', tests.povezave.seznam)
def test_pridobi_informacije(url):
    posnetek = rtvslo.rtv.pridobi_posnetek(url, n, None)
    info = rtvslo.rtv.pridobi_informacije(posnetek, n, CWD)
    # print(info.naslov)
    # print(info.mediatype)
    # print(info.povezava_do_posnetka)
    # print(info.opis)
    # print(info.džejsn)
    assert type(info.naslov) == str
    assert type(info.mediatype) == str
    assert type(info.povezava_do_posnetka) == str
    assert type(info.opis) == str
    assert type(info.džejsn) == dict
