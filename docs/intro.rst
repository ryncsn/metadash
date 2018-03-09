Intro
====================================

What is it?

Metadash is a (meta)data manager, a data aggregator, or a data gateway, a dashboard center, and supports plugins.

Metadash make use of concepts like "Generic Foreign Key(GKF)", "Entity attribute value model(EAV)", and there are two type of data in metadash, entity and attribute, each entitie have UUID for indexing and caching. Though sometimes, some of thoes conceptions are considered anti-pattern, but with powerful ORM and helpers, it's extremely flexible with acceptable performence.

Metadash uses Flask, SQLAlchemy, Vue, Webpack, and some plugins for them. There are some 'magic' and workaround, by which I try to make the model and api layer neat and clean, and make plugins as simple as possible. More documents is comming later.
