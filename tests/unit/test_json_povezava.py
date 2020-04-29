#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import pytest
import rtvslo.rtv
import tests.jsoni


@pytest.mark.parametrize('povezava, džejsn', tests.jsoni.povezave)
def test_json_povezava(povezava, džejsn):
    # print(rtvslo.rtv.json_povezava(džejsn))
    assert type(rtvslo.rtv.json_povezava(džejsn)) == str
