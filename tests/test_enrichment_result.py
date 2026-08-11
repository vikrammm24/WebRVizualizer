from webrviz.enrichment.result import EnrichmentResult
from webrviz.models.endpoint_metadata import EndpointMetadata
from webrviz.models.parameter import (
    Parameter,
    ParameterLocation,
)
from webrviz.models.relationship import (
    Relationship,
    RelationshipType,
)
from webrviz.models.technology import Technology
from webrviz.models.endpoint_identity import EndpointIdentity


def make_identity(path: str) -> EndpointIdentity:
    return EndpointIdentity(
        scheme="https",
        hostname="example.com",
        port=None,
        path=path,
    )


def test_empty_result_contains_no_enrichment() -> None:
    result = EnrichmentResult.empty()

    assert result.metadata == EndpointMetadata()
    assert result.parameters == frozenset()
    assert result.technologies == frozenset()
    assert result.relationships == frozenset()


def test_result_can_contain_metadata() -> None:
    metadata = EndpointMetadata.from_values(
        status_code=200,
    )

    result = EnrichmentResult(
        metadata=metadata,
    )

    assert result.metadata == metadata


def test_result_can_contain_parameter() -> None:
    parameter = Parameter(
        name="id",
        location=ParameterLocation.QUERY,
    )

    result = EnrichmentResult(
        parameters=frozenset({parameter}),
    )

    assert result.parameters == frozenset({parameter})


def test_result_can_contain_technology() -> None:
    technology = Technology("nginx")

    result = EnrichmentResult(
        technologies=frozenset({technology}),
    )

    assert result.technologies == frozenset({technology})


def test_result_can_contain_relationship() -> None:
    relationship = Relationship(
        source=make_identity("/login"),
        type=RelationshipType.REDIRECTS_TO,
        target=make_identity("/dashboard"),
    )

    result = EnrichmentResult(
        relationships=frozenset({relationship}),
    )

    assert result.relationships == frozenset(
        {relationship}
    )


def test_result_is_immutable() -> None:
    result = EnrichmentResult.empty()

    try:
        result.parameters = frozenset()
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "EnrichmentResult should be immutable"
        )
