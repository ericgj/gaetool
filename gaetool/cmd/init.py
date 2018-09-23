import os
import os.path
import shutil
import random
import subprocess
import ruamel.yaml as yaml
import pystache

CONFIG_ROOT = 'config'
BACKEND_ROOT = 'backend'
TEMPLATE_ROOT = os.path.join( 
    os.path.dirname( os.path.realpath(__file__) ),
    "..",
    "template"
)

def run(log, args):
    with log("init", project=args.project, env=args.env):
        init_config(args.project, args.env, log=log, force=args.force)
        init_backend(log=log, force=args.force)
        init_backend_service('default', log=log, force=args.force)
        init_backend_service_virtualenv('default', log=log, force=args.force)

def init_config(project, envs, *, log, force=False):
    with log("init config", envs=envs):
        for env in envs:
            init_config_dir(env, log=log, force=force)
            init_config_project_id(env, project, log=log)
            init_config_secret(env, log=log, force=force)
            init_config_static(env, project, log=log, force=force)

def init_config_dir(env, *, log, force=False):
    with log("init config dir: %s" % (env,), env=env):
        make_config_dir( env, force=force)

def init_config_project_id(env, project, *, log):
    with log("init config project id: %s" % (env,), env=env, project=project):
        update_config_yaml( env, 'project', 'id', project )

def init_config_secret(env, *, log, force=False):
    with log("init config secret: %s" % (env,), env=env):
        write_config( env, 'secret.yaml', gen_secret(), force=force )

def init_config_static(env, project, *, log, force=False):
    with log("init config static: %s" % (env,), env=env):
        render_template_file( os.path.join(CONFIG_ROOT,env,'static.yaml'), 
            {'project': project}, 
            force=force
        ) 


def init_backend(*, log, force=False):
    with log("init backend"):
        copy_template_dir( os.path.join(BACKEND_ROOT,'common'), force=force)

def init_backend_service(service, *, log, force=False):
    with log("init backend service", service=service):
        copy_template_dir( os.path.join(BACKEND_ROOT,'service'), 
                           target=os.path.join(BACKEND_ROOT,service), 
                           force=force
        )

def init_backend_service_virtualenv(service, *, log, force=False):
    with log("init backend service virtualenv", service=service):
        create_virtualenv('.env-%s' % service, force=force)


# Implementation

def config_dir(dir):
    return os.path.join(CONFIG_ROOT,dir)

def config_file(dir, fname):
    return os.path.join( config_dir(dir), fname )

def template_file(fname):
    return os.path.join(TEMPLATE_ROOT,fname)   

def backend_file(fname):
    return os.path.join(BACKEND_ROOT,fname)


def make_config_dir(env, force=False):
    targetdir = config_dir(env)
    if force and os.path.exists(targetdir):
        shutil.rmtree(targetdir)
    if not os.path.exists(targetdir):
        os.makedirs( targetdir, exist_ok=True)

def update_config_yaml(env, name, key, value):
    fname = config_file(env, name + ".yaml")
    data = None
    if os.path.isfile(fname):
        with open(fname,'r') as f:
            data = yaml.safe_load(f)
    if data is None:
        data = {}
    data[key] = value
    with open(fname, 'w') as f:
        f.write(yaml.dump(data))

def write_config(env, name, value, force=False):
    fname = config_file(env, name)
    if not force and os.path.isfile(fname):
        return
    with open(fname,'w') as f:
        f.write(value)


def copy_template_dir( dir, target=None, force=False ):
    sourcedir = template_file(dir)
    targetdir = dir if target is None else target
    if force and os.path.exists(targetdir):
        shutil.rmtree(targetdir)
    if not os.path.exists(targetdir):
        shutil.copytree( sourcedir, targetdir )


def render_template_file(name, vars, target=None, force=False):
    fname = template_file(name)
    if not os.path.isfile(fname):
        raise ValueError("No such template file found: %s" % (name,))
    target = name if target is None else target
    if not force and os.path.exists(target):
        return
    tmpl = ''
    with open(fname,'r') as f:
        tmpl = f.read()
    with open(target,'w') as f:
        f.write( pystache.render(tmpl, vars) )

def create_virtualenv(name, force=False):
    if not force and os.path.exists(name):
        return
    try:
        subprocess.run( ['virtualenv', name], 
            stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True 
        )
    except subprocess.CalledProcessError as e:
        raise Exception(e.stderr.decode('utf-8'))

def gen_secret():
    return ("%030x" % random.randrange(16**30)).upper()

