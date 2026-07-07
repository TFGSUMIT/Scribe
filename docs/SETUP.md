# Development Setup

## Requirements

- Git
- Python 3.13+
- VS Code
- uv

## Clone

```bash
git clone https://github.com/JaimeAraujo18/Scribe.git
```

## Install dependencies

```bash
uv sync
```

## Run

```bash
uv run python src/main.py
```

## GitHub Project Bootstrap

The `bootstrap/` tool syncs labels, milestones, the Projects v2 board and backlog issues from `bootstrap/resources/` onto the GitHub repository. See [bootstrap/README.md](../bootstrap/README.md) for details.

It needs a `.env` (copy `.env.example`) with a Personal Access Token scoped to `repo` and `project`:

```bash
python -m bootstrap.bootstrap init
```
