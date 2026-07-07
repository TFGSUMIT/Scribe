# Overview

This is the canonical reference for Scribe. When in doubt about scope, architecture, or roadmap, this document wins — other docs (`PRODUCT.md`, `VISION.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `BACKLOG.md`) go deeper on a single dimension, but this page is where they must all agree.

See also: [PRODUCT.md](PRODUCT.md) · [VISION.md](VISION.md) · [ARCHITECTURE.md](ARCHITECTURE.md) · [ROADMAP.md](ROADMAP.md) · [BACKLOG.md](BACKLOG.md) · [ADR 006 — Clean and Hexagonal Architecture](adr/006%20-%20clean%20and%20hexagonal%20architecture.md)

---

## What Scribe Is

Scribe is a platform for capturing, transcribing and organizing tabletop RPG sessions — online or in person.

It listens to a session, transcribes it, identifies who is speaking, and builds a structured, queryable memory of the campaign: NPCs, locations, events, items, quests, combats and timelines. That memory can later be searched with AI and reused to generate context for future sessions.

Discord is **one possible source of audio, not the platform**. The application core must work identically whether the audio comes from a Discord voice channel, a local microphone, an uploaded recording, or a live stream from another service.

## Goals

The system must be able to:

- Capture audio
- Identify participants
- Manage sessions
- Transcribe conversations in real time
- Persist transcripts
- Produce automatic summaries
- Build campaign history
- Answer questions about past campaigns using AI
- Produce context for future sessions
- Organize NPCs
- Organize locations
- Organize events
- Organize items
- Organize quests
- Organize combats
- Organize timelines

## Non-Goals

See [PRODUCT.md](PRODUCT.md#non-goals) — Scribe is not a virtual tabletop, dice bot, music bot, moderation bot, or character sheet manager.

---

## Architecture: Clean + Hexagonal

Formalized in [ADR 006](adr/006%20-%20clean%20and%20hexagonal%20architecture.md). Summary:

The **Core** never depends on Discord, a GUI, a specific database, a specific external API, or a specific AI model. It depends only on interfaces (ports). Everything concrete — Discord, a database engine, an AI provider, a UI — is an **Adapter** that implements those interfaces from the outside in.

```
Core
├── Domain        — entities and business rules (Session, Character, NPC, Quest, ...)
├── Application   — use cases orchestrating the domain
├── Interfaces    — ports: contracts the adapters must implement
├── Services      — domain services that don't belong to a single entity
├── Events        — the internal event catalog (see below)
└── Models        — shared data structures

Infrastructure (adapters — implement Core interfaces)
├── Discord Adapter
├── Audio Capture
├── Speech-to-Text
├── AI Providers
├── Database
└── File Storage

Presentation (depends on Core through interfaces, never the reverse)
├── Desktop App
├── Web Dashboard
└── Mobile App (future)
```

The dependency rule is one-directional: **Infrastructure → Core** and **Presentation → Core**, never the other way around.

## Input Sources

Every input source is an adapter that translates its own protocol into the same internal domain events. Today: **Discord** (voice channels). Planned, without touching Core: local microphone, a Desktop app, recorded audio files (WAV/MP3), generic real-time streaming, LiveKit, Jitsi, Zoom, Google Meet, and others.

A source is "done" when it can raise `SessionStarted`, `ParticipantJoined`, `SpeakerStarted`, and the other events below — the rest of the system does not know or care where they came from.

## AI Capabilities

AI is not limited to transcription. It is also responsible for:

- Generating session summaries
- Identifying player characters
- Identifying NPCs
- Identifying locations
- Identifying items
- Identifying events
- Identifying quests
- Identifying relationships between characters
- Answering questions about past campaigns
- Building long-term campaign memory
- Producing context for upcoming sessions

The AI provider must be swappable behind a Core interface. Candidates: OpenAI (initial), Gemini, Claude, Ollama, LM Studio.

## Persistence

The database stores: sessions, participants, characters, transcripts, events, summaries, embeddings, metadata, and files.

SQLite initially; PostgreSQL as the project grows (see [ADR 001](adr/001%20-%20programming%20language.md) for the language choice driving this stack).

## Event Catalog

Scribe favors event-driven architecture wherever it fits. All input sources emit the same events; Core logic reacts to events, not to a specific adapter. Known events (extend as new capabilities are added):

`SessionStarted` · `ParticipantJoined` · `ParticipantLeft` · `SpeakerStarted` · `SpeakerStopped` · `TranscriptReceived` · `SummaryGenerated` · `NPCDetected` · `QuestDetected` · `CombatStarted` · `CombatEnded`

## Quality Principles

SOLID · DRY · KISS · YAGNI · DDD where it earns its complexity · high testability · low coupling · high cohesion.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13 |
| Database | SQLite now, PostgreSQL later |
| Desktop UI | Tauri or Electron |
| Discord adapter | discord.py |
| Speech-to-Text | Whisper |
| AI | OpenAI initially, provider-agnostic by design |

## Relationship to Discord

[ADR 003](adr/003%20-%20discord.md) decided Discord ships first — that sequencing still stands. What changes under [ADR 006](adr/006%20-%20clean%20and%20hexagonal%20architecture.md) is that "Discord first" no longer means "Discord hardcoded into Core": it must be built as one adapter among others, so the sources listed above can be added later without rewriting the core.

## Roadmap

See [ROADMAP.md](ROADMAP.md) and [BACKLOG.md](BACKLOG.md). Both predate this document and are scoped to a Discord-only bot — expect them to be revised into source-agnostic phases as the GitHub backlog (milestones, board, issues) is generated from this overview.
