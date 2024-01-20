"""
A simple JSON-LD proxy jldp.

When provided a URL, this jldp will retrieve the content and
return a list of JSON-LD blocks extracted from it.

Copyright (c) 2019 - present Dave Vieglais
"""
import os
import typing
import fastapi
import fastapi.responses
import fastapi.staticfiles
import fastapi.middleware.cors
import starlette.responses
import jldp

DEFAULT_USER_AGENT = "Python/3 FastAPI JSONLD-Proxy"
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

app = fastapi.FastAPI(
    title="JSON-LD Proxy",
    version=jldp.__version__,
    description=__doc__,
    contact={
        "name": "Dave Vieglais",
        "url": "https://github.com/datadavev/jsonld-proxy",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/license/mit/",
    },
    openapi_url="/api/v1/openapi.json",
    docs_url="/api",
)

app.mount(
    "/static",
    fastapi.staticfiles.StaticFiles(directory=os.path.join(BASE_FOLDER, "static")),
    name="static",
)

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    raise fastapi.HTTPException(status_code=404, detail="Not found")


@app.get("/", summary="Return JSON-LD from the provided URL")
async def extract_jsonld(
    request: fastapi.Request,
    response: fastapi.Response,
    url: typing.Optional[str] = None,
    accept: typing.Optional[str] = None,
    user_agent: typing.Optional[str] = None,
):
    if url is None:
        return starlette.responses.FileResponse(
            os.path.join(BASE_FOLDER, "static/index.html")
        )
    if accept is None:
        accept = request.headers.get("accept", "*/*")
    if user_agent is None:
        user_agent = request.headers.get("user-agent", DEFAULT_USER_AGENT)
    res = jldp.do_extract_jsonld(url, accept, user_agent)
    if res.status == 200:
        return fastapi.responses.JSONResponse(
            content=res.jld,
            headers={
                "Content-Type": "application/ld+json",
                "x-jldp-final-url": res.final_url,
            },
        )
    if res.final_url is not None:
        response.headers["x-jldp-final-url"] = res.final_url
    return res
