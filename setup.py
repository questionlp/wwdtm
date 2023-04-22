# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Package setup file"""

from setuptools import setup

setup(
    name="wwdtm",
    install_requires=[
        "mysql-connector-python==8.0.33",
        "numpy==1.24.2",
        "python-dateutil==2.8.2",
        "python-slugify==8.0.1",
        "pytz==2023.3",
    ],
)
