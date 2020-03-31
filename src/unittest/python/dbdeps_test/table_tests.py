import unittest

from dbdeps.table import tables, views


class TableTest(unittest.TestCase):

    def setUp(self):
        from dbdeps.outside import ds
        self.con = ds.getConnection("","")

    def test_tables(self):
        tn = tables(self.con)
        print(tn)
        self.assertEqual(2, len(tn), 'Should have 2 real tables')
    
    def test_views(self):
        v = views(self.con)
        self.assertEqual(1, len(v), 'Should have 1 view')
        self.assertEqual('view1',v[0].name, 'Should have name "view"') 
        
    
if __name__ == '__main__':
    unittest.main()
