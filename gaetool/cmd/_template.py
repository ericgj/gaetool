import os
import os.path
import shutil
import pystache
from pystache.renderer import Renderer
import ruamel.yaml as yaml

TEMPLATE_ROOT = os.path.join( 
    os.path.dirname( os.path.realpath(__file__) ),
    "..",
    "template"
)


def template_file(fname):
    return os.path.join(TEMPLATE_ROOT,fname)   

def copy_template_dir( dir, target=None, force=False ):
    sourcedir = template_file(dir)
    targetdir = dir if target is None else target
    if force and os.path.exists(targetdir):
        shutil.rmtree(targetdir)
    if not os.path.exists(targetdir):
        shutil.copytree( sourcedir, targetdir )

def render_template_file(name, vars, target=None, force=False):
    fname = template_file(name)
    if not os.path.isfile(fname):
        raise ValueError("No such template file found: %s" % (name,))
    target = name if target is None else target
    if not force and os.path.exists(target):
        return
    tmpl = ''
    with open(fname,'r') as f:
        tmpl = f.read()
    with open(target,'w') as f:
        f.write( pystache.render(tmpl, vars) )


def render_templates( source_dir, template_dir, target_dir, file_ext='yaml', extras={} ):
    data = load_config(source_dir, extras)
    renderer = Renderer(
        search_dirs=[template_dir], 
        file_extension=file_ext,
        missing_tags='strict'
    )
    for f in os.listdir(template_dir):
        fname, ext = os.path.splitext(f)
        if ext == ('.' + file_ext) and os.path.isfile(os.path.join(template_dir,f)):
            with open(os.path.join(target_dir,f), 'w') as o:
                o.write(renderer.render_name(fname, data))


def load_config(dir, extras={}):
    ret = dict(
        ( os.path.splitext(f)[0], load_yaml(os.path.join(dir,f)) )
            for f in os.listdir(dir) if (
                os.path.splitext(f)[1] in ('.yaml', '.json') and
                os.path.isfile(os.path.join(dir,f))
            )
    )
    for (k,v) in extras.items():
        ret[k] = v
    return ret

def load_yaml(fname):
    data = None
    with open(fname,'r') as f:
        data = yaml.safe_load(f)
    return data

