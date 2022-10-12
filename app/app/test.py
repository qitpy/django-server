'''
sample tests
'''

from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """Tests Calc module"""

    def test_add_numbers(self):
        """Test add numbers"""
        res = calc.add(5, 6)
        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        res = calc.subtract(11, 2)
        self.assertEqual(res, 9)
