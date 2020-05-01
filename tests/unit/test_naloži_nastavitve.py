#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import rtvslo.nastavitve


def test_json_povezava():
    n = rtvslo.nastavitve.naloži_nastavitve()
    assert type(n) == dict
    assert type(n["client_id"]) == str
    assert len(n["client_id"]) == 32
    assert type(n["client_id"]) == str
    assert len(n["client_id"]) == 32
    assert type(n["predvajalnik"]) == str
