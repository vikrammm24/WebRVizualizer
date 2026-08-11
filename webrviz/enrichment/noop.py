from webrviz.enrichment.base import Enricher
from webrviz.enrichment.context import EnrichmentContext
from webrviz.enrichment.result import EnrichmentResult


class NoOpEnricher(Enricher):
    """
    Enricher that intentionally produces no enrichment.

    Useful for testing pipeline mechanics and as a safe default stage.
    """

    def enrich(
        self,
        context: EnrichmentContext,
    ) -> EnrichmentResult:
        return EnrichmentResult.empty()
