# SecureMessaging
[![Build Status](https://travis-ci.org/qateam123/secure-messaging-ui.svg?branch=master)](https://travis-ci.org/qateam123/secure-messaging-ui)

## Run with Docker

To get secure-messaging-ui running the following command will build and run the containers
```
docker-compose up -d
```

When the containers are running you are able to access the application as normal, and code changes will be reflected in the running application.
However, any new dependencies that are added would require a re-build.

To rebuild the secure-messaging-ui container, the following command can be used.
```
docker-compose build
```

If you need to rebuild the container from scratch to re-load any dependencies then you can run the following
```
docker-compose build --no-cache
```

## Setup
Based on python 3

Create a new virtual env for python3

```
mkvirtual --python=`which python3` <your env name>
```

Install dependencies using pip

```
pip install -r requirements.txt
```
