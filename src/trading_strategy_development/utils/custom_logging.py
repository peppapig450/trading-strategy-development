"""Centralized logging configuration for the trading strategy development package."""

from __future__ import annotations

import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final, TypedDict


def get_project_root() -> Path:
    """Determine the project root directory by finding the parent of the 'src' directory.

    Returns:
        Path object pointing to the project root.
    """
    current_file = Path(__file__).resolve()
    for parent in current_file.parents:
        if parent.name == "src":
            return parent.parent
    raise RuntimeError("Could not find project root (expected to find 'src' directory).")


DEFAULT_LOG_DIR: Final[Path] = get_project_root() / "logs"

if TYPE_CHECKING:

    class LoggingConfig(TypedDict):
        log_dir: Path
        log_file: Path
        log_level: int
        console_output: bool


def setup_logging(
    log_dir: str | Path = DEFAULT_LOG_DIR,
    log_level: int = logging.INFO,
    log_format: str | None = None,
    capture_warnings: bool = True,
    console_output: bool = True,
    file_prefix: str = "trading_log",
) -> LoggingConfig:
    """Set up logging configuration for the entire application with timed rotation.

    Args:
        log_dir: Directory to store log files (will be resolved relative to project root).
        log_level: Logging level (default: INFO).
        log_format: Custom log format string (if None, uses default format).
        capture_warnings: Whether to capture warnings via logging.
        console_output: Whether to output logs to console in addition to file.
        file_prefix: Prefix for log filename (e.g., 'trading_log' for 'trading_log.log').

    Returns:
        Dictionary with logging configuration details.
    """
    if isinstance(log_dir, str):
        log_dir = Path(log_dir)

    project_root = get_project_root()

    # Normalize log_dir to be relative to the project root
    if log_dir.is_absolute():
        # If the path is absolute, use only the last part of the path (e.g., /var/logs -> logs)
        log_dir = project_root / log_dir.name
    else:
        # If the path is relative, resolve it relative to the project root
        log_dir = (project_root / log_dir).resolve()
        # Ensure it's still under the project root (in case of '..' in the path)
        if not log_dir.is_relative_to(project_root):
            log_dir = project_root / log_dir.name

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except (OSError, PermissionError) as e:
        # If we can't create the log directory, fall back to a temp directory
        import tempfile

        log_dir = Path(tempfile.gettempdir()) / "trading_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        print(
            f"Warning: Could not create a log directory at {log_dir}. Using {log_dir} instead. Error: {e}",
            file=sys.stderr,
        )

    log_file = log_dir / f"{file_prefix}.log"

    log_format = log_format or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    try:
        file_handler = TimedRotatingFileHandler(
            filename=log_file, when="D", interval=1, backupCount=7, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        root_logger.addHandler(file_handler)
    except (OSError, PermissionError) as e:
        error_msg = f"Failed to set up file handler: {e!s}"
        print(error_msg, file=sys.stderr)

    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)
        root_logger.addHandler(console_handler)

    if capture_warnings:
        logging.captureWarnings(capture_warnings)

    root_logger.info("Logging initiated. Log file: %s", log_file)

    return {
        "log_dir": log_dir,
        "log_file": log_file,
        "log_level": log_level,
        "console_output": console_output,
    }


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name.

    Args:
        name: Name of the logger, typically the module name using __name__.

    Returns:
        Logger instance.
    """
    return logging.getLogger(name)
