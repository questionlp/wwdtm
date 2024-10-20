# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
import sys
from email.mime import base
from pathlib import Path

current_path = Path.cwd()
sys.path.insert(0, str(current_path.parent))

project = "wwdtm"
copyright = "2018-2024 Linh Pham. All Rights Reserved"
author = "Linh Pham"

extensions = [
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinxext.opengraph",
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

html_theme = "furo"

html_title = "Wait Wait Stats Library"

html_static_path = [
    "_static",
]

html_css_files = [
    "css/custom.css",
]

html_show_sourcelink = False
smartquotes = False

base_fonts = '"IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";'
monospace_fonts = '"IBM Plex Mono", Menlo, Consolas, Monaco, "Liberation Mono", "Lucida Console", monospace;'

html_theme_options = {
    "light_css_variables": {
        "font-stack": base_fonts,
        "font-stack--monospace": monospace_fonts,
        "color-foreground-primary": "#000000",
        "color-foreground-secondary": "#161616",
        "color-foreground-muted": "#21272a",
        "color-brand-content": "#0043ce",
        "color-background-primary": "#ffffff",
        "color-sidebar-background": "#f2f4f8",
        "color-sidebar-link-text--top-level": "#0043ce",
        "color-api-name": "#520408",
        "color-api-pre-name": "#da1e28",
        "color-highlight-on-target": "#f2f4f8",
        "color-sidebar-search-foreground": "#000000",
        "sidebar-item-font-size": "1rem",
        "toc-font-size": "0.95rem",
        "toc-title-font-size": "1rem",
        "color-toc-item-text": "var(--color-foreground-primary);",
        "color-toc-title-text": "var(--color-foreground-primary);",
        "code-font-size": "1rem",
    },
    "dark_css_variables": {
        "font-stack": base_fonts,
        "font-stack--monospace": monospace_fonts,
        "color-foreground-primary": "#ffffff",
        "color-foreground-secondary": "#f4f4f4",
        "color-foreground-muted": "#dde1e6",
        "color-brand-content": "#78a9ff",
        "color-background-primary": "#161616",
        "color-sidebar-background": "#21272a",
        "color-sidebar-link-text--top-level": "#78a9ff",
        "color-api-name": "#fa4d56",
        "color-api-pre-name": "#ffb3b8",
        "color-highlight-on-target": "#21272a",
        "color-sidebar-search-foreground": "#ffffff",
        "sidebar-item-font-size": "1rem",
        "toc-font-size": "0.95rem",
        "toc-title-font-size": "1rem",
        "color-toc-item-text": "var(--color-foreground-primary);",
        "color-toc-title-text": "var(--color-foreground-primary);",
        "code-font-size": "1rem",
    },
}

pygments_style = "sas"
pygments_dark_style = "rrt"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

autodoc_typehints = "description"
python_display_short_literal_types = True
