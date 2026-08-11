# ADR-002 — Observation and Provenance Model

## Status

Accepted

## Context

WebRViz receives information from multiple reconnaissance tools.

The same endpoint may be discovered by multiple sources.

For example:

    HTTPX → https://example.com/login
    Katana → https://example.com/login

These are separate observations but refer to the same canonical endpoint.

The model must preserve provenance without creating duplicate endpoints.

---

## Decision

WebRViz distinguishes between:

1. Observation
2. Canonical endpoint state

An Observation represents evidence produced by a specific source.

A canonical Endpoint represents the normalized attack-surface entity.

Conceptually:

    Source
       │
       ▼
    Observation
       │
       ▼
    Endpoint Identity
       │
       ▼
    Canonical Endpoint

---

## Observation

An Observation contains:

- Endpoint
- Source
- Optional raw input value

The observation is immutable.

---

## Source

Sources are represented using a string-backed value rather than a fixed enum.

Examples:

    httpx
    katana
    subfinder
    sublist3r

This allows new reconnaissance tools to be introduced without modifying
the core model.

---

## Provenance ownership

Provenance belongs to the Observation.

The Endpoint does not directly own a source field at this stage.

This prevents the URL entity from becoming coupled to a specific
reconnaissance tool.

---

## Canonical identity

Observations referring to the same canonical endpoint identity can later
be merged into one canonical endpoint.

For example:

    Observation(httpx, /login)
    Observation(katana, /login)

becomes:

    Canonical Endpoint
        /login
        sources:
            httpx
            katana

The merge mechanism is intentionally not implemented during this
architectural milestone.

---

## Observation history

WebRViz will not implement a full event/history system during Milestone 7.

Timestamps, historical state tracking, event replay, and change history
are deferred unless a later requirement justifies them.

---

## Field-level provenance

WebRViz will not initially track provenance independently for every
metadata field.

For example, the initial model does not require:

    status:
        value: 200
        source: httpx

Field-level provenance can be introduced later if conflicting metadata
requires it.

---

## Rationale

This model:

- preserves evidence
- supports multiple reconnaissance sources
- avoids duplicate canonical endpoints
- keeps parsers independent
- avoids premature event/history infrastructure
- provides an extension point for future enrichment
