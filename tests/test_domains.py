from webrviz.utils.domains import (
    get_parent_domain,
    get_root_domain,
    is_subdomain,
)


def test_get_parent_domain_for_subdomain() -> None:
    assert get_parent_domain("api.example.com") == "example.com"


def test_get_parent_domain_for_nested_subdomain() -> None:
    assert get_parent_domain("dev.api.example.com") == "api.example.com"


def test_get_parent_domain_for_root_domain() -> None:
    assert get_parent_domain("example.com") is None


def test_get_parent_domain_for_single_label_hostname() -> None:
    assert get_parent_domain("localhost") is None


def test_get_root_domain_for_subdomain() -> None:
    assert get_root_domain("api.example.com") == "example.com"


def test_get_root_domain_for_nested_subdomain() -> None:
    assert get_root_domain("dev.api.example.com") == "example.com"


def test_get_root_domain_for_root_domain() -> None:
    assert get_root_domain("example.com") == "example.com"


def test_get_root_domain_for_single_label_hostname() -> None:
    assert get_root_domain("localhost") == "localhost"


def test_is_subdomain_for_subdomain() -> None:
    assert is_subdomain("api.example.com") is True


def test_is_subdomain_for_nested_subdomain() -> None:
    assert is_subdomain("dev.api.example.com") is True


def test_is_subdomain_for_root_domain() -> None:
    assert is_subdomain("example.com") is False


def test_is_subdomain_for_single_label_hostname() -> None:
    assert is_subdomain("localhost") is False
