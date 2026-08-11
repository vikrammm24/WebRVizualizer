from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EndpointIdentity:
    """
    Canonical identity of a WebRViz endpoint.

    Query strings and fragments are intentionally excluded from
    endpoint identity.

    Identity is based on:
        - scheme
        - normalized hostname
        - effective port
        - path
    """

    scheme: str
    hostname: str
    port: int | None
    path: str

    @property
    def key(self) -> str:
        """
        Return a deterministic string representation of the identity.
        """
        authority = self.hostname

        if self.port is not None:
            authority = f"{authority}:{self.port}"

        return f"{self.scheme}://{authority}{self.path}"
