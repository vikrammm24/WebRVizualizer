from .domains import (
    get_parent_domain,
    get_root_domain,
    is_subdomain,
)
from .url import endpoint_from_url

__all__ = [
    "endpoint_from_url",
    "get_parent_domain",
    "get_root_domain",
    "is_subdomain",
]
