from __future__ import annotations

from argparse import ArgumentParser
from itertools import chain
from pathlib import Path
import sys

from webrviz.parsers.httpx import HttpxParser
from webrviz.parsers.katana import KatanaParser
from webrviz.services.builder import ApplicationBuilder


def validate_file(path: Path, name: str) -> None:
    """
    Validate that a supplied file exists.
    """

    if path.exists():
        return

    resolved = path.resolve()

    print()

    print(f"{name} file not found.\n")

    print(f"Provided path : {path}")
    print(f"Resolved path : {resolved}")

    print("\nRelative paths are resolved from your current working directory.")

    print(
        "Use an absolute path or run the command from the directory where the file exists."
    )

    sys.exit(1)


def main() -> None:
    parser = ArgumentParser(
        prog="webrviz",
        description="WebRViz - Web Application Visualizer",
    )

    parser.add_argument(
        "--httpx",
        type=Path,
        help="Path to httpx output",
    )

    parser.add_argument(
        "--katana",
        type=Path,
        help="Path to katana output",
    )

    args = parser.parse_args()

    parsers = []

    if args.httpx:
        validate_file(args.httpx, "HTTPX")
        parsers.append(HttpxParser(args.httpx))

    if args.katana:
        validate_file(args.katana, "Katana")
        parsers.append(KatanaParser(args.katana))

    if not parsers:
        parser.error("No input files supplied.")

    endpoints = chain.from_iterable(parser.parse() for parser in parsers)

    application = ApplicationBuilder.build(endpoints)

    #
    # Temporary summary.
    for host in application.root_hosts():
        print(host.hostname)

        for child in host.sorted_children:
            print("   └──", child.hostname)
    # Will be replaced in Milestone 5.
    #

    print()

    print("Application Summary\n")

    endpoint_count = 0

    for host in application.all_hosts():
        count = len(host.endpoints)

        endpoint_count += count

        print(f"{host.hostname:<25} {count}")

    print()

    print(f"Hosts: {len(application.hosts)}")
    print(f"Endpoints: {endpoint_count}")
