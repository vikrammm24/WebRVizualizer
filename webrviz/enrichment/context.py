from dataclasses import dataclass

from webrviz.models.normalized_observation import NormalizedObservation


@dataclass(frozen=True, slots=True)
class EnrichmentContext:
    """
    Immutable input supplied to an enrichment stage.

    Enrichers inspect the normalized observation and return enrichment
    results without directly mutating the application model.
    """

    observation: NormalizedObservation
