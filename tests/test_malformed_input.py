from pathlib import Path

from webrviz.parsers.httpx import HttpxParser
from webrviz.parsers.katana import KatanaParser


def test_httpx_parser_empty_file_returns_no_endpoints(
    tmp_path: Path,
) -> None:
    input_file = tmp_path / "httpx.txt"
    input_file.write_text("", encoding="utf-8")

    parser = HttpxParser(input_file)

    endpoints = parser.parse()

    assert endpoints == []


def test_katana_parser_empty_file_returns_no_endpoints(
    tmp_path: Path,
) -> None:
    input_file = tmp_path / "katana.txt"
    input_file.write_text("", encoding="utf-8")

    parser = KatanaParser(input_file)

    endpoints = parser.parse()

    assert endpoints == []


def test_httpx_parser_whitespace_only_file_returns_no_endpoints(
    tmp_path: Path,
) -> None:
    input_file = tmp_path / "httpx.txt"
    input_file.write_text(
        "   \n"
        "\t\n"
        "    \n",
        encoding="utf-8",
    )

    parser = HttpxParser(input_file)

    endpoints = parser.parse()

    assert endpoints == []


def test_katana_parser_whitespace_only_file_returns_no_endpoints(
    tmp_path: Path,
) -> None:
    input_file = tmp_path / "katana.txt"
    input_file.write_text(
        "   \n"
        "\t\n"
        "    \n",
        encoding="utf-8",
    )

    parser = KatanaParser(input_file)

    endpoints = parser.parse()

    assert endpoints == []


def test_httpx_parser_skips_invalid_urls(
    tmp_path: Path,
) -> None:
    input_file = tmp_path / "httpx.txt"

    input_file.write_text(
        "https://example.com\n"
        "not-a-valid-url\n"
        "https://example.com/login\n",
        encoding="utf-8",
    )

    parser = HttpxParser(input_file)

    endpoints = parser.parse()

    assert len(endpoints) == 2
    assert endpoints[0].full_url == "https://example.com"
    assert endpoints[1].full_url == "https://example.com/login"


def test_katana_parser_skips_invalid_urls(
    tmp_path: Path,
) -> None:
    input_file = tmp_path / "katana.txt"

    input_file.write_text(
        "https://example.com\n"
        "not-a-valid-url\n"
        "https://example.com/api\n",
        encoding="utf-8",
    )

    parser = KatanaParser(input_file)

    endpoints = parser.parse()

    assert len(endpoints) == 2
    assert endpoints[0].full_url == "https://example.com"
    assert endpoints[1].full_url == "https://example.com/api"
