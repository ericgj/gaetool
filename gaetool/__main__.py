import logging
from argparse import ArgumentParser
import colorama

logging.basicConfig(level=logging.INFO)
colorama.init()  # terminal colors shim for Windows

from .cmd import init
from .log import Log


def main():
    cmd = ArgumentParser(description='Deployment tools for Python GAE projects')
    sub = cmd.add_subparsers(help='command help')
    
    # init
    init = init_parser(sub)
    add_common_args(init)

    args = cmd.parse_args()
    if args.verbose == True:
        log = Log(logging.DEBUG)
    else:
        log = Log(logging.INFO)

    args.func(log, args)


def init_parser(root):
    cmd = root.add_parser('init', help='Initialize a project')
    cmd.add_argument('project', help='Google App Engine project ID')
    cmd.add_argument('-e', '--env', action='append',
        default=['development','test','staging','production'],
        help='Extra environment'
    )
    cmd.set_defaults(func=init.run)
    return cmd

def add_common_args(parser):
    parser.add_argument('-f', '--force', dest='force', action='store_true',
        help="Make changes to files if they exist"
    ) 
    parser.add_argument('--no-force', dest='force', action='store_false',
        help="Do not make changes to files if they exist (default)"
    )
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
        help="Verbose output"
    ) 
    parser.add_argument('--no-verbose', dest='verbose', action='store_false',
        help="Normal output (default)"
    )
    parser.set_defaults(force=False, verbose=False)


if __name__ == '__main__':
    main()
