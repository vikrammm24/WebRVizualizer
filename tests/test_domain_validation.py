import pytest

from webrviz.utils.domains import (
    get_parent_domain,
    get_root_domain,
    is_subdomain,
)


@pytest.mark.parametrize(
    ("hostname", "expected"),
    [
        ("example.com", None),
        ("api.example.com", "example.com"),
        ("dev.api.example.com", "api.example.com"),
        ("example.co.uk", None),
        ("api.example.co.uk", "example.co.uk"),
        ("dev.api.example.co.uk", "api.example.co.uk"),
    ],
)
def test_get_parent_domain(
    hostname: str,
    expected: str | None,
) -> None:
    assert get_parent_domain(hostname) == expected


@pytest.mark.parametrize(
    ("hostname", "expected"),
    [
        ("example.com", "example.com"),
        ("api.example.com", "example.com"),
        ("dev.api.example.com", "example.com"),
        ("example.co.uk", "example.co.uk"),
        ("api.example.co.uk", "example.co.uk"),
        ("dev.api.example.co.uk", "example.co.uk"),
    ],
)
def test_get_root_domain(
    hostname: str,
    expected: str,
) -> None:
    assert get_root_domain(hostname) == expected


@pytest.mark.parametrize(
    "hostname",
    [
        "api.example.com",
        "dev.api.example.com",
        "api.example.co.uk",
        "dev.api.example.co.uk",
    ],
)
def test_is_subdomain(
    hostname: str,
) -> None:
    assert is_subdomain(hostname) is True


@pytest.mark.parametrize(
    "hostname",
    [
        "example.com",
        "example.co.uk",
        "localhost",
    ],
)
def test_root_domains_are_not_subdomains(
    hostname: str,
) -> None:
    assert is_subdomain(hostname) is False
