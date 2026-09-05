import unittest

from handler import get


class ConditionalGetTests(unittest.TestCase):
    def test_matching_conditions_return_empty_304_with_validator(self):
        for header in ('"v2"', 'W/"v2"', '*', ' \t*\t ',
                       '"v1", "v2"', 'W/"v1", W/"v2"',
                       ' \t"v1" ,\tW/"v2" ', '"v2", "v3"',
                       '"other,tag", W/"v2"', ', "v2", ,'):
            with self.subTest(header=header):
                self.assertEqual(get(header), (304, {'ETag': '"v2"'}, b''))

    def test_nonmatching_conditions_preserve_representation(self):
        for header in (None, '', '"v1"', 'W/"v1"', '"v1", W/"v3"',
                       '"V2"', '"v20"', '"other,v2"', '"W/v2"'):
            with self.subTest(header=header):
                self.assertEqual(get(header),
                                 (200, {'ETag': '"v2"'}, b'current representation'))

    def test_malformed_conditions_do_not_match(self):
        for header in ('v2', 'w/"v2"', 'junk "v2"', '"v2"junk',
                       '"v2", junk', '*, "v2"', '"v2"\n'):
            with self.subTest(header=header):
                self.assertEqual(get(header),
                                 (200, {'ETag': '"v2"'}, b'current representation'))


if __name__ == '__main__':
    unittest.main()
