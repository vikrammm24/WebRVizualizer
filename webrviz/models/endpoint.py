from dataclasses import dataclass


@dataclass(slots=True)
class Endpoint:
    """
    Represents a discovered URL endpoint.
    """

    scheme: str
    hostname: str
    path: str
    port: int | None
    query: str | None
    full_url: str
