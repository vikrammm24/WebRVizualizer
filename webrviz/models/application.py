from __future__ import annotations

from dataclasses import dataclass, field

from webrviz.models.host import Host
from webrviz.utils.domains import get_parent_domain


@dataclass(slots=True)
class Application:
    """
    Represents the complete web application.

    Every Host is globally accessible through the hosts dictionary.

    Hierarchy is created by linking Host.children.
    """

    hosts: dict[str, Host] = field(default_factory=dict)

    def get_or_create_host(self, hostname: str) -> Host:
        """
        Return an existing Host or create one.
        """

        if hostname not in self.hosts:
            self.hosts[hostname] = Host(hostname)

        return self.hosts[hostname]

    def root_hosts(self) -> list[Host]:
        """
        Return every root host.

        Root hosts have no parent inside the Application.
        """

        roots = []

        for host in self.hosts.values():
            parent = get_parent_domain(host.hostname)

            if parent not in self.hosts:
                roots.append(host)

        return sorted(
            roots,
            key=lambda host: host.hostname,
        )

    def all_hosts(self) -> list[Host]:
        """
        Return every host alphabetically.
        """

        return sorted(
            self.hosts.values(),
            key=lambda host: host.hostname,
        )

    def all_endpoints(self):
        """
        Yield every endpoint in the application.
        """

        for host in self.all_hosts():
            yield from host.sorted_endpoints()
