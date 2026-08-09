# WebRViz

```text
██╗    ██╗███████╗██████╗ ██████╗ ██╗   ██╗██╗███████╗
██║    ██║██╔════╝██╔══██╗██╔══██╗██║   ██║██║╚══███╔╝
██║ █╗ ██║█████╗  ██████╔╝██████╔╝██║   ██║██║  ███╔╝
██║███╗██║██╔══╝  ██╔══██╗██╔══██╗╚██╗ ██╔╝██║ ███╔╝
╚███╔███╔╝███████╗██████╔╝██████╔╝ ╚████╔╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═════╝   ╚═══╝  ╚═╝╚══════╝

              Web Application Attack Surface Visualizer
```

> **WebRViz** turns reconnaissance output into a structured, readable web application attack-surface map.

Instead of manually reading large lists of URLs, WebRViz organizes discovered hosts and endpoints into a hierarchical terminal tree.

---

## Overview

WebRViz is a command-line application mapper designed for security researchers, penetration testers, and bug bounty hunters.

It currently accepts reconnaissance output from:

* **httpx**
* **katana**

The collected URLs are normalized, deduplicated, grouped by hostname, organized into host hierarchies, and rendered as a terminal tree.

### Example

Input:

```text
https://example.com
https://example.com/login
https://example.com/register
https://api.example.com
https://api.example.com/v1/admin
https://api.example.com/v1/users
https://www.example.com/
```

Output:

```text
Application
└── example.com
    ├── /
    ├── login
    ├── register
    ├── api.example.com
    │   ├── /
    │   └── v1
    │       ├── admin
    │       └── users
    └── www.example.com
        └── /
```

This makes relationships between hosts and endpoint paths immediately visible.

---

## Features

### Host hierarchy

WebRViz automatically organizes related subdomains:

```text
example.com
└── api.example.com
    └── dev.api.example.com
```

### Endpoint path hierarchy

Nested paths are represented as a tree:

```text
api.example.com
└── v1
    ├── admin
    └── users
```

Instead of:

```text
/v1/admin
/v1/users
```

### Deduplication

Duplicate URLs are removed before building the application model.

### Deterministic ordering

Hosts, endpoints, and path nodes are sorted to produce stable output.

### Input validation

WebRViz detects:

* missing input files
* directories supplied as files
* missing input arguments

and provides readable CLI errors instead of unnecessary tracebacks.

### Malformed input handling

Invalid URLs and malformed input lines are ignored by the parsers rather than crashing the application.

### Multiple reconnaissance sources

HTTPX and Katana outputs can be supplied independently or together.

---

## Installation

### Requirements

* Python **3.11+**
* `pip`
* A virtual environment is recommended

### Clone the repository

```bash
git clone https://github.com/vikrammm24/WebRVizualizer.git
cd WebRViz
```

### Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### Install WebRViz

```bash
pip install -e .
```

Verify the installation:

```bash
webrviz --help
```

---

## Usage

WebRViz accepts HTTPX and Katana output files.

### HTTPX only

```bash
webrviz --httpx httpx.txt
```

### Katana only

```bash
webrviz --katana katana.txt
```

### HTTPX + Katana

```bash
webrviz \
    --httpx httpx.txt \
    --katana katana.txt
```

### Sample data

The repository includes sample input files:

```text
sample_data/
├── httpx.txt
└── katana.txt
```

Run:

```bash
webrviz \
    --httpx sample_data/httpx.txt \
    --katana sample_data/katana.txt
```

---

## CLI

Run:

```bash
webrviz --help
```

Current interface:

```text
usage: webrviz [-h] [--httpx HTTPX] [--katana KATANA]

WebRViz - Web Application Visualizer

options:
  -h, --help       show this help message and exit
  --httpx HTTPX    Path to httpx output file
  --katana KATANA  Path to katana output file

Examples:
  webrviz --httpx httpx.txt
  webrviz --katana katana.txt
  webrviz --httpx httpx.txt --katana katana.txt
```

---

## Input Format

WebRViz currently consumes URL-oriented output files.

### HTTPX

Example:

```text
https://example.com
https://api.example.com
https://www.example.com
```

### Katana

Example:

```text
https://example.com/login
https://example.com/register
https://api.example.com/v1/users
```

The parsers:

* strip surrounding whitespace
* skip blank lines
* reject invalid URLs
* ignore invalid ports
* return normalized `Endpoint` objects

