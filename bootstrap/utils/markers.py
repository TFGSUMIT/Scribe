# ASCII-only status markers for CLI output. The Unicode symbols we used
# before (⏭ ➕ 🔄 ➖) look nicer but render as mojibake on a Windows console
# unless it's explicitly switched to UTF-8 (`chcp 65001`) — these render
# correctly everywhere, with no terminal configuration required.
CREATED = "+"
UPDATED = "~"
SKIPPED = "-"
DELETED = "x"
