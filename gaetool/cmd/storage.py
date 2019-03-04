import os.path
import subprocess
from ._config import read_project_id, write_config_yaml

def run_setup(log, args):
    config_file = args.config + ".yaml"
    with log('setup'):
        project = read_project_id(args.env)
        run_make_bucket(args.env, project, log=log)
        run_defacl_set(args.env, project, group=args.group, log=log)
        run_gen_config_static(args.env, project, 
            service=args.service, config_file=config_file, log=log, force=args.force
        )

def run_sync(log, args):
    with log('sync'):
        project = read_project_id(args.env)
        run_storage_sync(args.env, project, service=args.service, source=args.source, 
            cache=args.cache, log=log
        ) 
        

def run_make_bucket(env, project, *, log):
    with log('make bucket: %s' % (env,), env=env):
        gsutil_mb( bucket_name(env, project), project=project )

def run_defacl_set(env, project, *, group, log):
    if not group is None:
        with log('set default ACL: %s' % (env,), env=env, group=group):
            gsutil_defacl( bucket_name(env, project), 
                group=(group,'R') 
            )

def run_gen_config_static(env, project, *, service, config_file, log, force):
    with log('update config: %s' % (env,), env=env):
        data = {
            'protocol': 'https',
            'host': 'storage.googleapis.com',
            'port': None,
            'path': '/'.join((bucket_name(env, project), service))
        }
        write_config_yaml(env, config_file, data, force=force)  


def run_storage_sync(env, project, *, service, source, log, cache=False):
    with log('sync: %s %s' % (env,service), env=env, service=service):
        gsutil_rsync( 
            bucket_name(env,project),
            service, 
            os.path.join(source,service),
            cache=cache
        ) 


def gsutil_mb( bucket, project ):
    cmd = """
        gsutil mb -p "{project}" "gs://{bucket}/"
    """.strip().format( project=project, bucket=bucket )

    subprocess.run(cmd, shell=True, check=True)


def gsutil_defacl( bucket, group ):
    cmd = """
        gsutil defacl ch -g "{group}" "gs://{bucket}/"
    """.strip().format( bucket=bucket, group=":".join(group) )

    subprocess.run(cmd, shell=True, check=True)
    
def gsutil_rsync( bucket, path, source, cache=False ):
    hdrs = '-h "Cache-Control:no-cache, must-revalidate"' if not cache else ''
    cmd = """
        gsutil {headers} rsync -d -r "{source}" "gs://{bucket}/{path}"
    """.strip().format( headers=hdrs, bucket=bucket, path=path, source=source )

    subprocess.run(cmd, shell=True, check=True)


def bucket_name(env, project):
    return "%s-dot-%s" % (env,project)

