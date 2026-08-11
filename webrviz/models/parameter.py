from dataclasses import dataclass
from enum import StrEnum


class ParameterLocation(StrEnum):
    """
    Location where an endpoint parameter is supplied.
    """

    QUERY = "query"
    PATH = "path"
    HEADER = "header"
    COOKIE = "cookie"
    BODY = "body"


@dataclass(frozen=True, slots=True)
class Parameter:
    """
    Represents a parameter associated with an endpoint.

    Parameter extraction and intelligence are intentionally outside
    this model.
    """

    name: str
    location: ParameterLocation

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("parameter name must not be empty")
