def get_parent_domain(hostname: str) -> str | None:
    parts = hostname.split(".")

    if len(parts) <= 1:
        return None

    # Normal two-label domain:
    # example.com -> None
    if len(parts) == 2:
        return None

    # Multi-label public suffixes.
    # example.co.uk -> None
    # api.example.co.uk -> example.co.uk
    if parts[-2:] in [
        ["co", "uk"],
        ["org", "uk"],
        ["ac", "uk"],
        ["gov", "uk"],
    ]:
        if len(parts) == 3:
            return None

        return ".".join(parts[1:])

    # Normal subdomain:
    # api.example.com -> example.com
    # dev.api.example.com -> api.example.com
    return ".".join(parts[1:])


def get_root_domain(hostname: str) -> str:
    parts = hostname.split(".")

    if len(parts) <= 2:
        return hostname

    # example.co.uk -> example.co.uk
    # api.example.co.uk -> example.co.uk
    if parts[-2:] in [
        ["co", "uk"],
        ["org", "uk"],
        ["ac", "uk"],
        ["gov", "uk"],
    ]:
        return ".".join(parts[-3:])

    # api.example.com -> example.com
    # dev.api.example.com -> example.com
    return ".".join(parts[-2:])


def is_subdomain(hostname: str) -> bool:
    return get_parent_domain(hostname) is not None
