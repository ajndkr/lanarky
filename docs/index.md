---
hide:
  - navigation
  - toc
  - footer
---

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<div align="center">

<img src="assets/logo-light-mode.png#only-light" alt="lanarky-logo-light-mode" width="500">
<img src="assets/logo-dark-mode.png#only-dark" alt="lanarky-logo-dark-mode" width="500">

<h4>The web framework for building LLM microservices.</h4>

<a href="https://github.com/ajndkr/lanarky/blob/main/LICENSE">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</a>
<a href="https://coveralls.io/github/ajndkr/lanarky?branch=main">
  <img src="https://coveralls.io/repos/github/ajndkr/lanarky/badge.svg?branch=main" alt="Coverage">
</a>
<a href="https://pypistats.org/packages/lanarky">
  <img src="https://img.shields.io/pypi/dm/lanarky.svg" alt="Stats">
</a>

</div>

Lanarky is a **python (3.9+)** web framework for developers who want to build microservices using LLMs.
Here are some of its key features:

- **LLM-first**: Unlike other web frameworks, lanarky is built specifically for LLM developers.
  It's unopinionated in terms of how you build your microservices and guarantees zero vendor lock-in
  with any LLM tooling frameworks or cloud providers
- **Fast & Modern**: Built on top of FastAPI, lanarky offers all the FastAPI features you know and love.
  If you are new to FastAPI, visit [fastapi.tiangolo.com](https://fastapi.tiangolo.com) to learn more
- **Streaming**: Streaming is essential for many real-time LLM applications, like chatbots. Lanarky has
  got you covered with built-in streaming support over **HTTP** and **WebSockets**.
- **Open-source**: Lanarky is open-source and free to use. Forever.

<!-- termynal -->

```
$ pip install lanarky
```
