import os.path
from setuptools import setup

def rel(*paths):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *paths)

def get_version():
    from gaetool.version import VERSION
    return VERSION

def get_long_description():
    ret = ''
    with open(rel('README.md'), 'r') as f:
        ret = f.read()
    return ret

REQUIREMENTS = [
    "blessings>=1.7,<2.0;platform_system=='Linux'",
    "colorama>=0.3,<0.4;platform_system=='Linux'",
    "pystache>=0.5,<0.6",
    "ruamel.yaml>=0.15,<0.16"
]

DEV_REQUIREMENTS = [
    "flake8>=3.5,<4.0"
]

setup(
    name="gaetool",
    version=get_version(),
    author="Eric Gjertsen",
    author_email="ericgj72@gmail.com",
    description="Development tooling and deployment rig for Python 3.x standard and flex environments on Google App Engine.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=[ "gaetool", "gaetool/cmd", "gaetool/template" ],
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=REQUIREMENTS,
    extras_require={ 'dev': DEV_REQUIREMENTS },
    entry_points={ 'console_scripts': [ 'gaetool = gaetool.__main__:main' ] },
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only"
    ]
)

