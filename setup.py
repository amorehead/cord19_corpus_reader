#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='CORD_19_Corpus_Reader',
    version='0.0.4',
    description='A corpus reader for the CORD-19 dataset, compatible with NLTK',
    author='Alex Morehead',
    author_email='alex.morehead@gmail.com',
    url='https://github.com/amorehead/cord19_corpus_reader',
    install_requires=['nltk'],
    packages=find_packages(),
)
