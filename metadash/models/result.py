"""
Some basic metadata
"""
from metadash.models.base import EntityModel
from metadash.models.types import UUID
from metadash.models import db


class ManualTestResult(EntityModel):
    """
    Presents a test result
    """
    __tablename__ = 'metadash_manual_result'
    __alias__ = 'manual_result'

    outcome = db.Column(db.String(3072), nullable=False, index=True)


class AutoTestResult(EntityModel):
    """
    Presents a test result
    """
    __tablename__ = 'metadash_auto_result'
    __alias__ = 'auto_result'

    outcome = db.Column(db.String(3072), nullable=False, index=True)


class Group(EntityModel):
    """
    Presents a group of test results, eg: a test run
    """
    __tablename__ = 'metadash_test_group'
    __alias__ = 'test_group'

    name = db.Column(db.String(512), nullable=False, index=True)
