# M7-E — Normalized Intermediate Representation

## Purpose

The normalized intermediate representation provides a stable boundary
between reconnaissance parsers and the WebRViz application/domain model.

The goal is to prevent individual parsers from becoming coupled to:

- Application
- Host
- ApplicationBuilder
- PathTree
- Renderer
- CLI

---

## Pipeline

The target Phase 2 pipeline is:

    Raw Tool Output
          ↓
        Parser
          ↓
    NormalizedObservation
          ↓
      Application
       Processing
          ↓
     Canonical Model

---

## NormalizedObservation

A NormalizedObservation contains:

- Endpoint
- Source
- Optional raw value

It may expose the canonical endpoint identity.

---

## Parser responsibility

A parser is responsible for:

1. Reading raw tool output.
2. Validating relevant input.
3. Converting the input into an Endpoint.
4. Associating the source.
5. Producing NormalizedObservation objects.

---

## Parser non-responsibilities

A parser must not:

- Build Application objects.
- Construct Host hierarchy.
- Modify PathTree.
- Render output.
- Access Rich.
- Implement visualization logic.
- Perform unrelated enrichment.
- Manage global application state.

---

## Why the intermediate representation exists

Without an intermediate representation:

    HTTPX Parser
         ↓
    ApplicationBuilder
         ↓
    Application

A future parser must understand the internal Application model.

With the intermediate representation:

    HTTPX ──────┐
    Katana ─────┤
    Future ─────┤
                ↓
    NormalizedObservation
                ↓
       Application layer

Future parsers therefore only need to understand the normalized
input contract.

---

## Current implementation compatibility

Phase 1 parsers are not migrated to this interface during M7-E.

The interface is introduced first so that migration can occur as a
controlled later change.

Existing Phase 1 behavior remains unchanged.

---

## Design principle

Parsers describe what was found.

The application layer decides what that information means.
