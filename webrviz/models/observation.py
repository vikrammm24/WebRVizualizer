from dataclasses import dataclass

from webrviz.models.endpoint import Endpoint
from webrviz.models.endpoint_identity import EndpointIdentity
from webrviz.models.source import Source


@dataclass(frozen=True, slots=True)
class Observation:
    """
    Represents a single observation produced by a reconnaissance source.

    An observation is evidence about an endpoint. It is not itself the
    canonical application state.
    """

    endpoint: Endpoint
    source: Source
    raw_value: str | None = None

    @property
    def identity(self) -> EndpointIdentity:
        """
        Return the canonical identity of the observed endpoint.
        """
        return self.endpoint.canonical_identity()
