import pytest

from webrviz.models.endpoint import Endpoint
from webrviz.models.observation import Observation
from webrviz.models.source import Source


def make_endpoint(
    query: str | None = None,
) -> Endpoint:
    return Endpoint(
        scheme="https",
        hostname="example.com",
        path="/login",
        port=None,
        query=query,
        full_url=(
            "https://example.com/login"
            if query is None
            else f"https://example.com/login?{query}"
        ),
    )


def test_source_stores_source_name() -> None:
    source = Source("httpx")

    assert source.name == "httpx"


def test_source_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="source name"):
        Source("")


def test_observation_stores_endpoint_and_source() -> None:
    endpoint = make_endpoint()
    source = Source("httpx")

    observation = Observation(
        endpoint=endpoint,
        source=source,
    )

    assert observation.endpoint is endpoint
    assert observation.source is source


def test_observation_can_preserve_raw_value() -> None:
    endpoint = make_endpoint()

    observation = Observation(
        endpoint=endpoint,
        source=Source("httpx"),
        raw_value="https://example.com/login",
    )

    assert observation.raw_value == "https://example.com/login"


def test_observation_identity_comes_from_endpoint() -> None:
    endpoint = make_endpoint()

    observation = Observation(
        endpoint=endpoint,
        source=Source("httpx"),
    )

    assert observation.identity == endpoint.canonical_identity()


def test_httpx_and_katana_are_distinct_observations() -> None:
    endpoint = make_endpoint()

    httpx_observation = Observation(
        endpoint=endpoint,
        source=Source("httpx"),
    )

    katana_observation = Observation(
        endpoint=endpoint,
        source=Source("katana"),
    )

    assert httpx_observation != katana_observation


def test_httpx_and_katana_can_refer_to_same_endpoint() -> None:
    endpoint = make_endpoint()

    httpx_observation = Observation(
        endpoint=endpoint,
        source=Source("httpx"),
    )

    katana_observation = Observation(
        endpoint=endpoint,
        source=Source("katana"),
    )

    assert (
        httpx_observation.identity
        == katana_observation.identity
    )


def test_query_variations_can_produce_same_endpoint_identity() -> None:
    first = Observation(
        endpoint=make_endpoint("id=1"),
        source=Source("httpx"),
    )

    second = Observation(
        endpoint=make_endpoint("id=2"),
        source=Source("katana"),
    )

    assert first.identity == second.identity
