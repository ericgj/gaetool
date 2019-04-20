from ._environ import check_environ_vars
from ._virtualenv import run_in_virtualenv, service_virtualenv


def run(log, args):
    vars = exec_check_environ( args.env, args.service, 
        log=log, build_dir=args.build_dir, env_file=args.env_file
    )
    cmds = args.cmds
    for (i,cmd) in enumerate(cmds):
        with log("executing %d/%d" % (i+1,len(cmds)), env=args.env, service=args.service):
            run_in_virtualenv(
                service_virtualenv(args.service), 
                [cmd], 
                env=vars, 
                cwd=args.build_dir
            )

def exec_check_environ(env, service, *, log, build_dir, env_file):
    with log('checking environment', env=env, service=service):
        return check_environ_vars(env, service, build_dir=build_dir, env_file=env_file)


   
