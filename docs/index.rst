.. lanarky documentation master file, created by
   sphinx-quickstart on Thu May 18 01:03:27 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Lanarky
===================================

.. toctree::
   :maxdepth: 1
   :name: basic
   :caption: Basic
   :hidden:

   features
   getting_started

.. toctree::
   :maxdepth: 1
   :name: advanced
   :caption: Advanced
   :hidden:

   advanced/custom_callbacks

.. toctree::
   :maxdepth: 2
   :name: api
   :caption: API Reference
   :hidden:

   lanarky/lanarky

.. image:: https://img.shields.io/github/stars/ajndkr/lanarky
   :target: https://github.com/ajndkr/lanarky/stargazers

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://github.com/ajndkr/lanarky/blob/main/LICENSE

.. image:: https://badge.fury.io/py/lanarky.svg
   :target: https://pypi.org/project/lanarky/

.. image:: https://img.shields.io/badge/python-3.9-blue.svg
   :target: https://www.python.org/downloads/release/python-3916/

Lanarky is an open-source framework to deploy LLM applications in production.
It is built on top of `FastAPI <https://github.com/tiangolo/fastapi>`_ and comes with batteries included.

❓ Why?
-----------------

There are great low-code/no-code solutions in the open source to deploy your LLM projects. However,
most of them are opinionated in terms of cloud or deployment code. This project aims to provide users
with a cloud-agnostic and deployment-agnostic solution which can be easily integrated into existing
backend infrastructures.

💾 Installation
-----------------

The library is available on PyPI and can be installed via ``pip``.

.. code-block:: bash

   pip install lanarky

🤝 Contributing
----------------

.. image:: https://github.com/ajndkr/lanarky/actions/workflows/code-check.yaml/badge.svg
   :target: https://github.com/ajndkr/lanarky/actions/workflows/code-check.yaml

.. image:: https://github.com/ajndkr/lanarky/actions/workflows/publish.yaml/badge.svg
   :target: https://github.com/ajndkr/lanarky/actions/workflows/publish.yaml

Contributions are more than welcome! If you have an idea for a new feature or want to help improve lanarky,
please create an issue or submit a pull request on `GitHub <https://github.com/ajndkr/lanarky>`_.

See `CONTRIBUTING.md <./CONTRIBUTING.md>`_ for more information.

⚖️ License
----------

The library is released under the `MIT License <https://github.com/ajndkr/lanarky/blob/main/LICENSE>`_.
