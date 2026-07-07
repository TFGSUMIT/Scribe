import sys

from bootstrap.commands.init import initialize


def _ensure_utf8_stdio():
    # Windows terminals often default stdout/stderr to the system codepage
    # (e.g. cp1252), which can't encode the ✓/➕/⏭ symbols the services print.
    # Reconfiguring to UTF-8 keeps that output readable everywhere.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def main():
    _ensure_utf8_stdio()

    if len(sys.argv) < 2:
        print("Usage:")
        print("python bootstrap.py init")

        return

    command = sys.argv[1]

    if command == "init":
        initialize()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()