import pytest

from webrviz.utils.domains import (
    get_parent_domain,
    get_root_domain,
    is_subdomain,
)


@pytest.mark.parametrize(
    ("hostname", "expected"),
    [
        ("api.example.com", "example.com"),
        ("dev.api.example.com", "api.example.com"),
        ("www.example.co.uk", "example.co.uk"),
        ("api.example.co.uk", "example.co.uk"),
        ("localhost", None),
        ("example.com", None),
    ],
)
def test_get_parent_domain_edge_cases(
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
        ("www.example.co.uk", "example.co.uk"),
        ("api.example.co.uk", "example.co.uk"),
        ("localhost", "localhost"),
    ],
)
def test_get_root_domain_edge_cases(
    hostname: str,
    expected: str,
) -> None:
    assert get_root_domain(hostname) == expected


@pytest.mark.parametrize(
    "hostname",
    [
        "api.example.com",
        "dev.api.example.com",
        "www.example.co.uk",
        "api.example.co.uk",
    ],
)
def test_is_subdomain_edge_cases(hostname: str) -> None:
    assert is_subdomain(hostname) is True


@pytest.mark.parametrize(
    "hostname",
    [
        "example.com",
        "localhost",
    ],
)
def test_root_domains_are_not_subdomains(hostname: str) -> None:
    assert is_subdomain(hostname) is False
