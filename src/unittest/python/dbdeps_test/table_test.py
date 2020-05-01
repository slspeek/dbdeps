import unittest

from dbdeps.table import tables, views


class TableTest(unittest.TestCase):
    def setUp(self):
        from dbdeps_test.outside import datasource

        self.con = datasource().getConnection("", "")

    def test_tables(self):
        tn = tables(self.con)
        print(tn)
        self.assertEqual(2, len(tn), "Should have 2 real tables")

    def test_views(self):
        v = views(self.con)
        self.assertEqual(1, len(v), "Should have 1 view")
        self.assertEqual("view1", v[0].name, 'Should have name "view1"')


if __name__ == "__main__":
    unittest.main()
