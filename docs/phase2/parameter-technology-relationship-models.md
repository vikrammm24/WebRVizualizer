# M7-G — Parameter, Technology & Relationship Models

## Parameter

A Parameter represents a named input associated with an endpoint.

Fields:

- name
- location

Supported locations:

- query
- path
- header
- cookie
- body

Parameter extraction is not implemented during M7.

---

## Technology

A Technology represents a technology associated with an endpoint
or host.

Current fields:

- name

Version information is intentionally excluded until a concrete
requirement exists.

Technology detection is not implemented during M7.

---

## Relationship

A Relationship represents a semantic connection between canonical
endpoint identities.

Fields:

- source
- type
- target

Supported relationship types:

- redirects_to
- references
- discovered_from
- belongs_to
- exposes
- authenticates

Relationships reference EndpointIdentity rather than Endpoint objects.

Relationship discovery is not implemented during M7.

---

## Design principles

### Parameters

Parameter identity is:

    name + location

The same parameter name at different locations represents different
parameters.

Example:

    query:id

and:

    header:id

are distinct.

### Technologies

Technology identity is currently based on its name.

Version detection is deferred.

### Relationships

Relationships are immutable and deterministic.

A relationship is identified by:

    source + type + target

The model does not implement a generic graph database.

---

## Explicitly deferred

M7 does not implement:

- parameter extraction
- parameter value analysis
- technology detection
- technology fingerprinting
- version detection
- relationship discovery
- graph traversal
- graph persistence
