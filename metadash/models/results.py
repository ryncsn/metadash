"""
Test results related classes provider hooked to ResultsDB

Can be used to report all data to ResultsDB, or store extra meta data for
objects in ResultsDB
"""
import resultsdb_api

from flask import current_app as app
from sqlalchemy import event

from .base import BareEntityModel, EntityModel
from .base import cached_property
from .service import provide
from . import db


API = resultsdb_api.ResultsDBapi(app.config['RESULTSDB_API'])


@provide('testcase')  # TODO: standard interface for provider
class TestCase(EntityModel):  # Inherit from EntityModel to have a UUID
    """
    Stands for a test case
    """
    __tablename__ = __alias__ = 'testcase'
    __namespace__ = 'testcase'

    name = db.Column(db.Integer, primary_key=True, unique=True)

    @property
    def results(self):
        page = 0
        ret = []
        res = API.get_results(page=page, testcases=self.name)
        while res['next']:
            ret.extend[res['data']]
            res = API.get_results(page=page, groups=self.uuid)
            page = page + 1

    def as_dict(self, detail=False):
        ret = super(TestCase, self).as_dict(detail=detail)
        ret['name'] = self.raw['ref_url']
        return ret

    def _save(self):
        pass


@provide('testresult')
class TestResult(EntityModel):
    """
    Reference to a Test Result on ResultDB
    Used to maintain local constraints, and make metadata tracking easier
    """
    __tablename__ = __alias__ = 'testresult'
    __namespace__ = 'testresult'

    RESULTS_MAP = ['PASSED', 'FAILED', 'INFO', 'NEEDS_INSPECTION']  # Just remainer
    id = db.Column(db.Integer, primary_key=True)

    @cached_property
    def raw(self):
        if not self.id:
            raise RuntimeError('Not initialized result instance')
        return API.get_result(self.id)

    @property
    def data(self):
        return self.raw['data']

    @property
    def outcome(self):
        return self.raw['outcome']

    @property
    def result(self):
        return self.outcome

    def as_dict(self, detail=False):
        ret = super(TestResult, self).as_dict(detail)
        ret['result'] = self.result
        return ret

    def _save(self):
        pass


@provide('testrun')
class TestRun(BareEntityModel):
    """
    Reference to a Test Group on ResultDB
    Used to maintain local constraints, and make metadata tracking easier
    """
    __alias__ = 'testrun'
    __namespace__ = 'testrun'

    @cached_property
    def raw(self):
        if not self.uuid:
            raise RuntimeError('Not initialized result instance')
        return API.get_group(self.uuid)

    @property
    def results(self):
        page = 0
        ret = []
        res = API.get_results(page=page, groups=self.uuid)
        while res['next']:
            ret.extend[res['data']]
            res = API.get_results(page=page, groups=self.uuid)
            page = page + 1

    def as_dict(self, detail=False):
        ret = super(TestRun, self).as_dict()
        return ret

    def _save(self):
        pass


# TODO: after_delete
@event.listens_for(TestResult, 'after_insert')
def _testresult_after_insert(mapper, connection, target):
    target._save()


@event.listens_for(TestRun, 'after_insert')
def _testgroup_after_insert(mapper, connection, target):
    target._save()


@event.listens_for(TestCase, 'after_insert')
def _testcase_after_insert(mapper, connection, target):
    target._save()
