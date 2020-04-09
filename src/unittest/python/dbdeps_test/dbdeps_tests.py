import unittest
import logging

from dbdeps import build_graph


logger = logging.getLogger()

class DbDepsTest(unittest.TestCase):
    def setUp(self):
        from dbdeps.outside import ds
        self.ds = ds

    def test_deps(self):
        g = build_graph(self.ds)
        import tempfile
        tmp = tempfile.mktemp()
        logger.info(g.render(directory=tmp))
#         g.view()


class AutomobileTest(unittest.TestCase):
    def setUp(self):
        from dbdeps.outside import datasource2
        self.ds = datasource2()

    def test_deps(self):
        g = build_graph(self.ds)
        import tempfile
        tmp = tempfile.mktemp()
        logger.info(g.render(directory=tmp))
#         g.view()


class SQLParserTest(unittest.TestCase):

    def test_hello(self):
        pass


if __name__ == '__main__':
    unittest.main()
