from webrviz.models.endpoint import Endpoint


def test_endpoint_stores_values() -> None:
    endpoint = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=443,
        query="next=dashboard",
        full_url="https://example.com:443/login?next=dashboard",
    )

    assert endpoint.scheme == "https"
    assert endpoint.hostname == "example.com"
    assert endpoint.path == "/login"
    assert endpoint.port == 443
    assert endpoint.query == "next=dashboard"
    assert endpoint.full_url == "https://example.com:443/login?next=dashboard"


def test_identical_endpoints_are_equal() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=None,
        query=None,
        full_url="https://example.com",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=None,
        query=None,
        full_url="https://example.com",
    )

    assert endpoint_one == endpoint_two


def test_identical_endpoints_have_same_hash() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=None,
        query=None,
        full_url="https://example.com",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=None,
        query=None,
        full_url="https://example.com",
    )

    assert hash(endpoint_one) == hash(endpoint_two)


def test_different_endpoints_are_not_equal() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=None,
        query=None,
        full_url="https://example.com",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="https://example.com/login",
    )

    assert endpoint_one != endpoint_two


def test_duplicate_endpoints_can_be_removed_with_set() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=None,
        query=None,
        full_url="https://example.com",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=None,
        query=None,
        full_url="https://example.com",
    )

    endpoints = {endpoint_one, endpoint_two}

    assert len(endpoints) == 1
