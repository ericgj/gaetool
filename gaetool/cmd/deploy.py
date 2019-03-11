import os
import subprocess

from ._config import read_project_id
from .build import build, build_lint

def run(log, args):
    with log('deploy', env=args.env, service=args.service):
        build(env=args.env, service=args.service, log=log)
        build_lint(log=log, build_dir=args.build_dir)
        deploy(args.env, args.service, config=args.config, build_dir=args.build_dir, log=log)

def deploy(env, service, *, log, config="*.yaml", build_dir="build"):
    with log('app deploy: %s %s' % (env,service), env=env, service=service):
        gcloud_app_deploy( read_project_id(env), env, config, build_dir )


def gcloud_app_deploy(project, version, config, build_dir):
    if os.name == 'nt':
        configfile = "%s\\%s" % (build_dir, config)
    else:
        configfile = "%s/%s" % (build_dir, config)

    cmd = """
        gcloud app deploy --no-promote --project="{project}" --version="{version}" {configfile}
    """.strip().format( project=project, version=version, configfile=configfile )

    subprocess.run(cmd, shell=True, check=True)


