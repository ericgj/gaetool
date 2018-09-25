import os
import os.path
import shutil

from ._filesys import copy_files_within

BACKEND_ROOT = 'backend'

def backend_dir(dir):
    return os.path.join(BACKEND_ROOT, dir)

def backend_service_file(service, name):
    return os.path.join(BACKEND_ROOT, service, name)

def copy_backend_dir(service, target, force=False):
    sourcedir = backend_dir(service)
    targetdir = os.path.join( target, os.path.basename(sourcedir) ) 
    if force and os.path.exists(targetdir):
        shutil.rmtree(targetdir)
    if not os.path.exists(targetdir):
        shutil.copytree( sourcedir, targetdir )

def copy_backend_files(service, target, force=False):
    sourcedir = backend_dir(service)
    targetdir = target
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    copy_files_within( sourcedir, targetdir, force=force)



