# ADR-006 — Adopt Clean Architecture and Hexagonal Architecture

**Status:** Accepted

**Date:** 2026-07-06

**Supersedes:** [ADR-004 — Adopt a Modular Architecture](004%20-%20modular%20architecture.md)

## Context

ADR-004 established a modular architecture, separating Scribe into dedicated packages by domain: bot, audio, transcription, ai, campaign, exporters, database.

The product scope has since grown beyond a Discord bot. Scribe must capture audio from multiple, unrelated sources — Discord, a local microphone, a Desktop app, a Mobile app, recorded audio files, LiveKit, Jitsi, Zoom, Google Meet, and others — all sharing exactly the same application core. It must also support swapping AI providers (OpenAI, Gemini, Claude, Ollama, LM Studio) without touching the rest of the system.

Grouping code by domain package, as ADR-004 prescribes, organizes *where* code lives but says nothing about *which direction dependencies point*. Nothing in a plain modular split stops the campaign or AI package from importing `discord.py` directly, or a specific AI SDK, or a specific database driver. As soon as that happens, adding a new audio source or swapping an AI provider requires invasive changes to Core logic — exactly what the multi-source, multi-provider goal rules out.

## Decision

Scribe adopts **Clean Architecture** combined with **Hexagonal Architecture (Ports & Adapters)**.

- **Core** (`Domain`, `Application`, `Interfaces`, `Services`, `Events`, `Models`) never depends on Discord, a GUI, a specific database, a specific external API, or a specific AI model. It depends only on interfaces it defines itself (ports).
- **Infrastructure** implements those interfaces as **Adapters**: Discord Adapter, Audio Capture, Speech-to-Text, AI Providers, Database, File Storage. Adapters depend on Core, never the reverse.
- **Presentation** (Desktop App, Web Dashboard, future Mobile App) also depends inward on Core through interfaces.
- Every input source adapter translates its own protocol into the same internal domain events (`SessionStarted`, `TranscriptReceived`, `NPCDetected`, ...), so Core logic is entirely source-agnostic.

Full layout and event catalog: [docs/OVERVIEW.md](../OVERVIEW.md).

### Relationship to ADR-003 (Discord as initial platform)

[ADR-003](003%20-%20discord.md) is not reversed by this decision. Discord still ships first — that sequencing choice stands. What changes is the "simpler architecture" consequence ADR-003 listed as a benefit of a Discord-only scope: under this ADR, Discord must be built as one adapter behind Core ports from day one, not hardcoded into Core. Shipping Discord first is a scheduling decision; it is no longer an architectural coupling.

### Relationship to ADR-004

ADR-004's instinct — separate responsibilities so each domain evolves independently — is preserved, but plain package-by-domain grouping doesn't enforce a dependency direction. This ADR re-expresses that goal through Clean/Hexagonal layering, which does enforce it (Core cannot import Infrastructure; the reverse is required). ADR-004 is superseded by this ADR.

## Alternatives Considered

### Keep the plain modular architecture (ADR-004 as is)

Pros

- Simpler mental model
- No interfaces/ports boilerplate

Cons

- Nothing stops Core logic from importing `discord.py` or a specific AI SDK directly
- Adding a new audio source or swapping an AI provider later requires invasive refactors
- Directly contradicts the goal of decoupled input sources

### Full microservices per adapter

Pros

- Maximum isolation
- Independently deployable adapters

Cons

- Massive operational overhead for the project's current stage (single developer, single process)
- Premature under YAGNI

## Consequences

Positive

- Core is testable in isolation, using fake adapters in place of Discord, the database, or an AI provider
- New audio sources or AI providers can be added without touching Core
- Aligns with SOLID's Dependency Inversion Principle
- Cleanly supports event-driven design: events are defined in Core, adapters translate to and from them

Negative

- More upfront ceremony than a plain modular split: explicit interfaces/ports and dependency wiring between layers
- Steeper initial learning curve, particularly while learning Python — mitigated by introducing the layers incrementally and explaining each decision as it's implemented
