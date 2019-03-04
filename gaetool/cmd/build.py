import os
import os.path
import subprocess
import ruamel.yaml as yaml

from ._filesys import remove_and_create_dir
from ._config import config_dir, copy_config_files, read_project_id
from ._backend import backend_dir, copy_backend_dir, copy_backend_files
from ._template import render_templates
from ._virtualenv import service_virtualenv, virtualenv_cmd

BUILD_ROOT = 'build'

def run(log, args):
    build(args.env, args.service, log=log, build_dir=args.build_dir)
    build_lint(log=log, build_dir=args.build_dir)
    build_test(args.env, args.service, 
        test_runner=args.test_runner, log=log, build_dir=args.build_dir
    )

def build(env, service, *, log, build_dir=BUILD_ROOT):
    with log("build: %s %s" % (env,service), env=env, service=service, build_dir=build_dir):
        build_clear_build(log=log, build_dir=build_dir)
        build_copy_config(env, log=log, build_dir=build_dir)
        build_copy_backend_common(log=log, build_dir=build_dir)
        build_copy_backend_service(service, log=log, build_dir=build_dir)
        build_backend_templates(env, service, log=log, build_dir=build_dir)

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

def build_lint(*, log, build_dir=BUILD_ROOT):
    with log("linting"):
        run_lint(build_dir=build_dir)

def build_test(env, service, *, test_runner, log, build_dir=BUILD_ROOT):
    with log("testing", env=env, service=service):
        run_tests(env, service, test_runner=test_runner, build_dir=build_dir)


# Implementation

def run_lint(*, build_dir):
    try:
        subprocess.run(['flake8', build_dir],
            stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True 
        )
    except subprocess.CalledProcessError as e:
        raise Exception(
            "Lint error(s) (flake8):\n" + 
            e.stderr.decode('utf-8') + "\n" +
            e.stdout.decode('utf-8')
        )

def run_tests(env, service, *, test_runner, build_dir):
    if test_runner == 'unittest':
        testcmd = python_test_cmd_unittest(build_dir)
    elif test_runner == 'pytest':
        testcmd = python_test_cmd_pytest(build_dir)
    else:
        testcmd = python_test_cmd(build_dir, test_runner)

    subprocess.run( 
        " && ".join( 
            [ virtualenv_cmd(service_virtualenv(service)) ] + 
            environ_var_assigns(env, build_dir=build_dir) +
            testcmd
        ), 
        shell=True, check=True
    )


def environ_var_assigns(env, *, build_dir):
    vars = read_environ_vars(build_dir)
    project = read_project_id(env)
    if os.name == 'nt':
        return environ_var_assigns_nt(project, vars)
    else:
        return environ_var_assigns_posix(project, vars)

def environ_var_assigns_nt(project, vars):
    return (
        [ "SET %s=%s" % (k,v) for (k,v) in vars.items() ] +
        [ "SET GOOGLE_CLOUD_PROJECT=%s" % (project,) ]
    )

def environ_var_assigns_posix(project, vars):
    return (
        [ 'export %s="%s"' % (k,v) for (k,v) in vars.items() ] +
        [ 'export GOOGLE_CLOUD_PROJECT="%s"' % (project,) ]
    )


def python_test_cmd_unittest(build_dir):
    if os.name == 'nt':
        return python_test_cmd(build_dir, "python -m unittest test\\test_* --buffer")
    else:
        return python_test_cmd(build_dir, "python -m unittest test/test_* --buffer")

def python_test_cmd_pytest(build_dir):
    return python_test_cmd(build_dir, "pytest test/")


def python_test_cmd(build_dir, testcmd):
    return [ "cd %s" % (build_dir,), testcmd ]



def read_environ_vars(build_dir):
    data = read_yaml( os.path.join(build_dir,'app.yaml') )
    return data.get('env_variables',{})

def read_yaml(fname):
    data = None
    with open(fname, 'r') as f:
        data = yaml.safe_load(f)
    return data

