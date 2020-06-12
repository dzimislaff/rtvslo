# !/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import rtvslo.rtv
import pytest

pari = [
    ('', None),
    ('a', None),
    ('https://4d.rtvslo.si/arhiv/pogled-na/174574657', '174574657'),
    ('https://4d.rtvslo.si/arhiv/dokumentarni-filmi-in-oddaje-kulturno-umetniski-program/174615520', '174615520'),
    ('https://4d.rtvslo.si/arhiv/dokumentarni-filmi-in-oddaje-kulturno-umetniski-program/174369897', '174369897'),
    ('https://4d.rtvslo.si/arhiv/slovenski-film/60911866', '60911866'),
    ('https://4d.rtvslo.si/arhiv/dokumentarni-portret/6828', '6828'),
    (None, None),
    (4352345, None),
    ([123, 'sdf'], None),
    ({'a': 2353}, None),
    (('llk', 345435), None),
    # ('https://ars.rtvslo.si/2020/05/esej-na-radiu-200/', '174695579'),
    ('https://radioprvi.rtvslo.si/2020/05/eppur-si-muove-in-vendar-se-vrti-213/', '174695499'),
    ('https://val202.rtvslo.si/2020/05/koncert-doma-zmelkoow/', '174694953'),
]


@pytest.mark.parametrize('povezava_do_html, številka', pari)
def test_razberi_id(povezava_do_html, številka):
    assert rtvslo.rtv.razberi_id(povezava_do_html) == številka
