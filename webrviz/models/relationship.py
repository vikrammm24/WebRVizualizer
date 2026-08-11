from dataclasses import dataclass
from enum import StrEnum

from webrviz.models.endpoint_identity import EndpointIdentity


class RelationshipType(StrEnum):
    """
    Semantic relationship between WebRViz entities.
    """

    REDIRECTS_TO = "redirects_to"
    REFERENCES = "references"
    DISCOVERED_FROM = "discovered_from"
    BELONGS_TO = "belongs_to"
    EXPOSES = "exposes"
    AUTHENTICATES = "authenticates"


@dataclass(frozen=True, slots=True)
class Relationship:
    """
    Represents a relationship between canonical endpoints.

    Relationship discovery is outside the responsibility of this model.
    """

    source: EndpointIdentity
    type: RelationshipType
    target: EndpointIdentity
