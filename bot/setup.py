#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Santiago Prego
"""

from distutils.core import setup
from setuptools import find_packages

setup(name='Kaligram',
      version='0.1.0',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      description='Gestion remota a traves de telegram.',
      author='Santiago Prego',
      author_email='santiagoprego@gmail.com',
      url='https://github.com/lazeratio/Kaligram',
      license='GPL3',
      install_requires=['pyTelegramBotAPI'],
     )