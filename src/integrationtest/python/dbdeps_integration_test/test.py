import unittest
import logging
import subprocess, shlex
import os
import tempfile
import sys

logger = logging.getLogger()

SOFFICE_CMD = '/opt/libreoffice6.2/program/soffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo --nodefault --headless testdb/testdb.odb'



class LOIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        print('CWD:', os.getcwd())
        cmd = 'unzip -d {} /home/steven/dbdeps/target/dist/dbdeps.oxt'.format(self.tmp_dir)
        os.system(cmd)
        sys.path =  ['/home/steven/dbdeps/src/integrationtest/python/dbdeps_integration_test', '/opt/libreoffice6.2/program', '/opt/libreoffice6.2/program/python-core-3.5.7/lib', '/opt/libreoffice6.2/program/python-core-3.5.7/lib/lib-dynload', '/opt/libreoffice6.2/program/python-core-3.5.7/lib/lib-tk', '/opt/libreoffice6.2/program/python-core-3.5.7/lib/site-packages', '/home/steven/dbdeps/src/integrationtest/python', '/opt/libreoffice6.2/program/python-core-3.5.7/lib/python35.zip', '/opt/libreoffice6.2/program/python-core-3.5.7/lib/python3.5', '/opt/libreoffice6.2/program/python-core-3.5.7/lib/python3.5/plat-linux', '/opt/libreoffice6.2/program/python-core-3.5.7/lib/python3.5/lib-dynload']
        sys.path.append(os.path.join(self.tmp_dir, 'python/pythonpath'))
        print('PATH:', sys.path)
        self.office_proc = subprocess.Popen(shlex.split(SOFFICE_CMD), shell=False)
        from dbdeps.outside import ds
        self.ds = ds
        self.logger = logger


    def tearDown(self):
        self.office_proc.terminate()
        self.office_proc.kill()
        self.office_proc.wait()
        os.system('pkill soffice')
      
