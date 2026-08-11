from collections.abc import Iterable

from webrviz.enrichment.base import Enricher
from webrviz.enrichment.context import EnrichmentContext
from webrviz.enrichment.result import EnrichmentResult


class EnrichmentPipeline:
    """
    Executes enrichment stages in sequence.

    The pipeline does not mutate the canonical application model.
    It collects enrichment results for later application by the
    application/domain layer.
    """

    def __init__(
        self,
        enrichers: Iterable[Enricher] = (),
    ) -> None:
        self._enrichers = tuple(enrichers)

    def enrich(
        self,
        context: EnrichmentContext,
    ) -> tuple[EnrichmentResult, ...]:
        """
        Execute all configured enrichment stages.

        Results are returned in enricher registration order.
        """
        return tuple(
            enricher.enrich(context)
            for enricher in self._enrichers
        )
