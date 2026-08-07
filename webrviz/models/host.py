from __future__ import annotations

from dataclasses import dataclass, field

from webrviz.models.endpoint import Endpoint


@dataclass(slots=True)
class Host:
    """
    Represents a hostname within an application.

    A Host owns:
        • endpoints discovered on that hostname
        • child subdomains
    """

    hostname: str

    endpoints: list[Endpoint] = field(default_factory=list)

    children: dict[str, "Host"] = field(default_factory=dict)

    def add_endpoint(self, endpoint: Endpoint) -> None:
        """
        Add an endpoint to this host.
        """
        self.endpoints.append(endpoint)

    def add_child(self, child: "Host") -> None:
        """
        Attach a child subdomain.
        """
        self.children[child.hostname] = child

    @property
    def is_root(self) -> bool:
        """
        Whether this host is considered a root domain.

        This property is populated by the builder.
        """
        return "." not in self.hostname or len(self.hostname.split(".")) == 2

    def sort_endpoints(self) -> None:
        """
        Sort endpoints alphabetically in place.
        """
        self.endpoints.sort(key=lambda endpoint: endpoint.full_url)

    def sort_children(self) -> None:
        """
        Sort child hosts alphabetically in place.
        """
        self.children = dict(
            sorted(
                self.children.items(),
                key=lambda item: item[0],
            )
        )

    @property
    def sorted_children(self) -> list["Host"]:
        """
        Return child hosts sorted alphabetically.
        """
        return sorted(
            self.children.values(),
            key=lambda host: host.hostname,
        )
