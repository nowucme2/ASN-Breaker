import logging
from pathlib import Path


def setup_logger(project_path):

    log_dir = Path(project_path) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "scan.log"

    logger = logging.getLogger("asn_breaker")

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        handler = logging.FileHandler(log_file)

        formatter = logging.Formatter(
            "%(asctime)s  %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
