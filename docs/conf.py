# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Lanarky"
copyright = "2023, Ajinkya Indulkar"
author = "Ajinkya Indulkar"
release = "v0.6.4"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
]

# autodoc: Default to members and undoc-members
autodoc_default_options = {"members": True}

# autodoc: Don't inherit docstrings (e.g. for nn.Module.forward)
autodoc_inherit_docstrings = False

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_logo = "_static/logo_150px.png"
html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "light_css_variables": {
        "font-stack": "'Segoe UI', sans-serif",
        "font-stack--monospace": "Courier, monospace",
    },
}
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]
html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/ajndkr/lanarky",
            "html": "",
            "class": "fa-brands fa-solid fa-github fa-2x",
        },
        {
            "name": "Twitter",
            "url": "https://twitter.com/ajndkr",
            "html": "",
            "class": "fa-brands fa-solid fa-twitter fa-2x",
        },
    ],
}
