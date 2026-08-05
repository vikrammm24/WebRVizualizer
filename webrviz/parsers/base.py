from abc import ABC, abstractmethod
from pathlib import Path

from webrviz.models import Endpoint


class BaseParser(ABC):
    """
    Abstract base class for all reconnaissance parsers.
    """

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    @abstractmethod
    def parse(self) -> list[Endpoint]:
        """
        Parse the input file and return discovered endpoints.
        """
        raise NotImplementedError
