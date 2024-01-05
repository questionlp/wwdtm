# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
import sys
from pathlib import Path

from pallets_sphinx_themes import ProjectLink  # type: ignore[report-missing-imports]

current_path = Path.cwd()
sys.path.insert(0, str(current_path.parent))

project = "wwdtm"
copyright = "2018-2024 Linh Pham. All Rights Reserved"
author = "Linh Pham"

extensions = [
    "pallets_sphinx_themes",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
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
        ProjectLink("Source Code", "https://github.com/questionlp/wwdtm"),
        ProjectLink("PyPI", "https://pypi.org/project/wwdtm/"),
        ProjectLink("Stats API", "https://api.wwdt.me/"),
        ProjectLink("Stats Page", "https://stats.wwdt.me/"),
        ProjectLink("Graphs Site", "https://graphs.wwdt.me/"),
        ProjectLink("Reports Site", "https://reports.wwdt.me/"),
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
        # "localtoc.html",
        "relations.html",
        "project.html",
        "searchbox.html",
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
    "python": ("https://docs.python.org/3", None),
}

autodoc_typehints = "description"
python_display_short_literal_types = True
