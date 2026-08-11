# ADR-003 — Normalized Intermediate Representation

## Status

Accepted

## Context

WebRViz currently allows parsers to produce Endpoint objects directly.

As additional reconnaissance sources are introduced, allowing parsers
to understand the complete Application model would create unnecessary
coupling.

Phase 2 requires a stable boundary between raw reconnaissance data and
application/domain processing.

## Decision

Introduce NormalizedObservation as the intermediate representation
between parser output and the application layer.

The target pipeline is:

    Raw Input
       ↓
    Parser
       ↓
    NormalizedObservation
       ↓
    Application Processing
       ↓
    Canonical Application Model

## Consequences

### Positive

- Parsers remain simple.
- Future parsers do not need to understand Application internals.
- Rendering remains independent of parsers.
- Enrichment can operate after normalization.
- Parser migration can happen incrementally.

### Negative

- There is an additional data-model object.
- Phase 1 parsers initially produce their existing Endpoint objects.
- A later migration step is required.

## Rejected alternative

Direct parser-to-ApplicationBuilder coupling was rejected because it
would make each parser dependent on application construction details.

## Scope

This ADR defines the architecture only.

It does not migrate existing parsers or change Phase 1 behavior.
