"""Test module for the example class."""

import unittest
from microgenesis.example import Example

class TestExample(unittest.TestCase):
    """Test cases for the Example class."""
    
    def test_greet(self):
        """Test the greet method."""
        example = Example(name="Test")
        self.assertEqual(example.greet(), "Hello from Test!")
        
    def test_default_name(self):
        """Test the default name."""
        example = Example()
        self.assertEqual(example.greet(), "Hello from MicroGenesis!")
        
if __name__ == "__main__":
    unittest.main()
