import unittest

test_modules = [
    'lightdataparser.tests.test_cases',
    'lightdataparser.tests.test_types',
    'lightdataparser.tests.test_extract',
    'lightdataparser.tests.test_parse',
    'lightdataparser.tests.test_dump',
]

suite = unittest.TestSuite()

for t in test_modules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))


def test_all():
    return suite


def manual_test_all():
    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    manual_test_all()
