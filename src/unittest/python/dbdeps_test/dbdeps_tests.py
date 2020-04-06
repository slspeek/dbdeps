import unittest

from dbdeps import build_graph


class DbDepsTest(unittest.TestCase):
    def setUp(self):
        from dbdeps.outside import ds
        self.ds = ds
    
    def test_deps(self):
        g = build_graph(self.ds)
        import tempfile
        tmp = tempfile.mktemp() 
        print(g.render(directory=tmp))
#         g.view()
             


class SQLParserTest(unittest.TestCase):

    def test_hello(self):
        pass
    
    
if __name__ == '__main__':
    unittest.main()
