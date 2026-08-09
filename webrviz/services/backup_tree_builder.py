from __future__ import annotations

from rich.tree import Tree

from webrviz.models.application import Application
from webrviz.models.host import Host


class TreeBuilder:
    """
    Builds a Rich Tree from an Application.

    This class contains no printing logic.
    It is only responsible for converting the application model
    into a Rich Tree.
    """

    @staticmethod
    def build(application: Application) -> Tree:
        """
        Build and return a Rich Tree representing the application.
        """

        tree = Tree("[bold cyan]Application[/]")

        for host in application.root_hosts():
            TreeBuilder._add_host(tree, host)

        return tree

    @staticmethod
    def _add_host(parent: Tree, host: Host) -> None:
        """
        Recursively add a Host and its descendants to the tree.
        """

        host_node = parent.add(f"[bold green]{host.hostname}[/]")

        #
        # Add endpoints.
        #
        for endpoint in host.endpoints:
            host_node.add(f"[white]{endpoint.path}[/]")

        #
        # Add child hosts.
        #
        for child in host.children.values():
            TreeBuilder._add_host(host_node, child)
