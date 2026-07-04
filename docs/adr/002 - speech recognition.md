# ADR-002 — Prefer Local Speech Recognition

**Status:** Accepted

**Date:** 2026-07-04

## Context

Scribe continuously processes voice conversations that may contain personal information and private campaign content.

Sending all audio to cloud providers would introduce:

- Recurring costs
- Latency
- Privacy concerns
- Dependency on third-party services

## Decision

Speech recognition should run locally whenever technically feasible.

Cloud providers may be used as optional integrations, never as mandatory dependencies.

## Alternatives Considered

### Cloud Speech APIs

Examples:

- OpenAI
- Google Speech
- Azure Speech

Pros

- Excellent accuracy
- No local GPU required

Cons

- Cost per minute
- Internet dependency
- Privacy concerns

---

### Local Models

Examples:

- Faster Whisper
- whisper.cpp

Pros

- Offline
- Privacy
- Zero recurring cost
- Low latency

Cons

- Higher hardware requirements

## Consequences

Positive

- Better privacy
- Lower operating costs
- Offline capability

Negative

- Users need sufficient hardware
