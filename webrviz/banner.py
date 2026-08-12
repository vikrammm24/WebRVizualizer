from importlib.metadata import PackageNotFoundError, version


BANNER = r"""
██╗    ██╗███████╗██████╗ ██████╗ ██╗   ██╗██╗███████╗
██║    ██║██╔════╝██╔══██╗██╔══██╗██║   ██║██║╚══███╔╝
██║ █╗ ██║█████╗  ██████╔╝██████╔╝██║   ██║██║  ███╔╝
██║███╗██║██╔══╝  ██╔══██╗██╔══██╗╚██╗ ██╔╝██║ ███╔╝
╚███╔███╔╝███████╗██████╔╝██║  ██║ ╚████╔╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝

    Web Reconnaissance & Visualization
    ────────────────────────────────────

    [*] Discover  [*] Parse  [*] Normalize  [*] Visualize
"""


def get_version() -> str:
    try:
        return version("webrviz")
    except PackageNotFoundError:
        return "dev"


def print_banner() -> None:
    print(BANNER)
    print(f"    WebRViz v{get_version()}")
    print()
