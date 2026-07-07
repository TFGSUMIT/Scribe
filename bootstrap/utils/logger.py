import logging

from bootstrap.utils.paths import LOGS_DIR

LOG_FILE = LOGS_DIR / "bootstrap.log"


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger that writes to both the console and
    bootstrap/logs/bootstrap.log.

    Both get a timestamp — a short HH:MM:SS on the console so it stays
    readable, and a full date+time in the file so past runs can be told
    apart later.

    The two handlers also differ in verbosity, using standard log levels:
    the console only shows INFO (one short line per request), while the
    file also captures DEBUG (full request payloads, e.g. a GraphQL query
    and its variables) — useful when a run fails and you need to see
    exactly what was sent, without flooding the terminal on every run.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        # Already configured (e.g. called again for the same module) — avoid
        # attaching duplicate handlers, which would duplicate every log line.
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s %(message)s", datefmt="%H:%M:%S")
    )
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    logger.addHandler(file_handler)

    return logger
