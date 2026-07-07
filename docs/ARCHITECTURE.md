# Architecture

> Canonical reference: [docs/OVERVIEW.md](OVERVIEW.md) and [ADR 006](adr/006%20-%20clean%20and%20hexagonal%20architecture.md). This page illustrates one concrete pipeline (the Discord adapter); it does not define the layering itself.

The architecture follows Clean Architecture and Hexagonal Architecture (Ports & Adapters): a source-agnostic Core, with Discord, the database, AI providers and the UI plugged in as adapters. See [OVERVIEW.md](OVERVIEW.md#architecture-clean--hexagonal) for the full layer breakdown and event catalog.

The diagram below shows how audio flows end-to-end through the **Discord adapter** specifically — other adapters (local microphone, recorded files, streaming) feed the same Core through the same events, entering the pipeline further down instead of at the Discord Gateway step.

```plain
Discord
      │
      ▼
Discord Gateway
      │
      ▼
Voice Receiver
      │
      ▼
Audio Pipeline
      │
      ├── Voice Activity Detection
      ├── Audio Buffer
      ├── Speech Recognition
      │
      ▼
Session Service
      │
      ▼
AI Service
      │
      ▼
Campaign Database
      │
      ▼
Export Services
```

## Principles

- Loose Coupling
- High Cohesion
- Dependency Injection
- Testability
- Event Driven where appropriate
