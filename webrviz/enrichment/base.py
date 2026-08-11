from abc import ABC, abstractmethod

from webrviz.enrichment.context import EnrichmentContext
from webrviz.enrichment.result import EnrichmentResult


class Enricher(ABC):
    """
    Base contract for Phase 2 enrichment stages.

    Enrichers inspect normalized observations and produce immutable
    enrichment results.

    Enrichers must not directly mutate Application, Host, or Endpoint.
    """

    @abstractmethod
    def enrich(
        self,
        context: EnrichmentContext,
    ) -> EnrichmentResult:
        """
        Produce enrichment information for an observation.
        """
        raise NotImplementedError
