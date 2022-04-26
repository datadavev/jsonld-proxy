# jsonld-proxy

Render JSON-LD from source URL

Example:

```
curl https://jldv.deta.dev/jsonld/https://doi.pangaea.de/10.1594/PANGAEA.941495
```

or 

```
curl https://jldv.deta.dev/jsonld/https%3A%2F%2Fdoi.pangaea.de%2F10.1594%2FPANGAEA.941495
```

Run locally:

```
uvicorn --reload main:app
```
