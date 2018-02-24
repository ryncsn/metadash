# Metadash

[![Build Status](https://travis-ci.org/ryncsn/metadash.svg?branch=master)](https://travis-ci.org/ryncsn/metadash) [![codecov](https://codecov.io/gh/ryncsn/metadash/branch/master/graph/badge.svg)](https://codecov.io/gh/ryncsn/metadash)

## What is it?

 * Metadash is a (meta)data manager, a data aggregator, or a data gateway, a dashboard center, and supports plugins.
 * Metadash make use of concepts like "Generic Foreign Key(GKF)", "Entity attribute value model(EAV)", and there are two type of data in metadash, entity and attribute, each entitie have UUID for indexing and caching. Though sometimes, some of thoes conceptions are considered anti-pattern, but with powerful ORM and helpers, it's extremely flexible with acceptable performence.
 * Metadash uses Flask, SQLAlchemy, Vue, Webpack, and some plugins for them. There are some 'magic' and workaround, by which I try to make the model and api layer neat and clean, and make plugins as simple as possible. More documents is comming later.

## Get started
Deploy reference:
(docker and docker-compose required)
```
# Config
cp config/__init__.py config/config.py
$EDITOR config/config.py
# Use you favourite editor to edit config/config.py #

# Build docker image
docker build -t metadash .

# Setup containers
docker-compose up -d
```

Dev enviroment (With hot reload and dev server)
(npm and pipenv required, and python > 3.5)
```
# Setup dependency
bash setup.sh --dependency-only

# Config
cp config/__init__.py config/config.py
$EDITOR config/config.py
# Use you favourite editor to edit config/config.py #

# Start devel server
npm run ui-dev
python manager.py runserver
```

Any contribute, suggestion, issue is high welcomed!
It's not well documented and not fully implemented yet, so everything could go wrong.
