#!/usr/bin/env python3
# -*- coding utf-8 -*-
# @author: Roman Sinayev
# @created: 2017-08-03 19:17:22
# @modified: 2017-08-03 19:44:49
# @filename: setup.py

from setuptools import setup

setup(name='glitchart',
      version='0.1.0',
      packages=['glitchart'],
      install_requires=['Pillow'],
      entry_points={
          'console_scripts': [
              'glitchart = glitchart.glitchart:glitch_main'
          ]
      },
      )

