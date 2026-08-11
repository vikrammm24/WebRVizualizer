from webrviz.models.endpoint import Endpoint
from webrviz.models.endpoint_identity import EndpointIdentity


def test_canonical_identity_contains_scheme_hostname_port_and_path() -> None:
    endpoint = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=8443,
        query="id=1",
        full_url="https://example.com:8443/login?id=1",
    )

    identity = endpoint.canonical_identity()

    assert identity == EndpointIdentity(
        scheme="https",
        hostname="example.com",
        port=8443,
        path="/login",
    )


def test_query_does_not_affect_canonical_identity() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query="id=1",
        full_url="https://example.com/login?id=1",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query="id=2",
        full_url="https://example.com/login?id=2",
    )

    assert endpoint_one.canonical_identity() == endpoint_two.canonical_identity()


def test_hostname_case_does_not_affect_canonical_identity() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="EXAMPLE.COM",
        path="/login",
        port=None,
        query=None,
        full_url="https://EXAMPLE.COM/login",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="https://example.com/login",
    )

    assert endpoint_one.canonical_identity() == endpoint_two.canonical_identity()


def test_scheme_case_does_not_affect_canonical_identity() -> None:
    endpoint_one = Endpoint(
        scheme="HTTPS",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="HTTPS://example.com/login",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="https://example.com/login",
    )

    assert endpoint_one.canonical_identity() == endpoint_two.canonical_identity()


def test_http_default_port_is_removed() -> None:
    endpoint_one = Endpoint(
        scheme="http",
        hostname="example.com",
        path="/",
        port=80,
        query=None,
        full_url="http://example.com:80/",
    )

    endpoint_two = Endpoint(
        scheme="http",
        hostname="example.com",
        path="/",
        port=None,
        query=None,
        full_url="http://example.com/",
    )

    assert endpoint_one.canonical_identity() == endpoint_two.canonical_identity()


def test_https_default_port_is_removed() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=443,
        query=None,
        full_url="https://example.com:443/",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=None,
        query=None,
        full_url="https://example.com/",
    )

    assert endpoint_one.canonical_identity() == endpoint_two.canonical_identity()


def test_non_default_port_is_part_of_identity() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=None,
        query=None,
        full_url="https://example.com/",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=8443,
        query=None,
        full_url="https://example.com:8443/",
    )

    assert endpoint_one.canonical_identity() != endpoint_two.canonical_identity()


def test_http_and_https_are_different_identities() -> None:
    http_endpoint = Endpoint(
        scheme="http",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="http://example.com/login",
    )

    https_endpoint = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="https://example.com/login",
    )

    assert http_endpoint.canonical_identity() != https_endpoint.canonical_identity()


def test_trailing_slash_is_significant() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="https://example.com/login",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login/",
        port=None,
        query=None,
        full_url="https://example.com/login/",
    )

    assert endpoint_one.canonical_identity() != endpoint_two.canonical_identity()


def test_path_case_is_significant() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/Login",
        port=None,
        query=None,
        full_url="https://example.com/Login",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="https://example.com/login",
    )

    assert endpoint_one.canonical_identity() != endpoint_two.canonical_identity()


def test_empty_path_becomes_root_path() -> None:
    endpoint = Endpoint(
        scheme="https",
        hostname="example.com",
        path="",
        port=None,
        query=None,
        full_url="https://example.com",
    )

    identity = endpoint.canonical_identity()

    assert identity.path == "/"


def test_fragment_is_not_part_of_identity() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="https://example.com/login#admin",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="https://example.com/login#user",
    )

    assert endpoint_one.canonical_identity() == endpoint_two.canonical_identity()


def test_canonical_identity_key_is_deterministic() -> None:
    endpoint = Endpoint(
        scheme="https",
        hostname="EXAMPLE.COM",
        path="/login",
        port=443,
        query="id=123",
        full_url="https://EXAMPLE.COM:443/login?id=123",
    )

    assert endpoint.canonical_identity().key == "https://example.com/login"


def test_canonical_identity_does_not_change_endpoint_equality() -> None:
    endpoint_one = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query="id=1",
        full_url="https://example.com/login?id=1",
    )

    endpoint_two = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query="id=2",
        full_url="https://example.com/login?id=2",
    )

    assert endpoint_one != endpoint_two
    assert endpoint_one.canonical_identity() == endpoint_two.canonical_identity()
