from pybuilder.core import use_plugin, init, task, depends, description
from zipfile import ZipFile
from os.path import join
import os
import shutil


use_plugin('python.core')
use_plugin('python.unittest')
use_plugin("python.integrationtest")
use_plugin('python.coverage')
use_plugin('python.install_dependencies')
use_plugin('python.distutils')
use_plugin('python.pydev')
use_plugin('python.flake8')
use_plugin('filter_resources')
use_plugin('copy_resources')

name = 'dbdeps'
default_task = ['analyze', 'publish', 'oxt']
version = '0.1.2'


@init
def set_properties(project):
    project.depends_on('graphviz')
    project.set_property('coverage_exceptions', ['main'])
    project.set_property('filter_resources_glob', ['**/description.xml'])
    project.set_property("copy_resources_glob", ["META-INF/*",
                                                 'description/*',
                                                 'description.xml', 'icons/*.png',
                                                 'AddonUI.xcu',
                                                 'Accelerators.xcu',
                                                 'LICENSE',
                                                 'README.md',
                                                 'src/main/python/**'])

    project.set_property("copy_resources_target", "$dir_target/dbdeps_oxt")
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


def move(src, dst, logger):
    r = shutil.move(src, dst)
    logger.debug('moving {0} to {1} resulted in {2}'.format(src, dst, r))


@task
@depends('package')
@description("Builds a LibreOffice extension file")
def oxt(logger, project):

    dir_zip_source = project.expand_path('$dir_target/dbdeps_oxt')
    dir_target_dist = project.expand_path('$dir_target/dist')
    os.makedirs(dir_target_dist, exist_ok=True)

    zip_file = join(dir_target_dist, 'dbdeps.oxt')

    dir_pythonpath = project.expand_path(
        '$dir_target/dbdeps_oxt/python/pythonpath')
    if os.path.exists(dir_pythonpath):
        shutil.rmtree(project.expand_path(
        '$dir_target/dbdeps_oxt/python'))
    os.makedirs(dir_pythonpath, exist_ok=True)
    
    os.system(
        'python -m pip install graphviz --target {0}'.format(dir_pythonpath))

    move(project.expand_path('$dir_target/dbdeps_oxt/src/main/python/dbdeps'),
         project.expand_path(
             '$dir_target/dbdeps_oxt/python/pythonpath'), logger
         )

    move(project.expand_path('$dir_target/dbdeps_oxt/src/main/python/main.py'),
         project.expand_path(
             '$dir_target/dbdeps_oxt/python/main.py'), logger
         )

    shutil.rmtree(project.expand_path('$dir_target/dbdeps_oxt/src/'))

    zipFilesInDir(dir_zip_source, zip_file, dir_zip_source)

    logger.info('LibreOffice extension file written to {0}'.format(zip_file))
