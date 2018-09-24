import os
import subprocess

from ._template import copy_template_dir
from ._backend import backend_dir

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
        create_virtualenv('.env-%s' % service, force=force)



# Implementation

def create_virtualenv(name, force=False):
    if not force and os.path.exists(name):
        return
    try:
        subprocess.run( ['virtualenv', name], 
            stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True 
        )
    except subprocess.CalledProcessError as e:
        raise Exception(e.stderr.decode('utf-8'))

