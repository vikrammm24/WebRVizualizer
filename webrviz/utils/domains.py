"""
Utility functions for working with domain names.

These helpers are intentionally kept independent from the data models so they
can be reused by builders, renderers, exporters and future plugins.
"""

from __future__ import annotations


def get_parent_domain(hostname: str) -> str | None:
    """
    Return the immediate parent domain.

    Examples
    --------
    api.example.com -> example.com
    dev.api.example.com -> api.example.com
    example.com -> None
    localhost -> None
    """

    parts = hostname.split(".")

    if len(parts) <= 2:
        return None

    return ".".join(parts[1:])


def get_root_domain(hostname: str) -> str:
    """
    Return the highest domain in the hierarchy.

    Examples
    --------
    api.example.com -> example.com
    dev.api.example.com -> example.com
    example.com -> example.com
    localhost -> localhost
    """

    parts = hostname.split(".")

    if len(parts) <= 2:
        return hostname

    return ".".join(parts[-2:])


def is_subdomain(hostname: str) -> bool:
    """
    Return True if the hostname is a subdomain.
    """

    return get_parent_domain(hostname) is not None
