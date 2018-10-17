# Metadash

[Live Demo](http://metadash-frontend-metadash-openshift-online.a3c1.starter-us-west-1.openshiftapps.com/dashboard)

[![Build Status](https://travis-ci.org/ryncsn/metadash.svg?branch=master)](https://travis-ci.org/ryncsn/metadash) [![codecov](https://codecov.io/gh/ryncsn/metadash/branch/master/graph/badge.svg)](https://codecov.io/gh/ryncsn/metadash) 

## What is it?

 * Metadash is a (meta)data manager, a data aggregator, or a data gateway, a dashboard center, and supports plugins.
 * Metadash make use of concepts like "Generic Foreign Key(GKF)", "Entity attribute value model(EAV)", and there are two type of data in metadash, entity and attribute, each entitie have UUID for indexing and caching. Though sometimes, some of thoes conceptions are considered anti-pattern, but with powerful ORM and helpers, it's extremely flexible with acceptable performence.
 * Metadash uses Flask, SQLAlchemy, Vue, Webpack, and some plugins for them. There are some 'magic' and workaround, by which I try to make the model and api layer neat and clean, and make plugins as simple as possible. More documents is comming later.

## Quick start:
(Docker and docker-compose required)

### Build docker image
```
docker build -t metadash .
```

### Setup containers
```
docker-compose up -d
```

## Setup Development Enviroment:
Dev enviroment (With hot reload and dev server)
(npm and pipenv required, and python > 3.5)

### Setup dependency
```
bin/md-manager setup --develop --no-build
```

### Config Redis and SQL Database
*(Optinal: Required if you want to try async tasks or have better performance)*
```
cp config/config.py.dev.example config/config.py

# Edit config according to your requirement
$EDITOR config/config.py
```

### Start devel server
```
npm run ui-dev
bin/md-manager runserver
```

Any contribute, suggestion, issue is high welcomed!
It's not well documented and not fully implemented yet, so everything could go wrong.
