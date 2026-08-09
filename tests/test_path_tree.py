from webrviz.models.endpoint import Endpoint
from webrviz.services.path_tree import PathTree


def create_endpoint(path: str) -> Endpoint:
    return Endpoint(
        scheme="https",
        hostname="example.com",
        path=path,
        port=None,
        query=None,
        full_url=f"https://example.com{path}",
    )


def test_root_endpoint() -> None:
    tree = PathTree()

    endpoint = create_endpoint("/")

    tree.add(endpoint)

    nodes = tree.nodes()

    assert len(nodes) == 1
    assert nodes[0].segment == "/"
    assert nodes[0].endpoint == endpoint


def test_single_path() -> None:
    tree = PathTree()

    endpoint = create_endpoint("/login")

    tree.add(endpoint)

    nodes = tree.nodes()

    assert len(nodes) == 1

    login = nodes[0]

    assert login.segment == "login"
    assert login.endpoint == endpoint
    assert login.children == {}


def test_nested_path() -> None:
    tree = PathTree()

    endpoint = create_endpoint("/api/v1/users")

    tree.add(endpoint)

    nodes = tree.nodes()

    api = nodes[0]
    v1 = api.children["v1"]
    users = v1.children["users"]

    assert api.segment == "api"
    assert v1.segment == "v1"
    assert users.segment == "users"

    assert users.endpoint == endpoint


def test_multiple_branches() -> None:
    tree = PathTree()

    users = create_endpoint("/api/v1/users")
    admin = create_endpoint("/api/v1/admin")

    tree.add(users)
    tree.add(admin)

    nodes = tree.nodes()

    api = nodes[0]
    v1 = api.children["v1"]

    assert list(v1.children.keys()) == [
        "admin",
        "users",
    ]

    assert v1.children["admin"].endpoint == admin
    assert v1.children["users"].endpoint == users


def test_shared_path_prefix() -> None:
    tree = PathTree()

    api = create_endpoint("/api")
    v1 = create_endpoint("/api/v1")
    users = create_endpoint("/api/v1/users")

    tree.add(api)
    tree.add(v1)
    tree.add(users)

    nodes = tree.nodes()

    api_node = nodes[0]
    v1_node = api_node.children["v1"]
    users_node = v1_node.children["users"]

    assert api_node.endpoint == api
    assert v1_node.endpoint == v1
    assert users_node.endpoint == users


def test_trailing_slash_is_ignored() -> None:
    tree = PathTree()

    endpoint = create_endpoint("/api/v1/users/")

    tree.add(endpoint)

    nodes = tree.nodes()

    api = nodes[0]
    v1 = api.children["v1"]
    users = v1.children["users"]

    assert users.endpoint == endpoint
    assert users.children == {}


def test_query_is_not_part_of_path() -> None:
    endpoint = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/api/users",
        port=None,
        query="id=10",
        full_url="https://example.com/api/users?id=10",
    )

    tree = PathTree()

    tree.add(endpoint)

    nodes = tree.nodes()

    api = nodes[0]
    users = api.children["users"]

    assert users.segment == "users"
    assert users.endpoint == endpoint


def test_paths_are_sorted() -> None:
    tree = PathTree()

    tree.add(create_endpoint("/z"))
    tree.add(create_endpoint("/a"))
    tree.add(create_endpoint("/m"))

    nodes = tree.nodes()

    assert [node.segment for node in nodes] == [
        "a",
        "m",
        "z",
    ]


def test_nested_paths_are_sorted() -> None:
    tree = PathTree()

    tree.add(create_endpoint("/api/z"))
    tree.add(create_endpoint("/api/a"))
    tree.add(create_endpoint("/api/m"))

    nodes = tree.nodes()

    api = nodes[0]

    assert list(api.children.keys()) == [
        "a",
        "m",
        "z",
    ]
