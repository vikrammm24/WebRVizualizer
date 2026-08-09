from dataclasses import dataclass, field

from webrviz.models.endpoint import Endpoint
from webrviz.utils.domains import get_parent_domain


@dataclass
class Host:
    hostname: str
    endpoints: list[Endpoint] = field(default_factory=list)
    children: dict[str, "Host"] = field(default_factory=dict)
    parent: "Host | None" = None

    @property
    def is_root(self) -> bool:
        """
        Whether this host is a root domain.
        """
        return get_parent_domain(self.hostname) is None

    def add_endpoint(self, endpoint: Endpoint) -> None:
        self.endpoints.append(endpoint)

    def add_child(self, child: "Host") -> None:
        child.parent = self
        self.children[child.hostname] = child

    def sort_endpoints(self) -> None:
        """
        Sort endpoints attached to this host.
        """
        self.endpoints.sort(
            key=lambda endpoint: endpoint.path
        )

    def sort_children(self) -> None:
        """
        Sort child hosts by hostname.
        """
        self.children = dict(
            sorted(
                self.children.items(),
                key=lambda item: item[0],
            )
        )

    def sort(self) -> None:
        """
        Sort this host and all descendants.
        """
        self.sort_endpoints()
        self.sort_children()

        for child in self.children.values():
            child.sort()
