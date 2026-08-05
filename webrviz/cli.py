from argparse import ArgumentParser
from pathlib import Path

from rich.console import Console
from rich.table import Table

from webrviz.parsers import HttpxParser, KatanaParser
from webrviz.services import ApplicationMerger

console = Console()


def build_parser() -> ArgumentParser:
    """
    Configure the command-line interface.
    """
    parser = ArgumentParser(
        prog="webrviz",
        description="CLI-based Web Application Mapper",
    )

    parser.add_argument(
        "--httpx",
        type=Path,
        help="Path to the httpx output file",
    )

    parser.add_argument(
        "--katana",
        type=Path,
        help="Path to the katana output file",
    )

    return parser

def validate_file(
    parser: ArgumentParser,
    path: Path | None,
    tool_name: str,
) -> None:
    """
    Validate that an input file exists.
    """
    if path is None:
        return

    if not path.is_file():
        parser.error(
            f"{tool_name} file not found.\n\n"
            f"  Provided path : {path}\n"
            f"  Resolved path : {path.resolve()}\n\n"
            "Relative paths are resolved from your current working directory.\n"
            "Use an absolute path or run the command from the directory "
            "where the file exists."
        )

def validate_inputs(parser: ArgumentParser, args) -> None:
    """
    Validate CLI arguments.
    """

    if args.httpx is None and args.katana is None:
        parser.error(
            "At least one input file (--httpx or --katana) is required."
        )

    validate_file(parser, args.httpx, "HTTPX")
    validate_file(parser, args.katana, "Katana")

def print_summary(application) -> None:
    """
    Print a simple application summary.
    """

    table = Table(title="Application Summary")

    table.add_column("Host", style="cyan")
    table.add_column("Endpoints", justify="right")

    total_endpoints = 0

    for host in sorted(application.hosts.values(), key=lambda h: h.hostname):
        endpoint_count = len(host.endpoints)
        total_endpoints += endpoint_count

        table.add_row(
            host.hostname,
            str(endpoint_count),
        )

    console.print(table)

    console.print()
    console.print(f"[bold]Hosts:[/bold] {len(application.hosts)}")
    console.print(f"[bold]Endpoints:[/bold] {total_endpoints}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    validate_inputs(parser, args)

    console.rule("[bold cyan]WebRViz[/bold cyan]")

    merger = ApplicationMerger()

    endpoint_groups = []

    if args.httpx:
        console.print(f"[green][+][/green] Parsing HTTPX: {args.httpx}")

        parser_httpx = HttpxParser(args.httpx)
        endpoint_groups.append(parser_httpx.parse())

    if args.katana:
        console.print(f"[green][+][/green] Parsing Katana: {args.katana}")

        parser_katana = KatanaParser(args.katana)
        endpoint_groups.append(parser_katana.parse())

    application = merger.merge(*endpoint_groups)

    console.print()
    console.print("[bold green]✓ Parsing completed[/bold green]")
    console.print()

    print_summary(application)


if __name__ == "__main__":
    main()
