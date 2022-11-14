import os
import sys

sys.path.insert(0, os.path.abspath("../src"))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "mediatpy"
copyright = "2022, Sergio León"
author = "Sergio León"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx_autodoc_typehints"]
# extensions = ["sphinx.ext.autodoc"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {"display_version": True, "style_external_links": True}

html_context = {
    "display_github": True,
    "github_user": "panicoenlaxbox",
    "github_repo": "mediatpy",
    "github_version": "master",
    "conf_py_path": "/docs/",
}
