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
    logger.info(project.properties)
    
    dir_dist = get('dir_dist')
    target = join(dir_dist, 'dbdeps_oxt')
    dir_dist_dist = join(dir_dist, 'dist')
    os.makedirs(dir_dist_dist, exist_ok=True)
    file = join(dir_dist_dist, 'dbdeps.oxt')
    os.makedirs(target, exist_ok=True)
    dir_python = join(target, 'python')
    pythonpath = join(dir_python, 'pythonpath')
    os.makedirs(pythonpath, exist_ok=True)
    os.system('python -m pip install graphviz --target {0}'.format(pythonpath))


    from shutil import copytree, copy
    c_target = join(pythonpath, 'dbdeps')
    copytree(join(dir_dist, 'dbdeps'), c_target)
    def cp_to_target(file):
        copy(join(dir_dist, file), join(dir_python, file))
    
    cp_to_target('main.py')
        
    def cp_to_target(file):
        copy(join(project.get_property('basedir'), file), join(target, file))
    
    def cptree_to_target(file):
        copytree(join(project.get_property('basedir'), file), join(target, file))
    
    cp_to_target('description.xml')
    cp_to_target('AddonUI.xcu')
    cp_to_target('Accelerators.xcu')
    cp_to_target('LICENSE')
    cptree_to_target('META-INF')
    cptree_to_target('description')
    cptree_to_target('icons')
    zipFilesInDir(target, file, target)
    logger.info('LibreOffice extension file written')
    

