from webrviz.models.application import Application
from webrviz.models.endpoint import Endpoint
from webrviz.models.host import Host


def create_endpoint(
    hostname: str,
    path: str,
) -> Endpoint:
    return Endpoint(
        scheme="https",
        hostname=hostname,
        path=path,
        port=None,
        query=None,
        full_url=f"https://{hostname}{path}",
    )


def test_get_or_create_host_creates_host() -> None:
    application = Application()

    host = application.get_or_create_host("example.com")

    assert isinstance(host, Host)
    assert host.hostname == "example.com"
    assert application.hosts["example.com"] is host


def test_get_or_create_host_returns_existing_host() -> None:
    application = Application()

    first = application.get_or_create_host("example.com")
    second = application.get_or_create_host("example.com")

    assert first is second
    assert len(application.hosts) == 1


def test_get_or_create_host_creates_multiple_hosts() -> None:
    application = Application()

    example = application.get_or_create_host("example.com")
    api = application.get_or_create_host("api.example.com")

    assert application.hosts["example.com"] is example
    assert application.hosts["api.example.com"] is api
    assert len(application.hosts) == 2


def test_root_hosts_returns_hosts_without_known_parent() -> None:
    application = Application()

    example = application.get_or_create_host("example.com")
    api = application.get_or_create_host("api.example.com")

    example.add_child(api)

    roots = application.root_hosts()

    assert roots == [example]


def test_root_hosts_returns_multiple_independent_roots() -> None:
    application = Application()

    example = application.get_or_create_host("example.com")
    other = application.get_or_create_host("other.com")

    roots = application.root_hosts()

    assert roots == [example, other]


def test_root_hosts_is_sorted() -> None:
    application = Application()

    zulu = application.get_or_create_host("zulu.com")
    alpha = application.get_or_create_host("alpha.com")

    roots = application.root_hosts()

    assert roots == [alpha, zulu]


def test_all_hosts_returns_sorted_hosts() -> None:
    application = Application()

    zulu = application.get_or_create_host("zulu.com")
    alpha = application.get_or_create_host("alpha.com")
    api = application.get_or_create_host("api.alpha.com")

    hosts = application.all_hosts()

    assert hosts == [alpha, api, zulu]


def test_all_endpoints_returns_endpoints_from_all_hosts() -> None:
    application = Application()

    example = application.get_or_create_host("example.com")
    api = application.get_or_create_host("api.example.com")

    endpoint_one = create_endpoint(
        "example.com",
        "/",
    )

    endpoint_two = create_endpoint(
        "api.example.com",
        "/users",
    )

    example.add_endpoint(endpoint_one)
    api.add_endpoint(endpoint_two)

    endpoints = list(application.all_endpoints())

    assert endpoints == [
        endpoint_two,
        endpoint_one,
    ]
