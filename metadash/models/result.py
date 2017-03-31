"""
Some basic metadata
"""
import datetime

from metadash.models.base import EntityModel
from metadash.models.types import UUID
from metadash.models import db


class TestRun(EntityModel):
    """
    Presents a group of test results, eg: a test run
    """
    __tablename__ = __alias__ = 'test_run'

    name = db.Column(db.String(512), nullable=False, index=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class TestResult(EntityModel):
    """
    Presents a test result
    """
    __tablename__ = __alias__ = 'test_result'
    ALL_RESULTS = ['PASS', 'FAIL', 'SKIP', 'ERROR']

    result = db.Column(db.Enum(*ALL_RESULTS, name="result"), nullable=False, index=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    test_run = db.Column(UUID, db.ForeignKey(TestRun.uuid))
