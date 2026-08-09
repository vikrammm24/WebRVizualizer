import pytest

from webrviz.utils.url import endpoint_from_url


def test_http_url_is_valid() -> None:
    endpoint = endpoint_from_url("http://example.com")

    assert endpoint.hostname == "example.com"
    assert endpoint.scheme == "http"


def test_https_url_is_valid() -> None:
    endpoint = endpoint_from_url("https://example.com")

    assert endpoint.hostname == "example.com"
    assert endpoint.scheme == "https"


def test_url_with_port_is_valid() -> None:
    endpoint = endpoint_from_url(
        "https://example.com:8080"
    )

    assert endpoint.hostname == "example.com"
    assert endpoint.port == 8080


def test_url_with_path_is_valid() -> None:
    endpoint = endpoint_from_url(
        "https://example.com/login"
    )

    assert endpoint.hostname == "example.com"
    assert endpoint.path == "/login"


def test_url_with_query_is_valid() -> None:
    endpoint = endpoint_from_url(
        "https://example.com/search?q=test"
    )

    assert endpoint.hostname == "example.com"
    assert endpoint.query == "q=test"


@pytest.mark.parametrize(
    "url",
    [
        "example.com",
        "not-a-valid-url",
        "ftp://example.com",
        "https:///broken",
        "https://",
        "",
    ],
)
def test_invalid_url_is_rejected(url: str) -> None:
    with pytest.raises(ValueError):
        endpoint_from_url(url)
