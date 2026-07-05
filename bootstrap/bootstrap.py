import sys

from bootstrap.commands.init import initialize


def main():
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