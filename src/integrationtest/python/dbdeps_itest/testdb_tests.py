import unittest
from dbdeps_itest.lotest import LOIntegrationTest


class TestDBTest(LOIntegrationTest):

    def test_deps(self):
        from dbdeps import build_graph
        g = build_graph(self.ds)
        self.logger.info(g.render(directory=self.tmp_dir))
#         g.view()


if __name__ == '__main__':

    unittest.main()
