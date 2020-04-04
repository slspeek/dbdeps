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
    

def zipFilesInDir(dirName, zipFileName, root):
    # create a ZipFile object
    with ZipFile(zipFileName, 'w') as zipObj:
        # Iterate over all the files in directory
        
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                # create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath, os.path.relpath(filePath, root))
            
@task('package')
def oxt(logger, project):
    get = lambda p:project.expand_path(project.get_property(p))
    join = os.path.join
    
    dir_dist = get('dir_dist')
    target = join(dir_dist, 'dbdeps_oxt')
    os.makedirs(join(dir_dist, 'dist'), exist_ok=True)
    file = join(join(dir_dist, 'dist'), 'dbdeps.oxt')
    os.makedirs(target, exist_ok=True)
    pythonpath = join(target, 'pythonpath')
    os.makedirs(pythonpath, exist_ok=True)
    os.system('python -m pip install graphviz --target {0}'.format(pythonpath))


    from shutil import copytree, copy
    c_target = join(pythonpath, 'dbdeps')
    copytree(join(dir_dist, 'dbdeps'), c_target)
    copy(join(dir_dist, 'main.py'), join(target, 'main.py'))
    zipFilesInDir(target, file, target)
    logger.info('LibreOffice extension file written')
    

