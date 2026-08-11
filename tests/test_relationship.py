from webrviz.models.endpoint_identity import EndpointIdentity
from webrviz.models.relationship import (
    Relationship,
    RelationshipType,
)


def make_identity(path: str) -> EndpointIdentity:
    return EndpointIdentity(
        scheme="https",
        hostname="example.com",
        port=None,
        path=path,
    )


def test_relationship_stores_source_type_and_target() -> None:
    source = make_identity("/login")
    target = make_identity("/dashboard")

    relationship = Relationship(
        source=source,
        type=RelationshipType.REDIRECTS_TO,
        target=target,
    )

    assert relationship.source == source
    assert relationship.type == RelationshipType.REDIRECTS_TO
    assert relationship.target == target


def test_relationship_types_are_defined() -> None:
    assert RelationshipType.REDIRECTS_TO.value == "redirects_to"
    assert RelationshipType.REFERENCES.value == "references"
    assert RelationshipType.DISCOVERED_FROM.value == "discovered_from"
    assert RelationshipType.BELONGS_TO.value == "belongs_to"
    assert RelationshipType.EXPOSES.value == "exposes"
    assert RelationshipType.AUTHENTICATES.value == "authenticates"


def test_same_relationships_are_equal() -> None:
    source = make_identity("/login")
    target = make_identity("/dashboard")

    first = Relationship(
        source=source,
        type=RelationshipType.REDIRECTS_TO,
        target=target,
    )

    second = Relationship(
        source=source,
        type=RelationshipType.REDIRECTS_TO,
        target=target,
    )

    assert first == second


def test_relationship_type_is_part_of_identity() -> None:
    source = make_identity("/login")
    target = make_identity("/dashboard")

    redirect = Relationship(
        source=source,
        type=RelationshipType.REDIRECTS_TO,
        target=target,
    )

    reference = Relationship(
        source=source,
        type=RelationshipType.REFERENCES,
        target=target,
    )

    assert redirect != reference


def test_relationship_is_immutable() -> None:
    source = make_identity("/login")
    target = make_identity("/dashboard")

    relationship = Relationship(
        source=source,
        type=RelationshipType.REDIRECTS_TO,
        target=target,
    )

    try:
        relationship.target = source
    except AttributeError:
        pass
    else:
        raise AssertionError("Relationship should be immutable")
