"""
JLDP is a wrapper around pyld to provide a service that presents the JSON-LD found in
a resource given a target URL.

Copyright (C) 2019-present Dave Vieglais
"""
import dataclasses
import typing
import urllib.parse
import pyld.jsonld
import requests

__version__ = "0.1.0"
__author__ = "datadavev"

TIMEOUT_SECS = 8.0


@dataclasses.dataclass
class JldpResponse:
    status: int
    message: str
    request_url: str
    jld: typing.Union[typing.List[typing.Dict], typing.Dict]
    final_url: typing.Optional[str] = None
    error: typing.Optional[str] = None


def do_extract_jsonld(
    source_url: str,
    accept: str,
    user_agent: str,
) -> JldpResponse:
    """
    Extract JSON-LD from the provided URL.

    A non-error response will always be a list with one or more JSON-LD dictionaries.

    Args:
        source_url: The source URL. Redirects are followed.
        accept: HTTP Accept header. Defaults to "application/ld+json"
        user_agent: HTTP User-Agent header. Defaults to the user-agent of the requester

    Returns:
        List of JSON-LD or an ErrorResponse if an error was encountered.
    """
    headers = {"User-Agent": user_agent, "Accept": accept}
    response = None
    jld = []
    try:
        response = requests.get(source_url, headers=headers, timeout=TIMEOUT_SECS)
        if response.status_code != 200:
            return JldpResponse(
                status=response.status_code,
                message="HTTP Request returned an error status.",
                request_url=source_url,
                final_url=response.url,
                error=None,
                jld=jld
            )
    except Exception as e:
        if response is None:
            return JldpResponse(
                status=500,
                message="HTTP Request raised an error",
                request_url=source_url,
                error=str(e),
                jld=jld
            )
    try:
        options = {}
        content_type = response.headers.get("Content-Type", "text/html")
        if "ld+json" in content_type:
            jld = response.json()
        else:
            jld = pyld.jsonld.load_html(response.content, response.url, None, options)
    except Exception as e:
        return JldpResponse(
            message="JSON-LD extraction from retrieved content failed.",
            status=500,
            request_url=source_url,
            final_url=response.url,
            error=str(e),
            jld=jld
        )
    return JldpResponse(
        message="OK",
        status=response.status_code,
        request_url=source_url,
        final_url=response.url,
        jld=jld
    )
