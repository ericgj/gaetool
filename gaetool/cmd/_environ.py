import os.path
import json
from ruamel.yaml import YAML
yaml = YAML(typ='safe')
yaml.default_flow_style = False

from ._config import read_project_id

def write_environ_vars(env, service, *, build_dir, env_file):
    """ 
    Note: written as JSON, not YAML, so GAE doesn't think it's a config
    file during deployment.
    """
    vars = fetch_environ_vars(env, service, build_dir=build_dir)
    with open(os.path.join(build_dir, env_file), 'w') as f:
        json.dump(vars, f)

def read_environ_vars(*, build_dir, env_file):
    return read_yaml(os.path.join(build_dir, env_file))

def check_environ_vars(env, service, *, build_dir, env_file):
    vars = read_environ_vars(build_dir=build_dir, env_file=env_file)
    actual_env = vars.get('GAE_VERSION')
    actual_service = vars.get('GAE_SERVICE')
    if not (actual_env == env):
        raise ValueError(
            'The current build is for the %s environment, but you expected %s'  % 
            (actual_env, env)
        )
    if not (actual_service == service):
        raise ValueError(
            'The current build is for the %s service, but you expected %s' % 
            (actual_service, service)
        )
    return vars

def fetch_environ_vars(env, service, *, build_dir):
    project = read_project_id(env)
    vars = read_app_yaml_environ_vars(build_dir)
    vars['GOOGLE_CLOUD_PROJECT'] = project
    vars['GAE_SERVICE'] = service
    vars['GAE_VERSION'] = env
    return vars

def read_app_yaml_environ_vars(build_dir):
    data = read_yaml( os.path.join(build_dir,'app.yaml') )
    return data.get('env_variables',{})

def read_yaml(fname):
    data = None
    with open(fname, 'r') as f:
        data = yaml.load(f)
    return data

