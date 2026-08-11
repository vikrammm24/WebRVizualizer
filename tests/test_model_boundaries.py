from webrviz.models.application import Application
from webrviz.models.endpoint import Endpoint
from webrviz.models.host import Host


def test_application_owns_hosts() -> None:
    application = Application()

    host = application.get_or_create_host("example.com")

    assert application.hosts["example.com"] is host


def test_host_owns_endpoints() -> None:
    host = Host("example.com")

    endpoint = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="https://example.com/login",
    )

    host.add_endpoint(endpoint)

    assert endpoint in host.endpoints


def test_host_owns_child_hosts() -> None:
    parent = Host("example.com")
    child = Host("api.example.com")

    parent.add_child(child)

    assert parent.children["api.example.com"] is child
    assert child.parent is parent


def test_application_does_not_store_endpoints_directly() -> None:
    application = Application()

    assert not hasattr(application, "endpoints")
