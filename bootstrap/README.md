# Bootstrap

A small CLI that sets up the Scribe repository on GitHub — labels, milestones, the Projects v2 board, and backlog issues — from the desired state declared in `bootstrap/resources/`, instead of clicking through the GitHub UI by hand.

It follows one pattern everywhere: **reconcile**. Each service loads what's *desired* from a JSON file, loads what *exists* on GitHub, and does the minimum work to make them match (create what's missing, update what drifted, skip what's already correct). `LabelService` is the reference implementation for this pattern — read it first if you want to understand the shape before diving into the others.

## Running it

```bash
python -m bootstrap.bootstrap init
```

Requires a `.env` at the repo root (copy `.env.example`) with:

- `GITHUB_TOKEN` — a Personal Access Token with the **`repo`** and **`project`** scopes. `repo` covers labels/milestones/issues; `project` covers the Projects v2 board. Without `project`, everything up to the board will work and then fail.
- `GITHUB_OWNER`, `GITHUB_REPO` — the repository to bootstrap.
- `PROJECT_NAME` — optional; defaults to `"{repo} Project Board"`.

Running `init` twice is safe and expected — the second run should report everything as skipped, since nothing changed.

## What each step does

1. **Labels** (`services/label_service.py`) — syncs `resources/labels.json`. Also deletes labels on GitHub that aren't in the file.
2. **Milestones** (`services/milestone_service.py`) — syncs `resources/milestones.json`. Also deletes orphan milestones. Returns `{title: number}` for the issues step.
3. **Project board** (`services/project_service.py`) — creates/reuses the Projects v2 board from `resources/project.json` (name, description, custom fields), and links it to the repo. Returns the project id plus field/option ids for the issues step.
4. **Issues** (`services/issue_service.py`) — creates every issue declared across `resources/issues/*.json` (skipping ones that already exist by title), then adds each one to the board with its Epic/Sprint/Story Points fields filled in.

Issues are **never deleted or auto-closed** by this tool — closing a real issue is a product decision, not something a sync script should do silently.

## Known limitations

- **Views are not automatable.** `resources/views.json` documents the intended Board/Table/Roadmap views, but the GitHub GraphQL API has no mutation for creating or arranging Projects v2 views — they have to be set up by hand once, in the project's UI.
- **Single-select field options are only ever added, never replaced.** If a field like `Epic` already exists on the board but is missing an option from `project.json`, the tool logs a warning instead of fixing it automatically — replacing a single-select field's options via the API reissues every option with a new id, which would silently wipe the value already set on existing board items. Add the missing option by hand in the project settings when this happens.
- Backlog issues live under `resources/issues/`, split into one file per epic (`01-foundation.json`, `02-discord.json`, ...) so the backlog doesn't live in one giant file. All `*.json` files in that folder are loaded and concatenated — add a new file to introduce a new batch of issues.

## Logs

Every GitHub request (REST and GraphQL) is logged to `bootstrap/logs/bootstrap.log` (gitignored) in addition to the console, so a run can be inspected after the fact — useful when a sync fails partway through.
