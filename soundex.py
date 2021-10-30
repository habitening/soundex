"""Index a name using soundex phonetic algorithm."""

import unittest

LETTER_MAP = {
    'a': '0',
    'b': '1',
    'c': '2',
    'd': '3',
    'e': '0',
    'f': '1',
    'g': '2',
    'h': '0',
    'i': '0',
    'j': '2',
    'k': '2',
    'l': '4',
    'm': '5',
    'n': '5',
    'o': '0',
    'p': '1',
    'q': '2',
    'r': '6',
    's': '2',
    't': '3',
    'u': '0',
    'v': '1',
    'w': '0',
    'x': '2',
    'y': '0',
    'z': '2'
}
"""Dictionary mapping each letter to its number."""

def get_American_soundex(name):
    """Return string soundex code for name indexed using American soundex.

    Args:
        name: String name starting with a letter.
    Returns:
        String soundex code for name indexed using American soundex.
    """
    if not isinstance(name, str):
        raise TypeError(
            'name must be a non-empty string starting with a letter.')
    if len(name) <= 0:
        raise ValueError(
            'name must be a non-empty string starting with a letter.')
    letters = list(name.lower())
    last = letters[0]
    if last not in LETTER_MAP:
        raise ValueError(
            'name must be a non-empty string starting with a letter.')

    result = [last.upper()]
    for letter in letters[1:]:
        digit = LETTER_MAP[letter]
        if digit == LETTER_MAP[last]:
            # If two or more letters with the same number are adjacent,
            # then only retain the first letter
            continue
        if last in 'hw':
            if digit != result[-1]:
                result.append(digit)
        elif digit != '0':
            # Only include letters that are not aeiouyhw.
            # That is, drop aeiouyhw
            result.append(digit)
        last = letter

    # Append with zeroes until there are 3 numbers
    result.append('000')
    return ''.join(result)[:4]

def get_SQL_soundex(name):
    """Return string soundex code for name indexed using SQL soundex.

    Args:
        name: String name starting with a letter.
    Returns:
        String soundex code for name indexed using SQL soundex.
    """
    if not isinstance(name, str):
        raise TypeError(
            'name must be a non-empty string starting with a letter.')
    if len(name) <= 0:
        raise ValueError(
            'name must be a non-empty string starting with a letter.')
    letters = list(name.lower())
    saved = letters[0]
    if saved not in LETTER_MAP:
        raise ValueError(
            'name must be a non-empty string starting with a letter.')

    # Map all letters to their digits
    digits = [LETTER_MAP[letter] for letter in letters]
    # Replace all adjacent same digits with the first digit
    result = []
    last = digits[0]
    for digit in digits[1:]:
        if digit != last:
            result.append(digit)
        last = digit
    # Remove the zero digits
    result = [digit for digit in result if digit != '0']

    if LETTER_MAP[saved] == result[0]:
        # If the saved letter's digit is the same as the first digit,
        # then drop the digit and keep the letter.
        result[0] = saved.upper()
    else:
        result.insert(0, saved.upper())

    # Append with zeroes until there are 3 numbers
    result.append('000')
    return ''.join(result)[:4]


class _UnitTest(unittest.TestCase):
    def test_constants(self):
        """Test the module constants."""
        self.assertEqual(len(LETTER_MAP), 26)
        for letter in 'aeiouyhw':
            self.assertEqual(LETTER_MAP[letter], '0')
        for letter in 'bfpv':
            self.assertEqual(LETTER_MAP[letter], '1')
        for letter in 'cgjkqsxz':
            self.assertEqual(LETTER_MAP[letter], '2')
        for letter in 'dt':
            self.assertEqual(LETTER_MAP[letter], '3')
        for letter in 'l':
            self.assertEqual(LETTER_MAP[letter], '4')
        for letter in 'mn':
            self.assertEqual(LETTER_MAP[letter], '5')
        for letter in 'r':
            self.assertEqual(LETTER_MAP[letter], '6')

    def test_get_American_soundex(self):
        """Test the American soundex algorithm."""
        for value in [None, 42, []]:
            self.assertRaises(TypeError, get_American_soundex, value)
        for value in ['', '8oo', '*ab']:
            self.assertRaises(ValueError, get_American_soundex, value)
        for value, expected in [
            ('Ashcraft', 'A261'),
            ('Ashcroft', 'A261'),
            ('Deusen', 'D250'),
            ('Gutierrez', 'G362'),
            ('Honeyman', 'H555'),
            ('Jackson', 'J250'),
            ('Lee', 'L000'),
            ('Pfister', 'P236'),
            ('Rubin', 'R150'),
            ('Robert', 'R163'),
            ('Rupert', 'R163'),
            ('Tymczak', 'T522'),
            ('VanDeusen', 'V532'),
            ('Washington', 'W252')]:
            self.assertEqual(get_American_soundex(value), expected)
            self.assertEqual(get_American_soundex(value.lower()), expected)
            self.assertEqual(get_American_soundex(value.title()), expected)
            self.assertEqual(get_American_soundex(value.upper()), expected)

    def test_get_SQL_soundex(self):
        """Test the SQL soundex algorithm."""
        for value in [None, 42, []]:
            self.assertRaises(TypeError, get_SQL_soundex, value)
        for value in ['', '8oo', '*ab']:
            self.assertRaises(ValueError, get_SQL_soundex, value)
        for value, expected in [
            ('Honeyman', 'H555'),
            ('Robert', 'R163'),
            ('Rupert', 'R163'),
            ('Tymczak', 'T522')]:
            self.assertEqual(get_SQL_soundex(value), expected)
            self.assertEqual(get_SQL_soundex(value.lower()), expected)
            self.assertEqual(get_SQL_soundex(value.title()), expected)
            self.assertEqual(get_SQL_soundex(value.upper()), expected)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', nargs='?', default='',
                        help='name to index using the soundex algorithm')
    args = parser.parse_args()

    if len(args.name) > 0:
        print('American:', get_American_soundex(args.name))
        print('SQL:', get_SQL_soundex(args.name))
    else:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(_UnitTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
