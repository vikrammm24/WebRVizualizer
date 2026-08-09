from pathlib import Path

from webrviz.models.endpoint import Endpoint
from webrviz.parsers.httpx import HttpxParser
from webrviz.parsers.katana import KatanaParser


def test_httpx_parser_reads_urls(tmp_path: Path) -> None:
    input_file = tmp_path / "httpx.txt"

    input_file.write_text(
        "https://example.com\nhttps://example.com/login\n",
        encoding="utf-8",
    )

    parser = HttpxParser(input_file)

    endpoints = parser.parse()

    assert endpoints == [
        Endpoint(
            scheme="https",
            hostname="example.com",
            path="/",
            port=None,
            query=None,
            full_url="https://example.com",
        ),
        Endpoint(
            scheme="https",
            hostname="example.com",
            path="/login",
            port=None,
            query=None,
            full_url="https://example.com/login",
        ),
    ]


def test_katana_parser_reads_urls(tmp_path: Path) -> None:
    input_file = tmp_path / "katana.txt"

    input_file.write_text(
        "https://example.com/login\nhttps://api.example.com/v1/users\n",
        encoding="utf-8",
    )

    parser = KatanaParser(input_file)

    endpoints = parser.parse()

    assert endpoints == [
        Endpoint(
            scheme="https",
            hostname="example.com",
            path="/login",
            port=None,
            query=None,
            full_url="https://example.com/login",
        ),
        Endpoint(
            scheme="https",
            hostname="api.example.com",
            path="/v1/users",
            port=None,
            query=None,
            full_url="https://api.example.com/v1/users",
        ),
    ]


def test_httpx_parser_skips_blank_lines(tmp_path: Path) -> None:
    input_file = tmp_path / "httpx.txt"

    input_file.write_text(
        "\nhttps://example.com\n\n   \nhttps://example.com/login\n\n",
        encoding="utf-8",
    )

    parser = HttpxParser(input_file)

    endpoints = parser.parse()

    assert len(endpoints) == 2


def test_katana_parser_skips_blank_lines(tmp_path: Path) -> None:
    input_file = tmp_path / "katana.txt"

    input_file.write_text(
        "\nhttps://example.com\n\n   \nhttps://example.com/api\n\n",
        encoding="utf-8",
    )

    parser = KatanaParser(input_file)

    endpoints = parser.parse()

    assert len(endpoints) == 2


def test_httpx_parser_strips_whitespace(tmp_path: Path) -> None:
    input_file = tmp_path / "httpx.txt"

    input_file.write_text(
        "  https://example.com/login  \n",
        encoding="utf-8",
    )

    parser = HttpxParser(input_file)

    endpoints = parser.parse()

    assert endpoints[0].full_url == "https://example.com/login"


def test_katana_parser_strips_whitespace(tmp_path: Path) -> None:
    input_file = tmp_path / "katana.txt"

    input_file.write_text(
        "\t https://example.com/api \t\n",
        encoding="utf-8",
    )

    parser = KatanaParser(input_file)

    endpoints = parser.parse()

    assert endpoints[0].full_url == "https://example.com/api"


def test_httpx_parser_ignores_invalid_port(tmp_path: Path) -> None:
    input_file = tmp_path / "httpx.txt"

    input_file.write_text(
        "https://example.com\nhttps://example.com:invalid\nhttps://example.com/login\n",
        encoding="utf-8",
    )

    parser = HttpxParser(input_file)

    endpoints = parser.parse()

    assert endpoints == [
        Endpoint(
            scheme="https",
            hostname="example.com",
            path="/",
            port=None,
            query=None,
            full_url="https://example.com",
        ),
        Endpoint(
            scheme="https",
            hostname="example.com",
            path="/login",
            port=None,
            query=None,
            full_url="https://example.com/login",
        ),
    ]


def test_katana_parser_ignores_invalid_port(tmp_path: Path) -> None:
    input_file = tmp_path / "katana.txt"

    input_file.write_text(
        "https://example.com\nhttps://example.com:invalid\nhttps://example.com/api\n",
        encoding="utf-8",
    )

    parser = KatanaParser(input_file)

    endpoints = parser.parse()

    assert endpoints == [
        Endpoint(
            scheme="https",
            hostname="example.com",
            path="/",
            port=None,
            query=None,
            full_url="https://example.com",
        ),
        Endpoint(
            scheme="https",
            hostname="example.com",
            path="/api",
            port=None,
            query=None,
            full_url="https://example.com/api",
        ),
    ]
