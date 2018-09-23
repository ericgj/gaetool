# Google App Engine | Python 3 | Tooling

Development tooling and deployment rig for Python 3.x standard and flex
environments on Google App Engine.

## Features


## How to use

1. Set up and activate a virtualenv for development if you haven't already:

    virtualenv .env
    .env/bin/activate

2. Install the library:

    pip install gae-python3-tooling

3. Initialize:

    gae init my-gae-project-id

4. Initialize a new service:

    gae service add my-service

5. Specify requirements:

    gae req add --service="my-service" --service="my-other-service" WebOb pytz

6. Update (and freeze) requirements:

    gae req update --service="my-service" --service="my-other-service"

7. Build (and lint and test) a service:

    gae build development --service="my-service"

8. Deploy (build first) a service:

    gae deploy test --service="my-service"


