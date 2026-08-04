from argparse import ArgumentParser
from pathlib import Path

from rich.console import Console

console = Console()


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="webrviz", description="CLI Web Application Mapper")

    parser.add_argument("--httpx", type=Path, help="Path to httpx output")

    parser.add_argument("--katana", type=Path, help="Path to katana output")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.httpx and not args.httpx.is_file():
        parser.error(f"httpx file not found: {args.httpx}")

    if args.katana and not args.katana.is_file():
        parser.error(f"katana file not found: {args.katana}")

    console.rule("[bold cyan]WebRViz[/bold cyan]")

    console.print("[green]Loading files[/green]")

    console.print(f"HTTPX : {args.httpx}")
    console.print(f"Katana: {args.katana}")

    console.print("\n[bold green]Project initialized successfully[/bold green]")
