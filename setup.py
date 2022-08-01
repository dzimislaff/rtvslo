#!/usr/bin/env python
# -*- coding: 'UTF-8' -*-

# https://github.com/navdeep-G/setup.py
# https://github.com/navdeep-G/setup.py/blob/master/setup.py
# https://click.palletsprojects.com/en/7.x/setuptools/
# https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/

from setuptools import setup, find_packages
import __version__

različica_programa = __version__.__version__
ime_programa = "rtvslo"
opis_programa = ("Preprost program, ki dostopa do posnetkov na spletnem "
                 "portalu rtvslo.si.")
spletna_povezava = "https://github.com/dzimislaff/rtvslo"
email = "nejc.mobilc@gmail.com"
avtor = "Nejc"
različica_pythona = "!=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*, >=3.8.0"
zahtevani_moduli = [
    "requests"
]
dodatni_moduli = {
    "testiranje": ["pytest"],
}


setup(
    name=ime_programa,
    version=različica_programa,
    description=opis_programa,
    author=avtor,
    author_email=email,
    python_requires=različica_pythona,
    packages=find_packages(include=['rtvslo', 'rtvslo.*']),
    install_requires=zahtevani_moduli,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points="""
        [console_scripts]
        rtv=rtvslo.ukaznavrstica:ukaznavrstica
    """,
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Natural Language :: Slovenian,"
    ],
)
