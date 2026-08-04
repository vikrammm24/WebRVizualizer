from dataclasses import dataclass, field

from .endpoint import Endpoint


@dataclass(slots=True)
class Host:
    """
    Represents a domain or subdomain.
    """

    hostname: str
    endpoints: list[Endpoint] = field(default_factory=list)

    def add_endpoint(self, endpoint: Endpoint) -> None:
        self.endpoints.append(endpoint)
