# ADR-004 — Deterministic Metadata Merge

## Status

Accepted

## Decision

Metadata from multiple observations will be merged using set-union
semantics.

Conflicting values will be preserved rather than overwritten.

Example:

    status 200
    status 403

becomes:

    {200, 403}

## Rationale

Reconnaissance sources can observe different states of the same
endpoint.

Automatically selecting one value would discard evidence and could
produce an incorrect canonical state.

Preserving all observed values provides a deterministic and
information-preserving representation.

## Properties

The merge operation must be:

- commutative
- associative
- idempotent
- deterministic

## Unknown values

Unknown metadata is represented by an empty collection.

Artificial values such as status 0 are not used.

## Source priority

No source is considered authoritative during Milestone 7.

Source-specific priority may be introduced later only if a concrete
requirement justifies it.

## Scope

This decision defines metadata merging only.

It does not determine where metadata is attached to the Endpoint model.
That remains a separate architectural decision.
