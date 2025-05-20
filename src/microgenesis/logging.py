"""Logging configuration for MicroGenesis."""

import os
import logging
import logging.handlers
from pathlib import Path


def setup_logging(log_level="INFO", log_file=None):
    """Configure application logging.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (str, optional): Path to log file. If None, logs to console only.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Convert string level to logging level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger("microgenesis")
    logger.setLevel(numeric_level)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Clear existing handlers (in case setup_logging is called multiple times)
    logger.handlers = []
    
    # Always add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        try:
            # Ensure log directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir:
                Path(log_dir).mkdir(parents=True, exist_ok=True)
                
            # Create rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (IOError, PermissionError) as e:
            logger.error(f"Failed to create log file: {e}")
    
    return logger


def get_logger():
    """Get the application logger.
    
    Returns:
        logging.Logger: The application logger
    """
    logger = logging.getLogger("microgenesis")
    if not logger.handlers:
        # If logger hasn't been configured yet, use default settings
        return setup_logging()
    return logger
