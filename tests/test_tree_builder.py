from rich.tree import Tree

from webrviz.models.application import Application
from webrviz.models.endpoint import Endpoint
from webrviz.services.tree_builder import TreeBuilder


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


def get_child_labels(tree: Tree) -> list[str]:
    return [str(child.label) for child in tree.children]


def test_tree_builder_returns_rich_tree() -> None:
    application = Application()

    tree = TreeBuilder.build(application)

    assert isinstance(tree, Tree)


def test_tree_builder_creates_application_root() -> None:
    application = Application()

    tree = TreeBuilder.build(application)

    assert str(tree.label) == "[bold cyan]Application[/]"


def test_tree_builder_renders_root_host() -> None:
    application = Application()

    host = application.get_or_create_host("example.com")

    tree = TreeBuilder.build(application)

    labels = get_child_labels(tree)

    assert labels == ["[bold green]example.com[/]"]


def test_tree_builder_renders_endpoint() -> None:
    application = Application()

    host = application.get_or_create_host("example.com")

    endpoint = create_endpoint(
        "example.com",
        "/login",
    )

    host.add_endpoint(endpoint)

    tree = TreeBuilder.build(application)

    host_node = tree.children[0]

    labels = get_child_labels(host_node)

    assert labels == ["[white]/login[/]"]


def test_tree_builder_renders_multiple_endpoints() -> None:
    application = Application()

    host = application.get_or_create_host("example.com")

    endpoint_one = create_endpoint(
        "example.com",
        "/",
    )

    endpoint_two = create_endpoint(
        "example.com",
        "/login",
    )

    host.add_endpoint(endpoint_one)
    host.add_endpoint(endpoint_two)

    tree = TreeBuilder.build(application)

    host_node = tree.children[0]

    labels = get_child_labels(host_node)

    assert labels == [
        "[white]/[/]",
        "[white]/login[/]",
    ]


def test_tree_builder_renders_child_host() -> None:
    application = Application()

    parent = application.get_or_create_host("example.com")
    child = application.get_or_create_host("api.example.com")

    parent.add_child(child)

    tree = TreeBuilder.build(application)

    parent_node = tree.children[0]

    labels = get_child_labels(parent_node)

    assert labels == [
        "[bold green]api.example.com[/]",
    ]


def test_tree_builder_renders_nested_hosts() -> None:
    application = Application()

    root = application.get_or_create_host("example.com")
    api = application.get_or_create_host("api.example.com")
    dev = application.get_or_create_host("dev.api.example.com")

    root.add_child(api)
    api.add_child(dev)

    tree = TreeBuilder.build(application)

    root_node = tree.children[0]
    api_node = root_node.children[0]

    labels = get_child_labels(api_node)

    assert labels == [
        "[bold green]dev.api.example.com[/]",
    ]


def test_tree_builder_renders_endpoints_before_child_hosts() -> None:
    application = Application()

    root = application.get_or_create_host("example.com")
    child = application.get_or_create_host("api.example.com")

    endpoint = create_endpoint(
        "example.com",
        "/login",
    )

    root.add_endpoint(endpoint)
    root.add_child(child)

    tree = TreeBuilder.build(application)

    root_node = tree.children[0]

    labels = get_child_labels(root_node)

    assert labels == [
        "[white]/login[/]",
        "[bold green]api.example.com[/]",
    ]
