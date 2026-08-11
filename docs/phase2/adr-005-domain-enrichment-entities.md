# ADR-005 — Parameter, Technology and Relationship Models

## Status

Accepted

## Decision

WebRViz will represent parameters, technologies, and relationships as
small dedicated domain models.

### Parameter

Parameter contains:

- name
- location

### Technology

Technology initially contains:

- name

### Relationship

Relationship contains:

- source EndpointIdentity
- RelationshipType
- target EndpointIdentity

---

## Rationale

Dedicated models provide clear semantics while avoiding premature
implementation complexity.

Parameters, technologies, and relationships have different lifecycles
and should not be represented as arbitrary dictionaries.

---

## Parameter location

Parameter location uses a fixed enum:

- query
- path
- header
- cookie
- body

This prevents inconsistent location strings.

---

## Technology complexity

Technology versions, confidence scores, detection evidence, and source
information are intentionally deferred.

These can be added later if concrete requirements emerge.

---

## Relationship complexity

The relationship system intentionally remains small.

WebRViz will not introduce a generic graph database or unrestricted
relationship vocabulary during Phase 2 architecture work.

---

## Scope

This ADR defines the domain models only.

Detection and discovery logic belong to later milestones.
