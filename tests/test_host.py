from webrviz.models.endpoint import Endpoint
from webrviz.models.host import Host


def create_endpoint(
    path: str,
    full_url: str,
) -> Endpoint:
    return Endpoint(
        scheme="https",
        hostname="example.com",
        path=path,
        port=None,
        query=None,
        full_url=full_url,
    )


def test_host_stores_hostname() -> None:
    host = Host("example.com")

    assert host.hostname == "example.com"


def test_add_endpoint() -> None:
    host = Host("example.com")

    endpoint = create_endpoint(
        path="/login",
        full_url="https://example.com/login",
    )

    host.add_endpoint(endpoint)

    assert host.endpoints == [endpoint]


def test_add_multiple_endpoints() -> None:
    host = Host("example.com")

    endpoint_one = create_endpoint(
        path="/",
        full_url="https://example.com",
    )

    endpoint_two = create_endpoint(
        path="/login",
        full_url="https://example.com/login",
    )

    host.add_endpoint(endpoint_one)
    host.add_endpoint(endpoint_two)

    assert host.endpoints == [
        endpoint_one,
        endpoint_two,
    ]


def test_add_child() -> None:
    parent = Host("example.com")
    child = Host("api.example.com")

    parent.add_child(child)

    assert parent.children["api.example.com"] is child


def test_add_multiple_children() -> None:
    parent = Host("example.com")

    api = Host("api.example.com")
    www = Host("www.example.com")

    parent.add_child(api)
    parent.add_child(www)

    assert parent.children["api.example.com"] is api
    assert parent.children["www.example.com"] is www


def test_sort_endpoints() -> None:
    host = Host("example.com")

    endpoint_z = create_endpoint(
        path="/z",
        full_url="https://example.com/z",
    )

    endpoint_a = create_endpoint(
        path="/a",
        full_url="https://example.com/a",
    )

    endpoint_m = create_endpoint(
        path="/m",
        full_url="https://example.com/m",
    )

    host.add_endpoint(endpoint_z)
    host.add_endpoint(endpoint_a)
    host.add_endpoint(endpoint_m)

    host.sort_endpoints()

    assert host.endpoints == [
        endpoint_a,
        endpoint_m,
        endpoint_z,
    ]


def test_sort_children() -> None:
    parent = Host("example.com")

    child_z = Host("z.example.com")
    child_a = Host("a.example.com")
    child_m = Host("m.example.com")

    parent.add_child(child_z)
    parent.add_child(child_a)
    parent.add_child(child_m)

    parent.sort_children()

    assert list(parent.children.keys()) == [
        "a.example.com",
        "m.example.com",
        "z.example.com",
    ]


def test_root_host_is_root() -> None:
    host = Host("example.com")

    assert host.is_root is True


def test_subdomain_is_not_root() -> None:
    host = Host("api.example.com")

    assert host.is_root is False


def test_single_label_hostname_is_root() -> None:
    host = Host("localhost")

    assert host.is_root is True
