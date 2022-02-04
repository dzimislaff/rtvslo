#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

import subprocess
import rtvslo.rtv
import rtvslo.nastavitve
import tests.data.povezave

nastavitve = rtvslo.nastavitve.naloži_nastavitve()

for povezava in tests.data.povezave.delujoče:
    posnetek = rtvslo.rtv.Posnetek(povezava, nastavitve)
    posnetek.pridobi_številko()
    posnetek.pridobi_jwt()
    url = posnetek.povezava_api_posnetek()

    # --------------------------------------
    # url = posnetek.povezava_api_info()
    subprocess.call(
        ["wget", url], cwd="/home/nejc/Dokumenti/bin/rtvslo/tests")
