# Google App Engine | Python 3 | Tooling

Development tooling and deployment rig for Python 3.x standard and flex
environments on Google App Engine.

## Features


## How to use

1. Set up and activate a virtualenv for development if you haven't already:

```bash
virtualenv .env
.env/bin/activate
```

2. Install the library:

```bash
pip install gaetool
```
(or add it to your requirements.txt, etc.)

3. Initialize and create a default service:

```bash
gaetool init my-gae-project-id
```

4. Initialize a new service:

```bash
gaetool service add my-service
```

5. Specify requirements for multiple services:

```bash
gaetool req add --service="my-service" --service="my-other-service" WebOb pytz
```

6. Install and freeze requirements:

```bash
gaetool req install --service="my-service" 
```

7. Build a service for a given environment:

```bash
gaetool build --service="my-service" development
```

8. Run tests on the build:

```bash
gaetool exec --service="my-service" development "python -m pytest"
```

9. Deploy a service for a given environment:

```bash
gaetool build --service="my-service" test
gaetool deploy --service="my-service" test
```

Note that as of version 0.2.1, linting and testing and command execution have
been taken out of the `build` and `deploy` commands. Having "de-bundled" 
commands makes it easier to construct build pipelines however you see fit. At
the same time, the tool will prevent you from executing a command or deploying 
the app if the specified environment or service doesn't match the build.


## Other commands

### template 

This is a more generic build command where you can specify the exact source
and target directories, file extension of the template files, and subdirectory
where the templates reside.

The following command is equivalent to the `gaetool build` above (but without
the lint and test steps):

```bash
gaetool template development backend/my-service build --file-ext=yaml --template-dir=.
```

This can be useful for frontend or other client builds that need to access the 
same config as the backend, for instance.


