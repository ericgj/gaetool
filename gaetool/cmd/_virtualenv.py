import os
import os.path
import subprocess
import tempfile

def service_virtualenv(service):
    return ".env-%s" % service

def virtualenv_cmd(name):
    if os.name == 'nt':
        return "{name}\\Scripts\\activate".format(name=name)
    else:
        return ". {name}/bin/activate".format(name=name)

def create_virtualenv(name, force=False):
    if not force and os.path.exists(name):
        return
    try:
        subprocess.run( ['virtualenv', name], 
            stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True 
        )
    except subprocess.CalledProcessError as e:
        raise Exception(e.stderr.decode('utf-8'))


def uninstall_virtualenv(name):
    if os.name == 'nt':
        uninstall_virtualenv_nt(name)
    else:
        uninstall_virtualenv_posix(name)

def uninstall_virtualenv_posix(name):
    cmd = '(pip freeze | grep -v "^-e" | xargs pip uninstall -y)'
    run_in_virtualenv_quiet(name, [cmd])

def uninstall_virtualenv_nt(name):
    (f, tmpfile) = tempfile.mkstemp()
    f.close()
    cmd1 = 'pip freeze > %s' % tmpfile
    cmd2 = 'pip uninstall -r %s -y' % tmpfile
    cmd3 = 'rm -f %s' % tmpfile
    run_in_virtualenv_quiet(name, [cmd1,cmd2,cmd3])


def install_virtualenv(name, reqfile):
    cmd = 'pip install -r %s' % reqfile
    run_in_virtualenv_quiet(name, [cmd])

def freeze_virtualenv(name, reqfile):
    cmd = 'pip freeze > %s' % reqfile
    run_in_virtualenv_quiet(name, [cmd])



def run_in_virtualenv(name, cmds, *, env={}, cwd=None):
    if 'SYSTEMROOT' in os.environ:
        env['SYSTEMROOT'] = os.environ['SYSTEMROOT']   # Note: Windows needs

    subprocess.run( 
        " && ".join( 
            [ virtualenv_cmd(name) ] + 
            ( [] if cwd is None else [ 'cd "%s"' % (cwd,) ] ) + 
            cmds
        ), 
        shell=True, check=True, env=env
    )

def run_in_virtualenv_quiet(name, cmds, *, env={}, cwd=None):
    if 'SYSTEMROOT' in os.environ:
        env['SYSTEMROOT'] = os.environ['SYSTEMROOT']   # Note: Windows needs

    try:
        subprocess.run(
            ' && '.join(
                [ virtualenv_cmd(name) ] + 
                ( [] if cwd is None else [ 'cd "%s"' % (cwd,) ] ) + 
                cmds 
            ),
            shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=env
        )
    except subprocess.CalledProcessError as e:
        raise Exception(e.stderr.decode('utf-8'))

