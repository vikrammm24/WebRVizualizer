from webrviz.models.endpoint import Endpoint
from webrviz.models.normalized_observation import NormalizedObservation
from webrviz.models.source import Source


def make_endpoint(
    query: str | None = None,
) -> Endpoint:
    full_url = "https://example.com/login"

    if query is not None:
        full_url += f"?{query}"

    return Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=query,
        full_url=full_url,
    )


def test_normalized_observation_stores_endpoint() -> None:
    endpoint = make_endpoint()

    observation = NormalizedObservation(
        endpoint=endpoint,
        source=Source("httpx"),
    )

    assert observation.endpoint is endpoint


def test_normalized_observation_stores_source() -> None:
    observation = NormalizedObservation(
        endpoint=make_endpoint(),
        source=Source("httpx"),
    )

    assert observation.source.name == "httpx"


def test_normalized_observation_can_preserve_raw_value() -> None:
    observation = NormalizedObservation(
        endpoint=make_endpoint(),
        source=Source("httpx"),
        raw_value="https://example.com/login",
    )

    assert observation.raw_value == "https://example.com/login"


def test_normalized_observation_exposes_canonical_identity() -> None:
    endpoint = make_endpoint()

    observation = NormalizedObservation(
        endpoint=endpoint,
        source=Source("httpx"),
    )

    assert observation.identity == endpoint.canonical_identity()


def test_query_variations_share_identity() -> None:
    first = NormalizedObservation(
        endpoint=make_endpoint("id=1"),
        source=Source("httpx"),
    )

    second = NormalizedObservation(
        endpoint=make_endpoint("id=2"),
        source=Source("katana"),
    )

    assert first.identity == second.identity


def test_different_sources_remain_distinct() -> None:
    endpoint = make_endpoint()

    first = NormalizedObservation(
        endpoint=endpoint,
        source=Source("httpx"),
    )

    second = NormalizedObservation(
        endpoint=endpoint,
        source=Source("katana"),
    )

    assert first != second
