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
pip install gae-python3-tooling
```

3. Initialize:

```bash
gae init my-gae-project-id
```

4. Initialize a new service:

```bash
gae service add my-service
```

5. Specify requirements:

```bash
gae req add --service="my-service" --service="my-other-service" WebOb pytz
```

6. Install (and freeze) requirements:

```bash
gae req install --service="my-service" 
```

7. Build (and lint and test) a service for a given environment:

```bash
gae build development --service="my-service"
```

8. Build and deploy a service for a given environment:

```bash
gae deploy test --service="my-service"
```


