# ADR-001 — Adopt Python as the Primary Programming Language

**Status:** Accepted

**Date:** 2026-07-04

## Context

Scribe is an AI-powered Discord companion focused on real-time speech recognition, natural language processing and campaign management.

The project requires mature libraries for:

- Discord integration
- Audio processing
- Speech-to-Text
- Machine Learning
- Artificial Intelligence

The language should maximize development speed while providing access to the largest ecosystem in these areas.

## Decision

Python will be used as the primary programming language for the entire project.

## Alternatives Considered

### C\#

Pros

- Strong typing
- Excellent tooling
- High performance

Cons

- Smaller AI ecosystem
- Fewer speech recognition libraries
- More integration work required

---

### Node.js

Pros

- Great Discord ecosystem
- Large community

Cons

- Weaker AI ecosystem
- Most ML libraries require Python services

## Consequences

Positive

- Access to the best AI ecosystem available
- Excellent Speech-to-Text support
- Faster prototyping
- Large community

Negative

- Lower runtime performance compared to compiled languages
- Learning curve for contributors unfamiliar with Python
