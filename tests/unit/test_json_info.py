#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import pytest
import rtvslo.rtv
import rtvslo.nastavitve
import tests.jsoni

n = rtvslo.nastavitve.naloži_nastavitve()


@pytest.mark.parametrize('povezava, džejsn', tests.jsoni.info)
def test_info_json(povezava, džejsn):
    # print(rtvslo.rtv.json_info(džejsn, '', n).naslov)
    # print(rtvslo.rtv.json_info(džejsn, '', n).mediatype)
    # print(rtvslo.rtv.json_info(džejsn, '', n).opis)
    # print(rtvslo.rtv.json_info(džejsn, '', n).džejsn)
    assert type(rtvslo.rtv.json_info(džejsn, '', n).naslov) == str
    assert type(rtvslo.rtv.json_info(džejsn, '', n).mediatype) == str
    assert type(rtvslo.rtv.json_info(džejsn, '', n).opis) == str
    assert type(rtvslo.rtv.json_info(džejsn, '', n).džejsn) == dict
