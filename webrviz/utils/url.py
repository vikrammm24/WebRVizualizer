from urllib.parse import urlparse

from webrviz.models import Endpoint


def endpoint_from_url(url: str) -> Endpoint:
    parsed = urlparse(url)

    return Endpoint(
        scheme=parsed.scheme,
        hostname=parsed.hostname or "",
        path=parsed.path or "/",
        port=parsed.port,
        query=parsed.query or None,
        full_url=url,
    )
