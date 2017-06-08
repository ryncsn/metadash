"""
Config manager
"""
from metadash.models import db


class ConfigItem(db.Model):
    key = db.Column(db.Text(), primary_key=True, nullable=False)
    value = db.Column(db.Text())
