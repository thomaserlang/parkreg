#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='parkreg',
    version='0.1',
    author='Thomas Erlang Sloth',
    author_email='tes@dent.au.dk',
    url='https://gitlab.au.dk/au276587/parkreg',
    description='ParkReg',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    license=None,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'parkreg = parkreg.app:run',
        ],
    },
    classifiers=[],
)