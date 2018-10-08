# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name='pdbfile',
    version='0.0.1',
    packages=['pdbfile'],
    description='A basic clone of the Microsoft clr PDB file parser (debug symbols)',
    author='Mountainstorm',
    install_requires=['pefile'],
    scripts=['pdb_download_symbols', 'pdb_extract_signatures']
)
