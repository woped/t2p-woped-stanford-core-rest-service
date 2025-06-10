# woped-stanford-core-rest-service
Python Code for using current Stanford CoreNLP

| Table of content |
| :--------------- |
| 1.General Information |
| 2.Functionality |

After cloning this repository, it's essential to [set up git hooks](https://github.com/woped/woped-git-hooks/blob/main/README.md#activating-git-hooks-after-cloning-a-repository) to ensure project standards.

<h1>1. General Information</h1>

| <h2>Github</h2> |
|:---------|
| https://github.com/woped/woped-stanford-core-rest-service |

| <h2>Dockerhub</h2> |
|:---------|
| https://hub.docker.com/r/woped/stanford-corenlp-microservice |

This Projekt is part of CD-CI-Pipeline

<h1>2. Functionality</h1>

<h2>API</h2>

It is build as a ReST-API for this is the common ground for application communication these days. The following path can be used to get information from the stanford-corenlp-rest-service. 

| Host:Port | Path | Method | Headers | Params |
|:----------|:-----|:------:|:--------|:-------|
| https://woped.dhbw-karlsruhe.de:8083 | GET | / | - | - |
| https://woped.dhbw-karlsruhe.de:8083 | POST | / | - | - |
