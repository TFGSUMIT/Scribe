# ADR-004 — Adopt a Modular Architecture

**Status:** Accepted

**Date:** 2026-07-04

## Context

Scribe combines several independent domains:

- Discord communication
- Audio processing
- Speech recognition
- Artificial intelligence
- Campaign management
- Export services

Each domain should evolve independently.

## Decision

The project will follow a modular architecture, separating responsibilities into dedicated packages.

## Consequences

Positive

- Better maintainability
- Easier testing
- Independent evolution of modules

Negative

- Slightly more initial complexity
