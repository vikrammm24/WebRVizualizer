from dataclasses import dataclass, field


@dataclass(slots=True)
class HostMetadata:
    """
    Metadata that belongs to a Host rather than an individual Endpoint.

    This model intentionally contains only host-level information.
    Endpoint-specific information must remain on Endpoint.
    """

    ip_addresses: set[str] = field(default_factory=set)
    ports: set[int] = field(default_factory=set)
    server: str | None = None
