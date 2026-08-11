# M7-H — Enrichment Architecture

## Purpose

WebRViz requires a controlled architecture for adding metadata,
technologies, parameters, and relationships without turning
ApplicationBuilder into a monolithic component.

---

## Target pipeline

    Raw Tool Output
          ↓
        Parser
          ↓
    NormalizedObservation
          ↓
    EnrichmentPipeline
          ↓
    EnrichmentResult
          ↓
    Canonical Application State

---

## Enricher responsibility

An enricher:

1. Receives an EnrichmentContext.
2. Reads normalized observation data.
3. Produces an EnrichmentResult.

An enricher does not directly mutate:

- Application
- Host
- Endpoint

---

## EnrichmentContext

The context currently contains:

- NormalizedObservation

Additional read-only context may be introduced later if required.

---

## EnrichmentResult

An enrichment result may contain:

- EndpointMetadata
- Parameters
- Technologies
- Relationships

All result collections use immutable set semantics.

---

## Pipeline responsibility

The pipeline:

- executes enrichers
- preserves execution order
- returns enrichment results

The pipeline does not:

- merge canonical state
- mutate endpoints
- resolve conflicting metadata
- render output

---

## Merge responsibility

Metadata merging remains the responsibility of the merge layer
defined in M7-F.

The enrichment pipeline does not redefine merge semantics.

---

## ApplicationBuilder

ApplicationBuilder remains unchanged during M7-H.

Integration with real enrichment stages is deferred until later
milestones.

---

## Design principle

Detection and enrichment produce evidence.

The canonical model decides how that evidence becomes application state.

---

## Future stages

Potential future enrichers include:

- HTTP metadata enricher
- technology enricher
- parameter enricher
- relationship enricher

These are not implemented during M7-H.
