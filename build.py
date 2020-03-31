from pybuilder.core import use_plugin, init, task, depends
from zipfile import ZipFile
import os

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.coverage')
use_plugin('python.install_dependencies')
use_plugin('python.distutils')
use_plugin('python.pydev')
use_plugin('python.flake8')

name = 'dbdeps'
default_task = 'publish'


@init
def set_properties(project):
    project.depends_on('graphviz')
    project.set_property('coverage_exceptions', ['main'])
    

def zipFilesInDir(dirName, zipFileName):
    # create a ZipFile object
    with ZipFile(zipFileName, 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                # create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath)
            
@task
@depends('package')
def oxt(logger, project):
    target = project.expand_path(project.get_property('dir_dist'))
    file = os.path.join(project.get_property('dir_target'), 'dbdeps.oxt')
    zipFilesInDir(target, file)
    logger.info('LibreOffice extension file written')
    

