import unittest
import logging
import subprocess, shlex
import time
import os


from dbdeps_integration_test.test  import LOIntegrationTest


class TestDBTest(LOIntegrationTest):
    
    def test_deps(self):
        from dbdeps import build_graph
        g = build_graph(self.ds)
        import tempfile
        tmp = tempfile.mktemp()
        self.logger.info(g.render(directory=tmp))
#         g.view()

    
if __name__ == '__main__':
    unittest.main()
