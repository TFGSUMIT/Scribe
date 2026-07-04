# Architecture

The architecture follows a modular design.

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
