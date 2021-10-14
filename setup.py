# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is relased under the terms of the Apache License 2.0
"""Package setup file"""

import setuptools

setuptools.setup(name="wwdtm",
                 version="2.0a0",
                 description="Wait Wait... Don't Tell Me! Data Access Library",
                 long_description=("Provides show, host, scorekeeper, panelist and guest details "
                                   "from an instance of the Wait Wait... Don't Tell Me! Stats Page "
                                   "database"),
                 classifiers=[
                     "Development Status :: 1 - Planning",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: Apache Software License 2.0",
                     "Programming Language :: Python :: 3",
                     "Topic :: Software Development :: Libraries",
                 ],
                 url="http://linhpham.org/",
                 author="Linh Pham",
                 author_email="dev@wwdt.me",
                 license="Apache License 2.0",
                 packages=setuptools.find_packages(exclude=["tests"]),
                 package_dir={"wwdtm": "wwdtm"},
                 project_urls={
                     "Source": "https://github.com/questionlp/libwwdtm/",
                 },
                 python_requires=">=3.8",
                 install_requires=[
                     "mysql-connector-python>=8.0.24",
                     "numpy>=1.20.2",
                     "python-dateutil==2.8.1",
                     "python-slugify==4.0.1",
                     "pytz>=2021.1"
                 ],
                 include_package_data=True
                 )
