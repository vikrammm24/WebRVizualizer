from __future__ import annotations

from rich.console import Console
from rich.tree import Tree


class Printer:
    """
    Handles rendering Rich objects to the terminal.

    This class performs no formatting or traversal.
    """

    def __init__(self) -> None:
        self.console = Console()

    def print(self, tree: Tree) -> None:
        """
        Print a Rich Tree.
        """

        self.console.print(tree)
