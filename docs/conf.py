# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2021 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
import os
import sys

from pallets_sphinx_themes import ProjectLink # type: ignore

sys.path.insert(0, os.path.abspath('../'))

project = "wwdtm"
copyright = "2021 Linh Pham"
author = "Linh Pham"

extensions = [
    "pallets_sphinx_themes",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx_copybutton",
]

templates_path = [
    "_templates",
]

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".git",
    "venv",
]

html_theme = "flask"

html_context = {
    "project_links": [
        ProjectLink("Github", "https://github.com/questionlp"),
        ProjectLink("Repository", "https://github.com/questionlp/wwdtm"),
    ]
}

html_sidebars = {
    "index": [
        "globaltoc.html",
        "project.html",
        "searchbox.html",
    ],
    "**": [
        "globaltoc.html",
        "localtoc.html",
        "relations.html",
        "project.html",
        "searchbox.html"
    ],
}

html_static_path = [
    "_static",
]

html_css_files = [
    "css/custom.css",
]

html_show_sourcelink = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None)
}
