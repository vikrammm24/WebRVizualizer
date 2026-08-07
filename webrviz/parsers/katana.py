from pathlib import Path

from webrviz.models.endpoint import Endpoint
from webrviz.parsers.base import BaseParser
from webrviz.utils.url import endpoint_from_url


class KatanaParser(BaseParser):
    """
    Parser for Katana output files.

    Each non-empty line is expected to contain a single discovered URL.
    """

    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)

    def parse(self) -> list[Endpoint]:
        """
        Parse the Katana output file and return a list of discovered endpoints.
        """
        endpoints: list[Endpoint] = []

        with self.file_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                url = line.strip()

                # Skip blank lines
                if not url:
                    continue

                try:
                    endpoint = endpoint_from_url(url)
                    endpoints.append(endpoint)
                except ValueError:
                    # TODO:
                    # Replace this with structured logging in a future milestone.
                    continue

        return endpoints
