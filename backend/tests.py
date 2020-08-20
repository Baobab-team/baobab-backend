from unittest import TestCase


class BasicTest(TestCase):

    def test_basic(self):
        self.assertEqual(10, 2 * 5)
