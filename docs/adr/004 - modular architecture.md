# ADR-004 — Adopt a Modular Architecture

**Status:** Superseded by [ADR-006 — Clean and Hexagonal Architecture](006%20-%20clean%20and%20hexagonal%20architecture.md)

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

## Update

Superseded by [ADR-006](006%20-%20clean%20and%20hexagonal%20architecture.md), which re-expresses this same separation-of-concerns goal through Clean Architecture and Hexagonal Architecture — layering that also enforces the direction of dependencies, which a plain modular split did not.
