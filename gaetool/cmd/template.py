import os
import os.path

from ._filesys import remove_and_create_dir, copy_files_within
from ._config import config_dir, copy_config_files
from ._template import render_templates

def run(log, args):
    with log('template: %s' % (args.env,), env=args.env):
        template_clear_target(target_dir=args.target_dir, log=log)
        template_copy_config(args.env, target_dir=args.target_dir, log=log)
        template_copy(args.template_dir, target_dir=args.target_dir, log=log)
        template_render(args.env, args.template_dir, args.target_dir, 
             file_ext=args.file_ext, log=log
        )


def template_clear_target(*, target_dir, log):
    with log("clear target", target_dir=target_dir):
        remove_and_create_dir(target_dir)

def template_copy_config(env, *, log, target_dir):
    with log("copy config", env=env, target_dir=target_dir):
        copy_config_files(env, os.path.join(target_dir,'config'))

def template_copy(template_dir, *, log, target_dir):
    with log("copy", template_dir=template_dir, target_dir=target_dir):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        copy_files_within( template_dir, target_dir )

def template_render(env, template_dir, target_dir, *, file_ext, log):
    with log('rendering templates: %s %s' % (env, template_dir),
             env=env, template_dir=template_dir, 
             target_dir=target_dir, file_ext=file_ext):

        render_templates(
            config_dir(env), 
            template_dir,
            target_dir,
            file_ext=file_ext,
            extras={ 'environment': env }
        )


