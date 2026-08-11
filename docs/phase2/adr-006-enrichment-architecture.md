# ADR-006 — Enrichment Pipeline Architecture

## Status

Accepted

## Decision

WebRViz will use a staged enrichment architecture.

    NormalizedObservation
            ↓
      EnrichmentContext
            ↓
          Enricher
            ↓
      EnrichmentResult
            ↓
      Canonical Model

Multiple enrichers may be executed by an EnrichmentPipeline.

---

## Responsibilities

### Parser

Converts raw reconnaissance data into normalized observations.

### Enricher

Produces additional evidence or metadata from normalized observations.

### Pipeline

Controls enricher execution.

### Merge layer

Applies deterministic metadata merge semantics.

### Canonical model

Represents the current application state.

---

## Mutation policy

Enrichers must not directly mutate Application, Host, or Endpoint.

This prevents enrichment stages from becoming tightly coupled to the
application object graph.

---

## Result policy

Enrichment stages return immutable results.

This allows results to be:

- inspected
- tested
- merged
- serialized
- replayed

without hidden side effects.

---

## ApplicationBuilder

ApplicationBuilder is not converted into an enrichment coordinator
during M7.

Integration is deferred until concrete enrichment stages exist.

---

## Rationale

This architecture prevents a single component from accumulating:

- parser logic
- detection logic
- merge logic
- relationship logic
- rendering logic

The resulting system remains modular and testable.
