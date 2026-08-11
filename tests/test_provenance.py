from webrviz.models.endpoint import Endpoint
from webrviz.models.observation import Observation
from webrviz.models.source import Source


def test_provenance_belongs_to_observation() -> None:
    endpoint = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/admin",
        port=None,
        query=None,
        full_url="https://example.com/admin",
    )

    observation = Observation(
        endpoint=endpoint,
        source=Source("httpx"),
    )

    assert observation.source.name == "httpx"
    assert not hasattr(endpoint, "source")


def test_multiple_sources_can_observe_same_endpoint() -> None:
    endpoint = Endpoint(
        scheme="https",
        hostname="example.com",
        path="/admin",
        port=None,
        query=None,
        full_url="https://example.com/admin",
    )

    observations = {
        Observation(
            endpoint=endpoint,
            source=Source("httpx"),
        ),
        Observation(
            endpoint=endpoint,
            source=Source("katana"),
        ),
    }

    assert len(observations) == 2

    sources = {
        observation.source.name
        for observation in observations
    }

    assert sources == {"httpx", "katana"}
