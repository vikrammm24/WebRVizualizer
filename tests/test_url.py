from webrviz.models.endpoint import Endpoint
from webrviz.utils.url import endpoint_from_url


def test_parse_basic_https_url() -> None:
    endpoint = endpoint_from_url("https://example.com")

    assert endpoint == Endpoint(
        scheme="https",
        hostname="example.com",
        path="/",
        port=None,
        query=None,
        full_url="https://example.com",
    )


def test_parse_http_url() -> None:
    endpoint = endpoint_from_url("http://example.com")

    assert endpoint.scheme == "http"
    assert endpoint.hostname == "example.com"
    assert endpoint.path == "/"
    assert endpoint.port is None
    assert endpoint.query is None
    assert endpoint.full_url == "http://example.com"


def test_parse_url_with_port() -> None:
    endpoint = endpoint_from_url("https://example.com:8080")

    assert endpoint.scheme == "https"
    assert endpoint.hostname == "example.com"
    assert endpoint.path == "/"
    assert endpoint.port == 8080
    assert endpoint.query is None
    assert endpoint.full_url == "https://example.com:8080"


def test_parse_url_with_path() -> None:
    endpoint = endpoint_from_url("https://example.com/login")

    assert endpoint.scheme == "https"
    assert endpoint.hostname == "example.com"
    assert endpoint.path == "/login"
    assert endpoint.port is None
    assert endpoint.query is None
    assert endpoint.full_url == "https://example.com/login"


def test_parse_url_with_query() -> None:
    endpoint = endpoint_from_url(
        "https://example.com/search?q=test"
    )

    assert endpoint.scheme == "https"
    assert endpoint.hostname == "example.com"
    assert endpoint.path == "/search"
    assert endpoint.port is None
    assert endpoint.query == "q=test"
    assert endpoint.full_url == "https://example.com/search?q=test"


def test_parse_url_with_path_and_query() -> None:
    endpoint = endpoint_from_url(
        "https://example.com/api/users?page=2"
    )

    assert endpoint.scheme == "https"
    assert endpoint.hostname == "example.com"
    assert endpoint.path == "/api/users"
    assert endpoint.port is None
    assert endpoint.query == "page=2"
    assert endpoint.full_url == "https://example.com/api/users?page=2"


def test_root_path_defaults_to_slash() -> None:
    endpoint = endpoint_from_url("https://example.com")

    assert endpoint.path == "/"
