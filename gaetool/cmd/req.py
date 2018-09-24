
from ._backend import backend_service_file
from ._virtualenv import (
    service_virtualenv, create_virtualenv, 
    uninstall_virtualenv, install_virtualenv, freeze_virtualenv
)


def run_install(log, args):
    with log('install', service=args.service):
        req_create_virtualenv(args.service, force=args.force, log=log)
        if args.uninstall:
            req_uninstall(args.service, log=log)
        req_install(args.service, log=log)
        req_freeze(args.service, log=log)

def run_add(log, args):
    services = list(set(
        ['default'] if len(args.service) == 0 else args.service
    ))
    with log('add requirements', services=services, requirements=args.requirement):
        for service in services:
            req_add(service, args.requirement, log=log)

def req_add(service, reqs, *, log):
    with log('add requirements: %s' % (service,), service=service, requirements=reqs):
        append_requirements( 
            backend_service_file(service, 'requirements-.txt'),
            reqs 
        )


def req_create_virtualenv(service, *, log, force=False):
    with log('create virtualenv', service=service):
        create_virtualenv( service_virtualenv(service), force=force)

def req_uninstall(service, *, log):
    with log('uninstall existing libraries', service=service):
        uninstall_virtualenv( service_virtualenv(service) )

def req_install(service, *, log):
    with log('install requirements', service=service):
        install_virtualenv( service_virtualenv(service), 
            backend_service_file(service, 'requirements-.txt')
        )

def req_freeze(service, *, log):
    with log('freeze requirements', service=service):
        freeze_virtualenv( service_virtualenv(service),
            backend_service_file(service, 'requirements.txt')
        )



def append_requirements( reqfile, reqs ):
    with open(reqfile, 'a') as f:
        for req in reqs:
            print(req, file=f)


