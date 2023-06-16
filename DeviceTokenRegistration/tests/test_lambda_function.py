import unittest
from unittest.mock import MagicMock

from tests import test_variables

class TestLambdaFunction(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(True, True)
        
if __name__ == '__main__':
    unittest.main()
