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

7. Build, lint and test a service for a given environment:

```bash
gaetool build development --service="my-service"
```

8. Build and deploy a service for a given environment:

```bash
gaetool deploy test --service="my-service"
```


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


### build --exec

After building, you can run an arbitrary command within the built environment:
that is, with all the environment variables set and activating the service-
specific python virtual environment. 

```bash
gaetool build test --exec="bin/seed-datastore" 
```

This is useful for things that need a runtime environment similar to the
deployed environment, such as seeding a data store, or running the app inside
a local web server, etc.

