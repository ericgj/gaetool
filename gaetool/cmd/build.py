import os.path

from ._filesys import remove_and_create_dir
from ._config import config_dir, copy_config_files
from ._backend import backend_dir, copy_backend_dir, copy_backend_files
from ._template import render_templates
from ._environ import write_environ_vars

BUILD_ROOT = 'build'
ENV_FILE = 'env.json'

def run(log, args):
    build(args.env, args.service, log=log, build_dir=args.build_dir, env_file=args.env_file)

def build(env, service, *, log, build_dir=BUILD_ROOT, env_file=ENV_FILE):
    with log("build: %s %s" % (env,service), env=env, service=service, build_dir=build_dir):
        build_clear_build(log=log, build_dir=build_dir)
        build_copy_config(env, log=log, build_dir=build_dir)
        build_copy_backend_common(log=log, build_dir=build_dir)
        build_copy_backend_service(service, log=log, build_dir=build_dir)
        build_backend_templates(env, service, log=log, build_dir=build_dir)
        build_env_file(env, service, log=log, build_dir=build_dir, env_file=env_file)

def build_clear_build(*, log, build_dir=BUILD_ROOT):
    with log("clear build"):
        remove_and_create_dir(build_dir)

def build_copy_config(env, *, log, build_dir=BUILD_ROOT):
    with log("copy config", env=env):
        copy_config_files(env, os.path.join(build_dir,'config'))

def build_copy_backend_common(*, log, build_dir=BUILD_ROOT):
    with log("copy backend common"):
        copy_backend_dir('common', build_dir)

def build_copy_backend_service(service, *, log, build_dir=BUILD_ROOT):
    with log("copy backend service", service=service):
        copy_backend_files(service, build_dir)

def build_backend_templates(env, service, *, log, build_dir=BUILD_ROOT):
    with log("render backend templates", env=env, service=service):
        render_templates(
            config_dir(env), 
            backend_dir(service), 
            build_dir,
            extras={ 'environment': env, 'service': service }
        )

def build_env_file(env, service, *, log, build_dir=BUILD_ROOT, env_file=ENV_FILE):
    with log("create env file", env=env, service=service):
        write_environ_vars(env, service, build_dir=build_dir, env_file=env_file)


# Implementation

"""
def run_tests(env, service, *, test_runner, build_dir):
    if test_runner == 'unittest':
        cmd = python_test_cmd_unittest(build_dir)
    elif test_runner == 'pytest':
        cmd = python_test_cmd_pytest(build_dir)
    else:
        cmd = cmd_in_build(build_dir, test_runner)

    run_in_environ(env, service, cmd, build_dir=build_dir)


def run_in_environ(env, service, cmd, *, build_dir):
    subprocess.run( 
        " && ".join( 
            [ virtualenv_cmd(service_virtualenv(service)) ] + 
            environ_var_assigns(env, service, build_dir=build_dir) +
            cmd
        ), 
        shell=True, check=True
    )



def python_test_cmd_unittest(build_dir):
    if os.name == 'nt':
        return cmd_in_build(build_dir, "python -m unittest test\\test_* --buffer")
    else:
        return cmd_in_build(build_dir, "python -m unittest test/test_* --buffer")

def python_test_cmd_pytest(build_dir):
    if os.name == 'nt':
        return cmd_in_build(build_dir, "python -m pytest test\\")
    else:
        return cmd_in_build(build_dir, "python -m pytest test/")


"""

