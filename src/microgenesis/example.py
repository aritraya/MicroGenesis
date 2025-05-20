"""Example module with a sample class."""
from microgenesis.logging import get_logger

class Example:
    """Sample class to demonstrate project structure."""
    
    def __init__(self, name="MicroGenesis"):
        """Initialize with a name.
        
        Args:
            name (str): Name to use in greeting
        """
        self.name = name
        self.logger = get_logger()
        self.logger.debug(f"Created Example instance with name: {name}")
        
    def greet(self):
        """Return a greeting message.
        
        Returns:
            str: Formatted greeting message
        """
        message = f"Hello from {self.name}!"
        self.logger.info(f"Greeting generated: {message}")
        return message
        
    def set_name(self, name):
        """Update the name.
        
        Args:
            name (str): New name to use
            
        Raises:
            ValueError: If name is empty
        """
        if not name:
            self.logger.error("Attempted to set empty name")
            raise ValueError("Name cannot be empty")
            
        self.logger.debug(f"Changing name from {self.name} to {name}")
        self.name = name
