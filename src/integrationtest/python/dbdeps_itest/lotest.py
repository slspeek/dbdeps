import unittest
import logging
import subprocess
import shlex
import os
import tempfile
import sys
import uno
import time


logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)

SOFFICE_CMD = '/opt/libreoffice6.2/program/soffice --safe-mode --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo --nodefault  --headless /home/steven/dbdeps/testdb/testdb.odb'


class LOIntegrationTest(unittest.TestCase):

    def wait_for_connection(self):
#         time.sleep(3) # needed if no --headless
        localContext = uno.getComponentContext()

        # create the UnoUrlResolver
        resolver = localContext.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", localContext)

        ctx = 'Error'
        i = 0
        while(i < 5):
            try:
                # connect to the running office
                ctx = resolver.resolve(
                    "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
                break
            except:
                i += 1
                logger.debug('waiting on uno connection for %.0d seconds', i/1.25)
                time.sleep(1)

        if ctx == 'Error':
            raise OSError('Unable to connect to LibreOffice')
        return ctx.ServiceManager

    def setUp(self):
        self.startLO()
        self.logger = logger
        self.tmp_dir = tempfile.mkdtemp()
        logger.debug('CWD: %s', os.getcwd())
        cmd = 'unzip -d {} /home/steven/dbdeps/target/dist/dbdeps.oxt'.format(
            self.tmp_dir)
        os.system(cmd)
        sys.path.append(os.path.join(self.tmp_dir, 'python/pythonpath'))
        logger.debug('PATH: %s', sys.path)
        self.smgr = self.wait_for_connection()
        self.desktop = self.smgr.createInstance("com.sun.star.frame.Desktop")
        while(True):
            self.doc = self.desktop.getCurrentComponent()
            if self.doc != None:
                break
            else:
                logger.debug('waiting on current component')
                time.sleep(0.1)
        self.ds = self.doc.DataSource
        

    def startLO(self):
        self.office_proc = subprocess.Popen(
            shlex.split(SOFFICE_CMD), shell=False)
        logger.debug("LibreOffice started")

    def tearDown(self):
        self.desktop.terminate()
