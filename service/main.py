import logging
import logging.config
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pyld.jsonld

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
L = logging.getLogger(__name__)

app = FastAPI(
    title="JSON-LD Proxy",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", ],
    allow_credentials=True,
    allow_methods=["GET","HEAD"],
    allow_headers=["*"],
)

@app.get(
    "/jsonld/{source_url:path}",
    summary="Return JSON-LD from the provided URL"
)
async def extract_jsonld(
        request:Request,
        source_url: str=None
):
    headers = {
        "Content-Type":"application/ld+json"
    }
    if source_url is None or source_url=="":
        return JSONResponse(content=[], headers=headers)
    res = requests.get(source_url)
    options = {}
    content = {
        "source_url": source_url,
        "body": res.text
    }
    jld = pyld.jsonld.load_html(res.text, res.url, None, options)

    headers = {"Content-Type":"application/ld+json"}
    return JSONResponse(content=jld, headers=headers)
