# AGENTS.md

## Purpose of this repository

This repository is the **generic taxonomy resolution engine** for microbiome curation workflows.

Its scope is to implement and stabilize the reusable core needed to:

- build a local NCBI taxonomy reference database from the official taxdump
- resolve organism names against that taxonomy
- normalize messy user-entered taxon strings
- recover ranked lineage upward
- support deterministic matching and supervised fuzzy candidate suggestion
- persist reviewed decisions / mapping memory
- expose a stable local contract usable from CLI, scripts, and later Django integration

This repository is **not** the final project website/application repository.

The plan is:

1. build the generic taxonomy resolver here
2. build enough of the Excel-specific adapter and Django integration pattern to prove the workflow
3. then move the project-specific application work into the **MINdb** repository, where the actual domain application will continue

So this repo is the **core engine / library repo**, not the final end-user product repo.

---

## Scope boundaries

### In scope

This repository may contain:

- NCBI taxdump ingestion/build scripts
- local SQLite taxonomy reference DB builder
- taxonomy lookup/query layer
- lineage derivation logic
- normalization utilities
- deterministic resolver
- fuzzy/similarity suggestion logic
- status/policy definitions
- decision cache / reviewed mapping memory
- CLI utilities
- structured JSON-like resolver contracts
- tests for all of the above
- lightweight examples or adapters to validate integration with:
  - workbook parsing
  - Django service usage

### Limited / transitional scope

This repository may temporarily include:

- a **minimal Excel adapter prototype**
- a **minimal Django integration prototype**
- example review-queue logic
- proof-of-concept import/review flow

These are included only to validate that the generic resolver is usable in the real workflow.

### Out of scope

This repository should **not** become the long-term home for:

- the full MINdb website
- production Django app business logic
- MINdb-specific models and workflows beyond what is necessary to prove integration
- domain-specific website UI beyond small prototypes
- general paper curation logic unrelated to taxonomy resolution
- the final full Excel import system for MINdb
- unrelated microbiome database features

That work should move to the **MINdb** repository once the reusable core here is ready.

---

## Design principles

### 1. Generic first
The resolver must remain a reusable, generic taxonomy-resolution package.

It must **not** be tightly coupled to:
- one workbook schema
- one Django project
- one database schema for findings
- one UI

### 2. Local-first and reproducible
The system should work fully locally without depending on live NCBI API calls for core resolution.

Use:
- official NCBI taxdump
- local SQLite reference DB
- deterministic build steps
- versioned taxonomy builds when possible

### 3. Stable internal contract
Even when used locally through Python imports, the resolver should expose a stable structured contract as if it were an API.

Prefer:
- dataclasses / Pydantic models / typed dict-style structures
- JSON-serializable results
- fixed status enums
- explicit warnings and review states

### 4. Deterministic before fuzzy
Resolution order must be:

1. exact scientific name
2. exact synonym
3. normalized exact
4. only then fuzzy/similarity suggestion

Fuzzy matching is a **fallback suggestion mechanism**, not an authority.

### 5. Human review is a first-class feature
The system must support:
- confirm
- reject
- choose candidate
- manual review

The resolver should produce review-ready outputs, not just raw match scores.

### 6. Separate canonical identity from observed names
Do not conflate:
- canonical taxon identity
with
- the string written by a curator in a paper extraction sheet

A single canonical organism may have multiple observed name variants.

### 7. Keep interfaces thin
CLI, adapters, and Django integration should be thin layers over the core resolver package.

Do not duplicate resolver logic across entrypoints.

---

## Repository stages

### Stage 1 — core resolver foundation
Focus on:
- taxonomy DB builder
- schema
- local lookup
- normalization
- lineage
- deterministic resolution

### Stage 2 — supervised candidate suggestion
Add:
- fuzzy candidate generation
- ambiguity classification
- vague-label handling
- review-ready outputs

### Stage 3 — decision memory
Add:
- reviewed mapping cache
- reuse rules
- taxonomy-build-aware persistence

### Stage 4 — integration proof
Add only enough to validate:
- workbook parsing assumptions
- resolution queue generation
- minimal Django service integration
- minimal review workflow shape

### Stage 5 — handoff to MINdb repo
After the generic engine and integration shape are stable:
- move application-specific Excel workflow forward in MINdb
- move Django models/UI/business logic there
- keep this repository focused on the reusable resolver core

---

## Expected architecture

Recommended high-level layout:

```text
taxonomy_resolver/
  __init__.py
  db.py
  normalize.py
  lineage.py
  exact.py
  fuzzy.py
  policy.py
  cache.py
  service.py
  schemas.py

taxonomy_tools/
  build_ncbi_taxonomy.py
  resolve_name_cli.py
  resolve_batch_cli.py
  apply_decisions_cli.py

integration_prototypes/
  excel_adapter/
  django_example/

tests/