---

## How WebRViz Works

The current Phase 1 pipeline is:

```text
             HTTPX ─────────┐
                            │
                            ▼
                         Parsers
                            │
             Katana ────────┘
                            │
                            ▼
                       Endpoints
                            │
                            ▼
                    ApplicationBuilder
                       /          \
                      /            \
             Host hierarchy     Endpoints
                    │                │
                    │             PathTree
                    │                │
                    └───────┬────────┘
                            ▼
                       TreeBuilder
                            │
                            ▼
                         Rich Tree
                            │
                            ▼
                           CLI
```

### Data model

The application is represented using:

```text
Application
    │
    └── Host
          ├── Endpoint
          ├── Endpoint
          └── Child Host
```

Endpoint paths are separately transformed into a visualization hierarchy:

```text
Endpoint
   │
   │ /api/v1/users
   ▼
PathTree
   │
   ▼
api
└── v1
    └── users
```

This keeps the discovered endpoint model separate from terminal visualization logic.

---

## Project Structure

```text
WebRViz/
│
├── webrviz/
│   ├── cli.py
│   │
│   ├── models/
│   │   ├── application.py
│   │   ├── endpoint.py
│   │   └── host.py
│   │
│   ├── parsers/
│   │   ├── httpx.py
│   │   └── katana.py
│   │
│   ├── services/
│   │   ├── builder.py
│   │   ├── domains.py
│   │   ├── normalizer.py
│   │   ├── path_tree.py
│   │   └── tree_builder.py
│   │
│   └── output/
│       └── printer.py
│
├── tests/
│   ├── test_application.py
│   ├── test_builder.py
│   ├── test_builder_domains.py
│   ├── test_cli.py
│   ├── test_domains.py
│   ├── test_domains_edge_cases.py
│   ├── test_domain_validation.py
│   ├── test_endpoint.py
│   ├── test_host.py
│   ├── test_malformed_input.py
│   ├── test_parsers.py
│   ├── test_path_tree.py
│   ├── test_tree_builder.py
│   ├── test_url.py
│   └── test_url_validation.py
│
├── sample_data/
│   ├── httpx.txt
│   └── katana.txt
│
├── README.md
├── LICENSE
└── pyproject.toml
```

---

## Development

Create and activate the development environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project in editable mode:

```bash
pip install -e .
```

Run the complete test suite:

```bash
pytest -v
```

Current Phase 1 regression baseline:

```text
145 passed
```

The test suite covers:

* application behavior
* host hierarchy
* domain handling
* URL validation
* endpoint equality and deduplication
* HTTPX parsing
* Katana parsing
* malformed input
* CLI behavior
* path hierarchy
* tree rendering

---

## Error Handling

WebRViz is designed to fail cleanly on common user errors.

### No input

```bash
webrviz
```

Produces an argparse error indicating that no input files were supplied.

### Missing file

```bash
webrviz --httpx missing.txt
```

Produces a readable error containing the provided and resolved paths.

### Directory supplied as a file

```bash
webrviz --httpx /tmp
```

Produces:

```text
HTTPX path is not a file.

Provided path : /tmp
Resolved path : /tmp

The supplied path points to a directory or another non-file object.
```

The command exits with status `1` without producing a Python traceback.

---

## Current Phase

WebRViz is currently in **Phase 1 — Stabilization & Hardening**.

The Phase 1 objective is to turn the working MVP into a reliable foundation for future development.

Current capabilities include:

* HTTPX ingestion
* Katana ingestion
* URL normalization
* endpoint deduplication
* hostname grouping
* subdomain hierarchy
* endpoint path hierarchy
* deterministic rendering
* CLI validation
* malformed input handling
* regression testing

Current regression status:

```text
145 passed
```

---

## Roadmap

Future phases can build on the Phase 1 foundation.

Potential areas include:

```text
Phase 2
├── richer endpoint metadata
├── HTTP status information
├── technologies
├── parameters
├── endpoint relationships
└── richer attack-surface visualization
```

The exact Phase 2 scope will be defined after Phase 1 stabilization is complete.

---

## Philosophy

WebRViz is built around a simple idea:

> **Reconnaissance produces data. WebRViz turns that data into structure.**

The goal is not to replace reconnaissance tools.

The goal is to make their output easier to understand.

---

## License

See [LICENSE](LICENSE).
