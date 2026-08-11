from webrviz.models.host import Host
from webrviz.models.host_metadata import HostMetadata


def test_host_has_host_metadata() -> None:
    host = Host("example.com")

    assert isinstance(host.metadata, HostMetadata)


def test_host_metadata_defaults_are_empty() -> None:
    host = Host("example.com")

    assert host.metadata.ip_addresses == set()
    assert host.metadata.ports == set()
    assert host.metadata.server is None


def test_host_metadata_is_independent_between_hosts() -> None:
    first = Host("example.com")
    second = Host("api.example.com")

    first.metadata.ip_addresses.add("192.0.2.1")

    assert first.metadata.ip_addresses == {"192.0.2.1"}
    assert second.metadata.ip_addresses == set()


def test_host_metadata_can_store_host_information() -> None:
    host = Host("example.com")

    host.metadata.ip_addresses.add("192.0.2.1")
    host.metadata.ports.update({80, 443})
    host.metadata.server = "nginx"

    assert host.metadata.ip_addresses == {"192.0.2.1"}
    assert host.metadata.ports == {80, 443}
    assert host.metadata.server == "nginx"
