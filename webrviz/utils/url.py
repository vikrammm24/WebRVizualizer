from urllib.parse import urlparse

from webrviz.models.endpoint import Endpoint


def endpoint_from_url(url: str) -> Endpoint:
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    return Endpoint(
        scheme=parsed.scheme,
        hostname=parsed.hostname,
        path=parsed.path or "/",
        port=parsed.port,
        query=parsed.query or None,
        full_url=url,
    )
