import unittest

from dbdeps import buildGraph

class DbDepsTest(unittest.TestCase):
    def test_deps(self):
        buildGraph()
