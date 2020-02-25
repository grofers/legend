#!/usr/bin/env python

from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt') as fp:
        reqs = fp.read()

    return reqs.split()

setup(
    name='legend',
    version='0.1',
    description=('The legendary Grafana dashboard generator.'),
    author='Grofers Engineering',
    author_email='tech@grofers.com',
    url='https://github.com/grofers/legend',
    packages=find_packages(),
    install_requires=get_requirements(),
    entry_points='''
        [console_scripts]
        legend=legend.cli:main
    '''
)
