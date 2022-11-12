# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Package setup file"""

from setuptools import setup

setup(
    name="wwdtm",
    install_requires=[
        "mysql-connector-python==8.0.31",
        "numpy==1.23.4",
        "python-dateutil==2.8.2",
        "python-slugify==6.1.2",
        "pytz==2022.6",
    ],
)
