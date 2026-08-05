from pathlib import Path

from webrviz.models import Endpoint
from webrviz.parsers.base import BaseParser
from webrviz.utils.url import endpoint_from_url


class HttpxParser(BaseParser):
    """
    Parser for httpx output files.

    Each non-empty line is expected to contain a single URL.
    """

    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)

    def parse(self) -> list[Endpoint]:
        """
        Parse the httpx output file and return a list of discovered endpoints.
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
                    # Ignore malformed URLs for now.
                    # Later phases can add proper logging.
                    continue

        return endpoints
