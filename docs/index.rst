.. lanarky documentation master file, created by
   sphinx-quickstart on Thu May 18 01:03:27 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Lanarky
===================================

.. toctree::
   :maxdepth: 1
   :name: basic
   :hidden:

   features
   getting_started

.. toctree::
   :maxdepth: 1
   :name: frameworks
   :caption: Supported Frameworks
   :hidden:

   langchain/index

.. toctree::
   :maxdepth: 2
   :name: api
   :caption: API Reference
   :hidden:

   lanarky/index

.. image:: https://img.shields.io/github/stars/ajndkr/lanarky
   :target: https://github.com/ajndkr/lanarky/stargazers

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://github.com/ajndkr/lanarky/blob/main/LICENSE

.. image:: https://badge.fury.io/py/lanarky.svg
   :target: https://pypi.org/project/lanarky/

.. image:: https://img.shields.io/pypi/pyversions/lanarky.svg
   :target: https://pypi.org/project/lanarky/

.. image:: https://coveralls.io/repos/github/ajndkr/lanarky/badge.svg?branch=main
   :target: https://coveralls.io/github/ajndkr/lanarky?branch=main

.. image:: https://img.shields.io/pypi/dm/lanarky.svg
   :target: https://pypistats.org/packages/lanarky

.. image:: https://img.shields.io/twitter/follow/lanarky_io?style=social
   :target: https://twitter.com/intent/follow?screen_name=lanarky_io

A `FastAPI <https://github.com/tiangolo/fastapi>`_ framework to build production-grade LLM applications.

❓ Why?
-----------------

Many open-source projects for developing and deploying LLM applications have either opinionated designs,
particularly regarding deployment, or limitations in terms of scalability. This is where Lanarky comes in.
Lanarky is an open-source project that provides Python users with an unopinionated web framework for constructing
and deploying LLM applications. By leveraging FastAPI as its foundation, Lanarky ensures that applications built
with it are production-ready and can be seamlessly deployed on any cloud provider.

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

See `CONTRIBUTING.md <https://github.com/ajndkr/lanarky/blob/main/CONTRIBUTING.md>`_ for more information.

⚖️ License
----------

The library is released under the `MIT License <https://github.com/ajndkr/lanarky/blob/main/LICENSE>`_.

✨ Want to build LLM applications with us?
------------------------------------------

Are you interested in building LLM applications with us? We would love to hear from you! Reach out to us on
Twitter `@lanarky_io <https://twitter.com/lanarky_io>`_.

Let's connect and explore the possibilities of working together to create amazing LLM applications with Lanarky!
