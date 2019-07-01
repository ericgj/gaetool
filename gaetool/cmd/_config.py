import os
import os.path
import shutil
import ruamel.yaml as yaml

CONFIG_ROOT = 'config'

def config_dir(dir):
    return os.path.join(CONFIG_ROOT,dir)

def config_file(dir, fname):
    return os.path.join( config_dir(dir), fname )


def read_project_id(env):
    data = read_config_yaml(env, 'project')
    return None if data is None else data.get('id')

def make_config_dir(env, force=False):
    targetdir = config_dir(env)
    if force and os.path.exists(targetdir):
        shutil.rmtree(targetdir)
    if not os.path.exists(targetdir):
        os.makedirs( targetdir, exist_ok=True)

def update_config_yaml(env, name, key, value):
    data = read_config_yaml(env, name)
    if data is None:
        data = {}
    data[key] = value
    fname = config_file(env, name + ".yaml")
    with open(fname, 'w') as f:
        f.write(yaml.dump(data))

def write_config_yaml(env, name, data, force=False):
    write_config(env, name, yaml.dump(data), force=force)

def write_config(env, name, value, force=False):
    fname = config_file(env, name)
    if not force and os.path.isfile(fname):
        return
    with open(fname,'w') as f:
        f.write(value)

def read_config_yaml(env, name):
    fname = config_file(env, name + ".yaml")
    if not os.path.isfile(fname):
        return None
    data = None
    with open(fname,'r') as f:
        data = yaml.safe_load(f)
    return data

def copy_config_files(env, target, force=False):
    sourcedir = config_dir(env)
    targetdir = target
    if force and os.path.exists(targetdir):
        shutil.rmtree(targetdir)
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    copy_files_within( sourcedir, targetdir, force=force)


def copy_files_within(source, dest, force=False):
    for (root, dirs, files) in os.walk(source):
        for item in dirs:
            src_path = os.path.join(root, item)
            dst_path = os.path.join(dest, src_path.replace(source + os.sep,''))
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)

        for item in files:
            src_path = os.path.join(root, item)
            dst_path = os.path.join(dest, src_path.replace(source + os.sep,''))
            if os.path.exists(dst_path):
                if force:
                    shutil.copy2(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
        
