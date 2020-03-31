import unittest

from dbdeps import graph, buildGraph


class DbDepsTest(unittest.TestCase):
    def setUp(self):
        from dbdeps.outside import ds
        self.ds = ds
    
    def test_deps(self):
        g = buildGraph(self.ds)
        import tempfile
        tmp = tempfile.mktemp() 
        print(g.render(directory=tmp))      


class SQLParserTest(unittest.TestCase):

    def test_hello(self):
        pass
    
    
if __name__ == '__main__':
    unittest.main()
