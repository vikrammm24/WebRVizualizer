from __future__ import annotations

from dataclasses import dataclass, field

from webrviz.models.endpoint import Endpoint


@dataclass
class PathNode:
    """
    Represents a single segment in an endpoint path hierarchy.

    A PathNode may represent an endpoint itself and may also contain
    child path segments.
    """

    segment: str
    endpoint: Endpoint | None = None
    children: dict[str, "PathNode"] = field(default_factory=dict)

    def add_child(self, segment: str) -> "PathNode":
        """
        Get or create a child node for the given path segment.
        """

        if segment not in self.children:
            self.children[segment] = PathNode(segment)

        return self.children[segment]

    def sort_children(self) -> None:
        """
        Sort child nodes alphabetically.
        """

        self.children = dict(
            sorted(
                self.children.items(),
                key=lambda item: item[0],
            )
        )

        for child in self.children.values():
            child.sort_children()


class PathTree:
    """
    Builds a hierarchical representation of endpoint paths.

    Example
    -------
    /api/v1/users
    /api/v1/admin

    becomes:

    api
    └── v1
        ├── admin
        └── users
    """

    def __init__(self) -> None:
        self.root: dict[str, PathNode] = {}

    def add(self, endpoint: Endpoint) -> None:
        """
        Add an endpoint to the path hierarchy.
        """

        path = endpoint.path

        #
        # Root endpoint.
        #
        if path == "/":
            self.root["/"] = PathNode(
                segment="/",
                endpoint=endpoint,
            )
            return

        #
        # Remove leading/trailing slashes.
        #
        segments = [
            segment
            for segment in path.strip("/").split("/")
            if segment
        ]

        if not segments:
            self.root["/"] = PathNode(
                segment="/",
                endpoint=endpoint,
            )
            return

        #
        # Build the hierarchy.
        #
        current: dict[str, PathNode] = self.root

        for index, segment in enumerate(segments):
            if segment not in current:
                current[segment] = PathNode(segment)

            node = current[segment]

            #
            # The final segment represents the actual endpoint.
            #
            if index == len(segments) - 1:
                node.endpoint = endpoint

            current = node.children

    def sort(self) -> None:
        """
        Sort the entire path hierarchy.
        """

        self.root = dict(
            sorted(
                self.root.items(),
                key=lambda item: item[0],
            )
        )

        for node in self.root.values():
            node.sort_children()

    def nodes(self) -> list[PathNode]:
        """
        Return root path nodes in sorted order.
        """

        self.sort()

        return list(self.root.values())
