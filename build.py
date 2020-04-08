from pybuilder.core import use_plugin, init, task, depends, before, after
from zipfile import ZipFile
import os

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.coverage')
use_plugin('python.install_dependencies')
use_plugin('python.distutils')
use_plugin('python.pydev')
use_plugin('python.flake8')
use_plugin('filter_resources')

name = 'dbdeps'
default_task = ['oxt']
version = '0.1'

@init
def set_properties(project):
    project.depends_on('graphviz')
    project.set_property('coverage_exceptions', ['main'])
    project.set_property('filter_resources_glob', ['**/description.xml'])
    project.version = version
    
    

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


@task
@depends('package')
def oxt(logger, project):
    get = lambda p:project.expand_path(project.get_property(p))
    join = os.path.join
    
    dir_dist = get('dir_target')
    target = join(dir_dist, 'dbdeps_oxt')
    dir_dist_dist = join(dir_dist, 'dist')
    os.makedirs(dir_dist_dist, exist_ok=True)
    file = join(dir_dist_dist, 'dbdeps.oxt')
    
    zipFilesInDir(target, file, target)
    logger.info('LibreOffice extension file written')


def mkdir(logger, path):
    logger.info("About to create: {0}".format(path))
    os.makedirs(path, exist_ok=True)
    
@before('package')
def prepare_oxt(logger, project):
    logger.warn('prepare_oxt STARTED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    get = lambda p:project.expand_path(project.get_property(p))
    join = os.path.join
    
    dir_dist = get('dir_target')
    mkdir(logger, dir_dist)
    target = join(dir_dist, 'dbdeps_oxt')
    mkdir(logger, target)
    dir_python = join(target, 'python')
    mkdir(logger, dir_python)
    pythonpath = join(dir_python, 'pythonpath')
    os.makedirs(pythonpath, exist_ok=True)
    os.system('python -m pip install graphviz --target {0}'.format(pythonpath))


    dir_src = get('dir_source_main_python')
    from shutil import copytree, copy
    c_target = join(pythonpath, 'dbdeps')
    copytree(join(dir_src, 'dbdeps'), c_target)
    def cp_to_target(file):
        copy(join(dir_src, file), join(dir_python, file))
    
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
    logger.warn('prepare_oxt ENDED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    

