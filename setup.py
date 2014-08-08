#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

name_ = 'pyroman2'
version_ = '2.0.0'

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 3",
    "Topic :: Text Processing :: Markup",
]

setup(
    name=name_,
    version=version_,
    author='Johan Egneblad',
    author_email='johan.egneblad@DELETEMEgmail.com',
    description='Typesetting tool and library',
    license = "BSD",
    url='https://github.com/eblade/'+name_,
    download_url='https://github.com/eblade/'+name_+'/archive/v'+version_+'.tar.gz',
    packages=[name_],
    classifiers = classifiers
)
