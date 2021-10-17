# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Package setup file"""

from setuptools import setup

setup(name="wwdtm",
      install_requires=[
          "mysql-connector-python==8.0.26",
          "numpy==1.21.2",
          "python-dateutil==2.8.2",
          "python-slugify==5.0.1",
          "pytz==2021.1",
      ]
)
