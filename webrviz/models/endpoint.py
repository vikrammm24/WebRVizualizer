from dataclasses import dataclass

from webrviz.models.endpoint_identity import EndpointIdentity


@dataclass(frozen=True, slots=True)
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

    def canonical_identity(self) -> EndpointIdentity:
        """
        Return the canonical identity of this endpoint.

        Canonical identity includes:
            - normalized scheme
            - normalized hostname
            - effective port
            - path

        Query strings are intentionally excluded.
        """

        scheme = self.scheme.lower()
        hostname = self.hostname.lower()

        port = self.port

        if port == 80 and scheme == "http":
            port = None
        elif port == 443 and scheme == "https":
            port = None

        path = self.path or "/"

        return EndpointIdentity(
            scheme=scheme,
            hostname=hostname,
            port=port,
            path=path,
        )
