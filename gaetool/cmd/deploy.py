import os
import subprocess

from ._config import read_project_id
from .build import build, build_lint, build_test

def run(log, args):
    with log('deploy', env=args.env, service=args.service):
        build(env='development', service=args.service, log=log)
        build_lint(log=log)
        build_test(args.service, log=log)

        build(env=args.env, service=args.service, log=log)
        deploy(args.env, args.service, config=args.config, log=log)

def deploy(env, service, *, log, config="*.yaml"):
    with log('app deploy: %s %s' % (env,service), env=env, service=service):
        gcloud_app_deploy( read_project_id(env), env, config )


def gcloud_app_deploy(project, version, config):
    if os.name == 'nt':
        configfile = "build\\%s" % (config,)
    else:
        configfile = "build/%s" % (config,)

    cmd = """
        gcloud app deploy --no-promote --project="{project}" --version="{version}" {configfile}
    """.strip().format( project=project, version=version, configfile=configfile )

    subprocess.run(cmd, shell=True, check=True)


