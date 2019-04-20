import os
import subprocess

from ._config import read_project_id
from ._environ import check_environ_vars

def run(log, args):
    deploy_check_environ( args.env, args.service, 
        log=log, build_dir=args.build_dir, env_file=args.env_file
    ) 
    with log('deploy', env=args.env, service=args.service):
        deploy(args.env, args.service, config=args.config, build_dir=args.build_dir, log=log)

def deploy_check_environ(env, service, *, log, build_dir, env_file):
    with log('checking environment', env=env, service=service):
        return check_environ_vars(env, service, build_dir=build_dir, env_file=env_file)

def deploy(env, service, *, log, build_dir, config="*.yaml"):
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


