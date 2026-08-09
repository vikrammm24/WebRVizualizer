from webrviz.models.endpoint import Endpoint
from webrviz.services.builder import ApplicationBuilder


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


def test_builder_creates_application() -> None:
    endpoint = create_endpoint(
        "example.com",
        "/",
    )

    application = ApplicationBuilder.build([endpoint])

    assert len(application.hosts) == 1
    assert "example.com" in application.hosts


def test_builder_groups_endpoints_by_hostname() -> None:
    endpoint_one = create_endpoint(
        "example.com",
        "/",
    )

    endpoint_two = create_endpoint(
        "example.com",
        "/login",
    )

    application = ApplicationBuilder.build(
        [endpoint_one, endpoint_two]
    )

    host = application.hosts["example.com"]

    assert host.endpoints == [
        endpoint_one,
        endpoint_two,
    ]


def test_builder_removes_duplicate_endpoints() -> None:
    endpoint_one = create_endpoint(
        "example.com",
        "/",
    )

    endpoint_duplicate = create_endpoint(
        "example.com",
        "/",
    )

    application = ApplicationBuilder.build(
        [endpoint_one, endpoint_duplicate]
    )

    host = application.hosts["example.com"]

    assert len(host.endpoints) == 1
    assert host.endpoints[0] == endpoint_one


def test_builder_creates_multiple_hosts() -> None:
    example_endpoint = create_endpoint(
        "example.com",
        "/",
    )

    api_endpoint = create_endpoint(
        "api.example.com",
        "/",
    )

    application = ApplicationBuilder.build(
        [
            example_endpoint,
            api_endpoint,
        ]
    )

    assert set(application.hosts) == {
        "example.com",
        "api.example.com",
    }


def test_builder_creates_parent_child_relationship() -> None:
    example_endpoint = create_endpoint(
        "example.com",
        "/",
    )

    api_endpoint = create_endpoint(
        "api.example.com",
        "/",
    )

    application = ApplicationBuilder.build(
        [
            example_endpoint,
            api_endpoint,
        ]
    )

    example = application.hosts["example.com"]
    api = application.hosts["api.example.com"]

    assert example.children["api.example.com"] is api


def test_builder_handles_nested_subdomains() -> None:
    root_endpoint = create_endpoint(
        "example.com",
        "/",
    )

    api_endpoint = create_endpoint(
        "api.example.com",
        "/",
    )

    dev_endpoint = create_endpoint(
        "dev.api.example.com",
        "/",
    )

    application = ApplicationBuilder.build(
        [
            root_endpoint,
            api_endpoint,
            dev_endpoint,
        ]
    )

    root = application.hosts["example.com"]
    api = application.hosts["api.example.com"]
    dev = application.hosts["dev.api.example.com"]

    assert root.children["api.example.com"] is api
    assert api.children["dev.api.example.com"] is dev


def test_builder_does_not_create_missing_parent() -> None:
    endpoint = create_endpoint(
        "dev.api.example.com",
        "/",
    )

    application = ApplicationBuilder.build([endpoint])

    dev = application.hosts["dev.api.example.com"]

    assert dev.children == {}
    assert application.root_hosts() == [dev]


def test_builder_sorts_endpoints() -> None:
    endpoint_z = create_endpoint(
        "example.com",
        "/z",
    )

    endpoint_a = create_endpoint(
        "example.com",
        "/a",
    )

    endpoint_m = create_endpoint(
        "example.com",
        "/m",
    )

    application = ApplicationBuilder.build(
        [
            endpoint_z,
            endpoint_a,
            endpoint_m,
        ]
    )

    host = application.hosts["example.com"]

    assert host.endpoints == [
        endpoint_a,
        endpoint_m,
        endpoint_z,
    ]


def test_builder_sorts_child_hosts() -> None:
    root = create_endpoint(
        "example.com",
        "/",
    )

    child_z = create_endpoint(
        "z.example.com",
        "/",
    )

    child_a = create_endpoint(
        "a.example.com",
        "/",
    )

    child_m = create_endpoint(
        "m.example.com",
        "/",
    )

    application = ApplicationBuilder.build(
        [
            root,
            child_z,
            child_a,
            child_m,
        ]
    )

    host = application.hosts["example.com"]

    assert list(host.children.keys()) == [
        "a.example.com",
        "m.example.com",
        "z.example.com",
    ]


def test_builder_sorts_application_hosts() -> None:
    zulu = create_endpoint(
        "zulu.com",
        "/",
    )

    alpha = create_endpoint(
        "alpha.com",
        "/",
    )

    example = create_endpoint(
        "example.com",
        "/",
    )

    application = ApplicationBuilder.build(
        [
            zulu,
            alpha,
            example,
        ]
    )

    assert list(application.hosts.keys()) == [
        "alpha.com",
        "example.com",
        "zulu.com",
    ]
