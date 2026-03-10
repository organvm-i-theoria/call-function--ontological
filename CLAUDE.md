# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository implements the **FUNCTIONcalled()** naming and metadata convention — a system for self-documenting file names and metadata sidecars. The core principle is that names should be **autological** (self-descriptive), containing their purpose, role, and context without requiring external lookup.

## Naming Convention

**Repository names:** Use `call-{name}--{descriptor}` format
- Single hyphen (`-`) separates words within a segment
- Double hyphen (`--`) separates the function name from its descriptor

**File names:** Pattern `{Layer}.{Role}.{Domain}.{Extension}`
- Versions must follow semver format (e.g., `1.0.0`, `2.1.3-beta.1`)

## Commands

```bash
# Install dependencies
make install-deps          # Installs jsonschema + semgrep

# Validate metadata files
make validate              # Validates *.meta.json against the schema

# Validate file naming conventions
make validate-naming       # Checks files follow {Layer}.{Role}.{Domain}.{ext}

# Run semgrep rules
make semgrep               # Validates header comments structure

# Run ALL validators
make validate-all          # Runs validate + validate-naming + semgrep

# Build the registry
make registry              # Scans for .meta.json files, outputs registry/registry.json

# Install pre-commit hook
make hook-install          # Runs all validators on git commit
```

To validate specific files directly:
```bash
python tools/validate_meta.py path/to/file.meta.json
python tools/validate_naming.py path/to/file.ext
```

## Architecture

### Layer System

Files follow the naming pattern `{Layer}.{Role}.{Domain}.{Extension}`. The four canonical layers are:

| Layer | Alias | Purpose | Languages |
|-------|-------|---------|-----------|
| `core` | `bones` | Foundation, kernel, structure | C, C++, Rust, Go |
| `interface` | `skins` | Portals, surfaces, UI | HTML, CSS, JS, PHP |
| `logic` | `breath` | Scripts, intelligence, agents | Python, Lua, Ruby |
| `application` | `body` | Embodiment, apps, bridges | Swift, Obj-C, Java |

Each layer directory contains starter `template.*` files with header comments describing the role.

### Metadata Sidecar Pattern

Any file can have a companion metadata sidecar named `{filename}.meta.json`. The schema supports two profiles:

- **light**: Minimal required fields (`profile`, `name`, `identifier`, `version`)
- **full**: Extended fields including `schema:type`, `conformsTo`, `encodingFormat`, `dateCreated`, `dateModified`

Schema: `standards/FUNCTIONcalled_Metadata_Sidecar.v1.1.schema.json`

### Registry

The registry builder (`tools/registry-builder.py`) walks the repo, finds all `.meta.json` files, and generates `registry/registry.json` — a catalog of all tracked resources with paths and optional SHA256 hashes.

## Commit Message Format

```
[layer:role] action — scope
```

Example: `[breath:agent] improve inference — caching`

<!-- ORGANVM:AUTO:START -->
## System Context (auto-generated — do not edit)

**Organ:** ORGAN-I (Theory) | **Tier:** standard | **Status:** PUBLIC_PROCESS
**Org:** `organvm-i-theoria` | **Repo:** `call-function--ontological`

### Edges
- **Produces** → `unspecified`: theory

### Siblings in Theory
`recursive-engine--generative-entity`, `organon-noumenon--ontogenetic-morphe`, `auto-revision-epistemic-engine`, `narratological-algorithmic-lenses`, `sema-metra--alchemica-mundi`, `system-governance-framework`, `cognitive-archaelogy-tribunal`, `a-recursive-root`, `radix-recursiva-solve-coagula-redi`, `.github`, `nexus--babel-alexandria-`, `reverse-engine-recursive-run`, `4-ivi374-F0Rivi4`, `cog-init-1-0-`, `collective-persona-operations` ... and 4 more

### Governance
- Foundational theory layer. No upstream dependencies.

*Last synced: 2026-03-08T20:11:34Z*

## Session Review Protocol

At the end of each session that produces or modifies files:
1. Run `organvm session review --latest` to get a session summary
2. Check for unimplemented plans: `organvm session plans --project .`
3. Export significant sessions: `organvm session export <id> --slug <slug>`
4. Run `organvm prompts distill --dry-run` to detect uncovered operational patterns

Transcripts are on-demand (never committed):
- `organvm session transcript <id>` — conversation summary
- `organvm session transcript <id> --unabridged` — full audit trail
- `organvm session prompts <id>` — human prompts only


## Active Directives

| Scope | Phase | Name | Description |
|-------|-------|------|-------------|
| system | any | prompting-standards | Prompting Standards |
| system | any | research-standards-bibliography | APPENDIX: Research Standards Bibliography |
| system | any | research-standards | METADOC: Architectural Typology & Research Standards |
| system | any | sop-ecosystem | METADOC: SOP Ecosystem — Taxonomy, Inventory & Coverage |
| system | any | autopoietic-systems-diagnostics | SOP: Autopoietic Systems Diagnostics (The Mirror of Eternity) |
| system | any | cicd-resilience-and-recovery | SOP: CI/CD Pipeline Resilience & Recovery |
| system | any | cross-agent-handoff | SOP: Cross-Agent Session Handoff |
| system | any | document-audit-feature-extraction | SOP: Document Audit & Feature Extraction |
| system | any | essay-publishing-and-distribution | SOP: Essay Publishing & Distribution |
| system | any | market-gap-analysis | SOP: Full-Breath Market-Gap Analysis & Defensive Parrying |
| system | any | pitch-deck-rollout | SOP: Pitch Deck Generation & Rollout |
| system | any | promotion-and-state-transitions | SOP: Promotion & State Transitions |
| system | any | repo-onboarding-and-habitat-creation | SOP: Repo Onboarding & Habitat Creation |
| system | any | research-to-implementation-pipeline | SOP: Research-to-Implementation Pipeline (The Gold Path) |
| system | any | security-and-accessibility-audit | SOP: Security & Accessibility Audit |
| system | any | session-self-critique | session-self-critique |
| system | any | source-evaluation-and-bibliography | SOP: Source Evaluation & Annotated Bibliography (The Refinery) |
| system | any | stranger-test-protocol | SOP: Stranger Test Protocol |
| system | any | strategic-foresight-and-futures | SOP: Strategic Foresight & Futures (The Telescope) |
| system | any | typological-hermeneutic-analysis | SOP: Typological & Hermeneutic Analysis (The Archaeology) |
| unknown | any | gpt-to-os | SOP_GPT_TO_OS.md |
| unknown | any | index | SOP_INDEX.md |
| unknown | any | obsidian-sync | SOP_OBSIDIAN_SYNC.md |

Linked skills: evaluation-to-growth


**Prompting (Anthropic)**: context 200K tokens, format: XML tags, thinking: extended thinking (budget_tokens)

<!-- ORGANVM:AUTO:END -->


## ⚡ Conductor OS Integration
This repository is a managed component of the ORGANVM meta-workspace.
- **Orchestration:** Use `conductor patch` for system status and work queue.
- **Lifecycle:** Follow the `FRAME -> SHAPE -> BUILD -> PROVE` workflow.
- **Governance:** Promotions are managed via `conductor wip promote`.
- **Intelligence:** Conductor MCP tools are available for routing and mission synthesis.
