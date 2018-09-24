import os
import os.path
import shutil
import subprocess

from ._config import config_dir, copy_config_files
from ._backend import backend_dir, copy_backend_dir, copy_backend_files
from ._template import render_templates
from ._virtualenv import service_virtualenv, virtualenv_cmd

BUILD_ROOT = 'build'

def run(log, args):
    with log("build", env=args.env, service=args.service):
        build_clear_build(log=log)
        build_copy_config(args.env, log=log)
        build_copy_backend_common(log=log)
        build_copy_backend_service(args.service, log=log)
        build_backend_templates(args.env, args.service, log=log)
        build_lint(log=log)
        build_test(args.service, log=log)

def build_clear_build(*, log):
    with log("clear build"):
        remove_and_create_dir(BUILD_ROOT)

def build_copy_config(env, *, log):
    with log("copy config", env=env):
        copy_config_files(env, os.path.join(BUILD_ROOT,'config'))

def build_copy_backend_common(*, log):
    with log("copy backend common"):
        copy_backend_dir('common', BUILD_ROOT)

def build_copy_backend_service(service, *, log):
    with log("copy backend service", service=service):
        copy_backend_files(service, BUILD_ROOT)

def build_backend_templates(env, service, *, log):
    with log("render backend templates", env=env, service=service):
        render_templates(
            config_dir(env), 
            backend_dir(service), 
            BUILD_ROOT,
            extras={ 'environment': env, 'service': service }
        )

def build_lint(*, log):
    with log("linting"):
        run_lint()

def build_test(service, *, log):
    with log("testing", service=service):
        run_tests(service)


# Implementation

def remove_and_create_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

def run_lint():
    try:
        subprocess.run(['flake8', BUILD_ROOT],
            stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True 
        )
    except subprocess.CalledProcessError as e:
        raise Exception(
            "Lint error(s) (flake8):\n" + 
            e.stderr.decode('utf-8') + "\n" +
            e.stdout.decode('utf-8')
        )

def run_tests(service):
    subprocess.run( 
        " && ".join( [ virtualenv_cmd(service_virtualenv(service)), python_test_cmd()] ), 
        shell=True, check=True
    )

def python_test_cmd():
    if os.name == 'nt':
        return "cd build && python -m unittest test\\test_* --buffer"
    else:
        return "cd build && python -m unittest test/test_* --buffer"


