from dataclasses import dataclass, field

from webrviz.models.endpoint_metadata import EndpointMetadata
from webrviz.models.parameter import Parameter
from webrviz.models.relationship import Relationship
from webrviz.models.technology import Technology


@dataclass(frozen=True, slots=True)
class EnrichmentResult:
    """
    Result produced by an enrichment stage.

    Every collection is immutable so enrichment stages cannot
    accidentally mutate another stage's result.
    """

    metadata: EndpointMetadata = field(
        default_factory=EndpointMetadata
    )

    parameters: frozenset[Parameter] = field(
        default_factory=frozenset
    )

    technologies: frozenset[Technology] = field(
        default_factory=frozenset
    )

    relationships: frozenset[Relationship] = field(
        default_factory=frozenset
    )

    @classmethod
    def empty(cls) -> "EnrichmentResult":
        """
        Return an empty enrichment result.
        """
        return cls()
