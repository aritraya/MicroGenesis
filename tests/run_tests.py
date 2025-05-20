"""Test runner for the project."""

import unittest

if __name__ == "__main__":
    # Discover and run all tests
    test_suite = unittest.defaultTestLoader.discover('tests')
    unittest.TextTestRunner().run(test_suite)
