from dataclasses import dataclass

from webrviz.models.endpoint import Endpoint
from webrviz.models.endpoint_identity import EndpointIdentity
from webrviz.models.source import Source


@dataclass(frozen=True, slots=True)
class NormalizedObservation:
    """
    Normalized representation produced by a reconnaissance parser.

    This object forms the boundary between parser output and the
    application/domain layer.

    Parsers should produce normalized observations rather than directly
    manipulating Application, Host, or rendering objects.
    """

    endpoint: Endpoint
    source: Source
    raw_value: str | None = None

    @property
    def identity(self) -> EndpointIdentity:
        """
        Return the canonical identity of the normalized endpoint.
        """
        return self.endpoint.canonical_identity()
