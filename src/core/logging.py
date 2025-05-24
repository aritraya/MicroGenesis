"""Logging configuration for MicroGenesis scaffolding tool."""

import os
import logging
import logging.handlers
import sys


class LoggingManager:
    """Manages logging configuration for the application."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Create a singleton instance of LoggingManager."""
        if cls._instance is None:
            cls._instance = super(LoggingManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logging manager if not already done."""
        if not LoggingManager._initialized:
            self.logger = logging.getLogger("microgenesis")
            self.setup_logging()
            LoggingManager._initialized = True
    
    def setup_logging(self, log_level="INFO", log_file=None):
        """Configure application logging.
        
        Args:
            log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file (str, optional): Path to log file. If None, logs to console only.
        """
        # Convert string level to logging level
        numeric_level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Set logger level
        self.logger.setLevel(numeric_level)
        
        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # Clear existing handlers
        self.logger.handlers = []
        
        # Add console handler with color formatting for different log levels
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
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
                self.logger.addHandler(file_handler)
            except (IOError, PermissionError) as e:
                self.logger.error(f"Failed to create log file: {e}")
    
    def get_logger(self):
        """Get the application logger.
        
        Returns:
            logging.Logger: The application logger
        """
        return self.logger


def get_logger():
    """Get the application logger.
    
    Returns:
        logging.Logger: The application logger
    """
    return LoggingManager().get_logger()
