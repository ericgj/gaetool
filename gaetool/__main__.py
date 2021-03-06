import logging
from argparse import ArgumentParser

try:
    import colorama
    colorama.init()  # terminal colors shim for Windows... 
                     # except blessings doesn't work with Windows, so this is kind of pointless
except:
    pass

logging.basicConfig(level=logging.INFO)

from .cmd import init, service, build, template, exec, req, deploy, storage
from .log import Log

def main():
    cmd = ArgumentParser(description='Deployment tools for Python Google App Engine projects')
    sub = cmd.add_subparsers(help='command help')
    
    # init
    init_cmd = init_parser(sub)
    add_force_args(init_cmd)
    add_common_args(init_cmd)

    # service
    service_parser(sub)

    # req
    req_parser(sub)

    # build
    build_cmd = build_parser(sub)
    add_build_args(build_cmd)
    add_common_args(build_cmd)

    # template
    templ_cmd = templ_parser(sub)
    add_common_args(templ_cmd)
    
    # exec
    exec_cmd = exec_parser(sub)
    add_build_args(exec_cmd)
    add_common_args(exec_cmd)

    # deploy
    deploy_cmd = deploy_parser(sub)
    add_build_args(deploy_cmd)
    add_common_args(deploy_cmd)

    # storage
    storage_parser(sub)

    args = cmd.parse_args()
    if args.verbose == True:
        log = Log(logging.DEBUG)
    else:
        log = Log(logging.INFO)

    args.func(log, args)


def init_parser(root):
    cmd = root.add_parser('init', description='Initialize a project')
    cmd.add_argument('project', help='Google App Engine project ID')
    cmd.add_argument('-e', '--env', action='append',
        default=['development','test','staging','production'],
        help='Extra environments, multiple can be specified'
    )
    cmd.set_defaults(func=init.run)
    return cmd

def service_parser(root):
    cmd = root.add_parser('service')
    sub = cmd.add_subparsers(help='actions on services')

    # add
    service_add = service_add_parser(sub)
    add_force_args(service_add)
    add_common_args(service_add)

    return cmd

def service_add_parser(root):
    cmd = root.add_parser('add', description='Add a backend service')
    cmd.add_argument('service', help='Name of the service')
    cmd.set_defaults(func=service.run_add)
    return cmd

def req_parser(root):
    cmd = root.add_parser('req')
    sub = cmd.add_subparsers(help='actions on requirements')

    # install
    req_install = req_install_parser(sub)
    add_common_args(req_install)

    # add
    req_add = req_add_parser(sub)
    add_common_args(req_add)

    return cmd

def req_install_parser(root):
    cmd = root.add_parser('install', description='Install and freeze requirements')
    cmd.add_argument('-s', '--service', help='Name of the service', default='default')
    cmd.add_argument('--uninstall', dest='uninstall', action='store_true',
        help='Uninstall existing libraries first'
    )
    cmd.add_argument('--no-uninstall', dest='uninstall', action='store_false',
        help='Do not uninstall existing libraries first (default)'
    )
    cmd.set_defaults(uninstall=False, func=req.run_install)
    return cmd

def req_add_parser(root):
    cmd = root.add_parser('add', description='Add requirements across services')
    cmd.add_argument('requirement', metavar='REQ', nargs='+',
        help='Requirement to add (in pip install format)'
    )
    cmd.add_argument('-s', '--service', action='append', default=[],
        help='Name of the service ("default" if none specified), multiple can be specified'
    )
    cmd.set_defaults(func=req.run_add)
    return cmd
  
def build_parser(root):
    cmd = root.add_parser('build', description="Build, lint and test service locally")
    cmd.add_argument('env', help='Runtime environment')
    cmd.add_argument('-s', '--service', help='Name of the service', default='default')
    cmd.set_defaults(func=build.run)
    return cmd

def templ_parser(root):
    cmd = root.add_parser('template', description="Generic build from templates")
    cmd.add_argument('env', help='Runtime environment (determines config)')
    cmd.add_argument('source_dir', help='Source directory')
    cmd.add_argument('target_dir', help='Target (build) directory')
    cmd.add_argument('--template-dir', 
        help='Source subdirectory for templates (default: .)'
    )
    cmd.add_argument('--file-ext', default='yaml', 
        help='File extension of templates (default: yaml)'
    )
    cmd.set_defaults(func=template.run)
    return cmd

def exec_parser(root):
    cmd = root.add_parser('exec', description="Execute command(s) in built environment")
    cmd.add_argument('env', help='Runtime environment')
    cmd.add_argument('-s', '--service', help='Name of the service', default='default')
    cmd.add_argument('cmds', nargs='+', help='Command(s) to execute in built environment')
    cmd.set_defaults(func=exec.run)
    return cmd

def deploy_parser(root):
    cmd = root.add_parser('deploy', description="Build and deploy service to Google App Engine")
    cmd.add_argument('env', help='Runtime environment (GAE version)')
    cmd.add_argument('-s', '--service', help='Name of the service', default='default')
    cmd.add_argument('-c', '--config', help='Config (yaml) files to deploy', default='*.yaml')
    cmd.set_defaults(func=deploy.run)
    return cmd

def storage_parser(root):
    cmd = root.add_parser('storage')
    sub = cmd.add_subparsers(help='manage static files on Google Storage')

    # setup
    storage_setup = storage_setup_parser(sub)
    add_force_args(storage_setup)
    add_common_args(storage_setup)

    # sync
    storage_sync = storage_sync_parser(sub)
    add_common_args(storage_sync)

    return cmd

def storage_setup_parser(root):
    cmd = root.add_parser('setup', description="Set up Google Storage bucket")
    cmd.add_argument('env', help='Runtime environment (GAE version)')
    cmd.add_argument('-s', '--service', dest='service', 
        help='Name of the service', default='default')
    cmd.add_argument('-g', '--group', dest='group', 
        help='Group entity read access to bucket')
    cmd.add_argument('--config', dest='config', default='static', 
        help='Local config file to update')
    cmd.set_defaults(func=storage.run_setup)
    return cmd

def storage_sync_parser(root):
    cmd = root.add_parser('sync', description="Sync Google Storage bucket")
    cmd.add_argument('env', help='Runtime environment (GAE version)')
    cmd.add_argument('-s', '--service', dest='service', 
        help='Name of the service', default='default')
    cmd.add_argument('--source', dest='source', 
        help='Source directory or URL', default='static')
    cmd.add_argument('--cache', dest='cache', action='store_true',
        help='Use default Google Storage caching')
    cmd.add_argument('--no-cache', dest='cache', action='store_false',
        help='Turn off Google Storage caching (default)')
    cmd.set_defaults(cache=False, func=storage.run_sync)
    return cmd


def add_force_args(parser):
    parser.add_argument('-f', '--force', dest='force', action='store_true',
        help="Make changes to files if they exist"
    ) 
    parser.add_argument('--no-force', dest='force', action='store_false',
        help="Do not make changes to files if they exist (default)"
    )
    parser.set_defaults(force=False)

def add_build_args(parser):
    parser.add_argument('--build-dir', help='Build (output) directory', default=build.BUILD_ROOT)
    parser.add_argument('--env-file', help='Environment var file', default=build.ENV_FILE)


def add_common_args(parser):
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
        help="Verbose output"
    ) 
    parser.add_argument('--no-verbose', dest='verbose', action='store_false',
        help="Normal output (default)"
    )
    parser.set_defaults(verbose=False)


if __name__ == '__main__':
    main()
