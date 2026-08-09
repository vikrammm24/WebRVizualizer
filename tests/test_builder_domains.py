from webrviz.models.endpoint import Endpoint
from webrviz.services.builder import ApplicationBuilder


def create_endpoint(hostname: str, path: str) -> Endpoint:
    return Endpoint(
        scheme="https",
        hostname=hostname,
        path=path,
        port=None,
        query=None,
        full_url=f"https://{hostname}{path}",
    )


def test_builder_handles_co_uk_domain_hierarchy() -> None:
    endpoints = [
        create_endpoint("example.co.uk", "/"),
        create_endpoint("api.example.co.uk", "/api"),
        create_endpoint("dev.api.example.co.uk", "/debug"),
    ]

    builder = ApplicationBuilder()
    application = builder.build(endpoints)

    root = application.get_or_create_host("example.co.uk")
    api = application.get_or_create_host("api.example.co.uk")
    dev_api = application.get_or_create_host(
        "dev.api.example.co.uk"
    )

    assert root.is_root
    assert api.parent is root
    assert dev_api.parent is api


def test_builder_does_not_treat_co_uk_as_parent() -> None:
    endpoints = [
        create_endpoint("example.co.uk", "/"),
    ]

    builder = ApplicationBuilder()
    application = builder.build(endpoints)

    root = application.get_or_create_host("example.co.uk")

    assert root.is_root
    assert "co.uk" not in application.hosts


def test_builder_handles_multiple_co_uk_subdomains() -> None:
    endpoints = [
        create_endpoint("example.co.uk", "/"),
        create_endpoint("www.example.co.uk", "/"),
        create_endpoint("api.example.co.uk", "/"),
        create_endpoint("dev.api.example.co.uk", "/"),
    ]

    builder = ApplicationBuilder()
    application = builder.build(endpoints)

    root = application.get_or_create_host("example.co.uk")
    www = application.get_or_create_host("www.example.co.uk")
    api = application.get_or_create_host("api.example.co.uk")
    dev_api = application.get_or_create_host(
        "dev.api.example.co.uk"
    )

    assert root.is_root

    assert www.parent is root
    assert api.parent is root
    assert dev_api.parent is api
