from dataclasses import dataclass, field

from .host import Host


@dataclass(slots=True)
class Application:
    """
    Represents the discovered application.
    """

    hosts: dict[str, Host] = field(default_factory=dict)

    def get_or_create_host(self, hostname: str) -> Host:
        if hostname not in self.hosts:
            self.hosts[hostname] = Host(hostname)

        return self.hosts[hostname]
