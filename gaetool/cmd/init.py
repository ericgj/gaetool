import os.path
import random

from ._config import CONFIG_ROOT, make_config_dir, update_config_yaml, write_config
from ._template import render_template_file, copy_template_dir
from ._backend import BACKEND_ROOT
from .service import  add_backend_service, add_backend_service_virtualenv

def run(log, args):
    with log("init", project=args.project, env=args.env):
        init_config(args.project, args.env, log=log, force=args.force)
        init_backend(log=log, force=args.force)
        add_backend_service('default', log=log, force=args.force)
        add_backend_service_virtualenv('default', log=log, force=args.force)

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


# Implementation

def gen_secret():
    return ("%030x" % random.randrange(16**30)).upper()

