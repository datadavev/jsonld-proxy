# jsonld-proxy

Render JSON-LD from source URL.

Deployed at https://jsonld.rslv.xyz

Example:

```
curl https://jsonld.rslv.xyz/?url=https://doi.pangaea.de/10.1594/PANGAEA.941495
```

or 

```
curl https://jsonld.rslv.xyz/?url=https%3A%2F%2Fdoi.pangaea.de%2F10.1594%2FPANGAEA.941495
```

Run locally:

```
EXPORT PYTHONPATH=$(pwd)
python jldp/run_server.py
```
