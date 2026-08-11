# M7-F — Metadata Merge Rules

## Purpose

WebRViz may receive metadata about the same canonical endpoint from
multiple reconnaissance sources.

Metadata merging must be deterministic and must not silently destroy
conflicting observations.

---

## Merge strategy

Metadata collections use set-union semantics.

For two metadata objects A and B:

    merge(A, B) = A ∪ B

Duplicate values are retained once.

Conflicting values are preserved.

---

## Scalar observations

Values that may appear scalar at the tool level are represented as
sets in the merged canonical metadata.

Example:

    HTTPX → status 200
    Other source → status 403

becomes:

    status_codes = {200, 403}

Neither observation is silently discarded.

---

## Collections

The following fields use set semantics:

- status_codes
- content_types
- response_sizes
- technologies
- redirect_targets

---

## Missing values

Missing values do not overwrite known values.

For example:

    Existing:
        status = 200

    New observation:
        status = unknown

The resulting state remains:

    status_codes = {200}

Unknown is represented by an empty collection rather than a fabricated
default.

---

## Duplicate values

Duplicate observations are merged once.

Example:

    HTTPX → nginx
    Katana → nginx

becomes:

    technologies = {"nginx"}

---

## Conflicting values

Conflicting observations are preserved.

Example:

    HTTPX → nginx
    Future source → Apache

becomes:

    technologies = {"nginx", "Apache"}

No source is given priority during M7.

---

## Determinism

Metadata merging must be:

- deterministic
- commutative
- idempotent
- associative

The order of reconnaissance sources must not change the resulting
canonical metadata.

---

## Unknown vs empty

An empty metadata collection represents that no value has been observed.

It does not mean:

- zero
- false
- HTTP status 0
- empty technology
- empty content type

No artificial placeholder values are inserted.

---

## Scope

M7-F defines merge semantics only.

It does not implement:

- HTTPX enrichment
- technology detection
- parameter extraction
- source-specific priority
- field-level provenance
- historical metadata
