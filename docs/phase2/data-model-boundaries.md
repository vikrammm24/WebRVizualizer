# WebRViz Phase 2 — Data Model Boundaries

## Purpose

This document defines ownership boundaries between Application, Host,
and Endpoint.

The goal is to prevent enrichment metadata from becoming arbitrarily
attached to the wrong entity.

---

## Application

Application represents the complete discovered application structure.

### Owns

- Global host registry
- Host hierarchy
- Application-wide traversal
- Future application-level relationships

### Does not own

- Individual endpoint metadata
- HTTP response metadata
- Host IP addresses
- TLS information
- Endpoint parameters
- Rendering information

---

## Host

Host represents a network/application host identified by hostname.

### Owns

- Hostname
- IP addresses
- Network ports
- Server information
- Host-level metadata
- Child host hierarchy
- Endpoints belonging to the host

### Does not own

- Endpoint HTTP status
- Endpoint query parameters
- Endpoint-specific response information
- Terminal rendering information

---

## Endpoint

Endpoint represents a discovered URL endpoint.

### Owns

- Scheme
- Hostname reference
- Path
- Port as part of URL identity
- Query observation
- Original URL
- Canonical endpoint identity
- Future endpoint-level metadata

Potential future endpoint metadata:

- HTTP status
- Content type
- Response size
- Redirect information
- Parameters
- Endpoint-specific technologies
- Endpoint relationships

---

## Presentation

The data model must not depend on the renderer.

The following are presentation concerns:

- Rich Tree
- Rich Text
- terminal formatting
- colors
- symbols
- layout

The canonical model must remain usable by:

- Rich output
- JSON output
- Web UI
- Graph visualization
- future exporters

---

## Ownership hierarchy

Application
└── Host
    ├── Host metadata
    └── Endpoint
        └── Endpoint metadata

---

## Design rule

Metadata belongs to the smallest entity that can correctly own it.

If information describes the host generally, it belongs to Host.

If information describes a specific URL endpoint, it belongs to Endpoint.

If information describes the complete discovered application structure,
it belongs to Application.

## Observation and provenance

Reconnaissance input is treated as an observation before becoming part of
the canonical application state.

    HTTPX ──────┐
                │
    Katana ────┤
                │
    Future ─────┘
                │
                ▼
           Observation
                │
                ├── Endpoint
                ├── Source
                └── Raw value
                │
                ▼
       Canonical Endpoint Identity
                │
                ▼
        Canonical Application State
