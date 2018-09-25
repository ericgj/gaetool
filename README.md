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


