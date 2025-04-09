"""
Tests for the custom logging utility module.
"""

import logging
import os
import tempfile
from pathlib import Path
from unittest.mock import patch
import pytest
from trading_strategy_development.utils.custom_logging import setup_logging, get_logger, get_project_root


def test_get_project_root() -> None:
    """Test that the project root is correctly identified."""
    root = get_project_root()
    assert root.exists()
    assert (root / "src").exists(), "Project root should contain a 'src' directory"


def test_setup_logging() -> None:
    """Test that the logging setup works properly."""
    # Use a temporary directory for log files
    with tempfile.TemporaryDirectory() as temp_dir:
        log_config = setup_logging(
            log_dir=temp_dir,
            log_level=logging.DEBUG,
            console_output=False,
        )
        
        # Check that the log file was created
        log_file = Path(log_config["log_file"])
        assert log_file.exists()
        
        # Get a logger and log a test message
        logger = get_logger("test_logger")
        test_message = "This is a test log message"
        logger.info(test_message)
        
        # Check that the message was written to the log file
        with open(log_file, "r") as f:
            log_content = f.read()
        
        assert "test_logger" in log_content
        assert test_message in log_content


def test_setup_logging_with_permission_error() -> None:
    """Test that logging setup handles permission errors gracefully."""
    # Mock mkdir to raise a permission error
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        mock_mkdir.side_effect = PermissionError("Permission denied")
        
        # Since we can't write to the log directory, it should fall back to a temp directory
        log_config = setup_logging(
            log_dir="logs",
            log_level=logging.INFO,
            console_output=False,
        )
        
        # Check that a fallback directory was used
        log_dir = Path(log_config["log_dir"])
        assert log_dir.name == "trading_logs"
        assert "temp" in str(log_dir) or "tmp" in str(log_dir)


def test_get_logger() -> None:
    """Test that the get_logger function returns the correct logger."""
    logger_name = "test.module.name"
    logger = get_logger(logger_name)
    
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name