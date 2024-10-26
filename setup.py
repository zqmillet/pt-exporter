#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup
from setuptools import find_packages

from pt_exporter import VERSION

with open('pt_exporter/requirements.txt', 'r', encoding='utf8') as file:
    install_requires = list(map(lambda x: x.strip(), file.readlines()))

setup(
    name='pt-exporter',
    version=VERSION,
    author='kinopico',
    author_email='zqmillet@qq.com',
    url='https://github.com/zqmillet/pt-exporter',
    description='a prometheus exporter for private tracker',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pt-exporter=pt_exporter.__main__:main',
        ]
    }
)
