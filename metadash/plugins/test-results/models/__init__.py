"""
A test result storing schema consulting ResultsDB and Junit used by Jenkins

This is tend to play as a test result sumittion center of a CI platform
So use the model: testrun <- testresult -> testcase to make it clearer to track
And metadash provides tag and attribute for any entity, so only keep most basic
and often used attributes as columns.

ref_url should be either null or unique
"""
from sqlalchemy.sql import func, label

from metadash.injector import provide
from metadash.cache import cache_on_arguments, cached_entity_property
from metadash.models import db
from metadash.models.base import EntityModel
from metadash.models.types import UUID


# Restful API is not ACID, so use a high limit for bulk operation
FOREIGN_OBJECT_LIMIT = 65535

URL_LENGTH = 2083


@provide('testcase')
class TestCase(EntityModel):  # Inherit from EntityModel, so have a UUID
    """
    Stands for a test case
    """
    __tablename__ = __alias__ = __namespace__ = 'testcase'

    # Key in resultsdb
    name = db.Column(db.String(512), primary_key=True, unique=True, index=True)
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    ref_url = db.Column(db.String(URL_LENGTH), unique=True, nullable=True)

    def as_dict(self, detail=True):
        ret = super(TestCase, self).as_dict(detail=detail)
        return ret


@provide('testrun')
class TestRun(EntityModel):
    """
    Reference to a Test Group on ResultDB
    Used to maintain local constraints, and make metadata tracking easier
    """
    __tablename__ = __alias__ = __namespace__ = 'testrun'
    STATUS = ['PENDING', 'RUNNING', 'FINISHED']  # Just reminder
    status = db.Column(db.Enum(*STATUS, name='testrun_status'), index=True, default='PENDING')
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    name = db.Column(db.String(512), nullable=False, unique=False)
    ref_url = db.Column(db.String(URL_LENGTH), unique=True, nullable=True)

    @cached_entity_property(expiration_time=30)
    def results(self):
        return dict(
            db.session.query(TestResult.result, label('count', func.count(TestResult.result)))
            .filter(TestResult.testrun_uuid == self.uuid)
            .group_by(TestResult.result).all())

    @cached_entity_property()
    def _properties_cache(self):
        return dict(self.properties)

    def as_dict(self, **kwargs):
        # TODO: helper for properties caching
        exclude = kwargs.setdefault('exclude', [])
        if 'properties' not in exclude:
            exclude.append('properties')
            ret = super(TestRun, self).as_dict(**kwargs)
            ret['properties'] = self._properties_cache
        else:
            ret = super(TestRun, self).as_dict(**kwargs)
        ret['results'] = self.results
        return ret


@provide('testresult')
class TestResult(EntityModel):
    """
    Reference to a Test Result on ResultDB
    Used to maintain local constraints, and make metadata tracking easier
    """
    __tablename__ = __alias__ = __namespace__ = 'testresult'

    RESULTS = ['PASSED', 'FAILED', 'SKIPPED', 'ERROR']  # Just reminder
    RESULTSDB_MAP = ['PASSED', 'FAILED', 'INFO', 'NEEDS_INSPECTION']  # Just reminder

    result = db.Column(db.Enum(*RESULTS, name='testresult_result'), index=True, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    duration = db.Column(db.Float(), default=0.0, nullable=True)
    ref_url = db.Column(db.String(URL_LENGTH), unique=True, nullable=True)

    testrun_uuid = db.Column(UUID, db.ForeignKey('testrun.uuid'), nullable=False)
    testrun = db.relationship("TestRun", foreign_keys=[testrun_uuid], backref="testresults")
    testcase_name = db.Column(db.String(512), db.ForeignKey('testcase.name'), nullable=False)
    testcase = db.relationship("TestCase", foreign_keys=[testcase_name], backref="testresults")

    def as_dict(self, **kwargs):
        ret = super(TestResult, self).as_dict(**kwargs)
        return ret
