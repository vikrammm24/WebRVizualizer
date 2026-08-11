from webrviz.enrichment.base import Enricher
from webrviz.enrichment.context import EnrichmentContext
from webrviz.enrichment.noop import NoOpEnricher
from webrviz.enrichment.pipeline import EnrichmentPipeline
from webrviz.enrichment.result import EnrichmentResult
from webrviz.models.endpoint import Endpoint
from webrviz.models.normalized_observation import NormalizedObservation
from webrviz.models.source import Source


def make_context() -> EnrichmentContext:
    endpoint = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=None,
        full_url="https://example.com/login",
    )

    observation = NormalizedObservation(
        endpoint=endpoint,
        source=Source("httpx"),
    )

    return EnrichmentContext(
        observation=observation,
    )


def test_context_stores_observation() -> None:
    context = make_context()

    assert context.observation.source.name == "httpx"


def test_noop_enricher_returns_empty_result() -> None:
    enricher = NoOpEnricher()

    result = enricher.enrich(make_context())

    assert result == EnrichmentResult.empty()


def test_pipeline_with_no_enrichers_returns_empty_tuple() -> None:
    pipeline = EnrichmentPipeline()

    results = pipeline.enrich(make_context())

    assert results == ()


def test_pipeline_executes_enricher() -> None:
    pipeline = EnrichmentPipeline(
        enrichers=[NoOpEnricher()],
    )

    results = pipeline.enrich(make_context())

    assert len(results) == 1
    assert results[0] == EnrichmentResult.empty()


def test_pipeline_preserves_enricher_order() -> None:
    execution_order: list[str] = []

    class FirstEnricher(Enricher):
        def enrich(
            self,
            context: EnrichmentContext,
        ) -> EnrichmentResult:
            execution_order.append("first")
            return EnrichmentResult.empty()

    class SecondEnricher(Enricher):
        def enrich(
            self,
            context: EnrichmentContext,
        ) -> EnrichmentResult:
            execution_order.append("second")
            return EnrichmentResult.empty()

    pipeline = EnrichmentPipeline(
        enrichers=[
            FirstEnricher(),
            SecondEnricher(),
        ],
    )

    pipeline.enrich(make_context())

    assert execution_order == [
        "first",
        "second",
    ]


def test_pipeline_returns_one_result_per_enricher() -> None:
    pipeline = EnrichmentPipeline(
        enrichers=[
            NoOpEnricher(),
            NoOpEnricher(),
            NoOpEnricher(),
        ],
    )

    results = pipeline.enrich(make_context())

    assert len(results) == 3
    assert all(
        result == EnrichmentResult.empty()
        for result in results
    )
