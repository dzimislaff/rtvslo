#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import pytest
import rtvslo.rtv
import rtvslo.nastavitve
import tests.povezave


n = rtvslo.nastavitve.naloži_nastavitve()


@pytest.mark.parametrize('url', tests.povezave.seznam)
def test_pridobi_posnetek(url):
    posnetek = rtvslo.rtv.pridobi_posnetek(url, n, None)
    assert type(posnetek.povezava_do_posnetka) == str
    assert type(posnetek.številka) == str
    assert type(posnetek.jwt) == str
    assert type(posnetek.client_id) == str
