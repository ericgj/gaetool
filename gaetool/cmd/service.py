
from ._template import copy_template_dir
from ._backend import backend_dir
from ._virtualenv import create_virtualenv, service_virtualenv

def run_add(log, args):
    with log("service add", service=args.service):
        add_backend_service(args.service, log=log, force=args.force)
        add_backend_service_virtualenv(args.service, log=log, force=args.force)
    

def add_backend_service(service, *, log, force=False):
    with log("add backend service", service=service):
        copy_template_dir( backend_dir('service'), 
                           target=backend_dir(service), 
                           force=force
        )

def add_backend_service_virtualenv(service, *, log, force=False):
    with log("add backend service virtualenv", service=service):
        create_virtualenv( service_virtualenv(service), force=force)




