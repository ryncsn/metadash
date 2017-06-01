"""
Minimized model for storing test results

With quiet lots of data stored in ResultsDB.
Can't access any data in ResultsDB, that don't have a corresponding
TestCase instance in local database, if back port is needed, need to
implement it in other side since can't do ACID job through REST.

TODO: This may produce some garbage.
XXX: Storing relationship data remotely just because it works, shoule create local relation
TODO: Store readonly data locally, as they should never need to be synced
"""
from resultsdb_api import ResultsDBapi, ResultsDBapiException
from config import ActiveConfig
from typing import List

from . import get_or_create
from sqlalchemy import event
from sqlalchemy.orm.session import Session

from .base import BareEntityModel, EntityModel
from .service import provide, defered, cached_property
from . import db

# Restful API is not ACID, use a limit for bulk operation
FOREIGN_OBJECT_LIMIT = 65535


API = ResultsDBapi(ActiveConfig.RESULTSDB_API)


def handle_404(func):
    def fn(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ResultsDBapiException as error:
            if error.response.status_code == 404:
                return {}
            raise
    return fn


# Using defered for async job which need to call the restful api
# TODO: defered loop is not supported
@provide('testcase')
class TestCase(EntityModel):  # Inherit from EntityModel, so have a UUID
    """
    Stands for a test case
    """
    __tablename__ = __alias__ = __namespace__ = 'testcase'

    name = db.Column(db.Integer, primary_key=True, unique=True, index=True)

    @cached_property
    @handle_404
    def raw(self):
        return API.get_testcase(self.name) if self.name else {}

    @cached_property
    @defered
    def results(self) -> List[str]:
        return API.get_results(testcases=self.name, limit=FOREIGN_OBJECT_LIMIT)['data']

    @cached_property
    def ref_url(self):
        return self.raw.get('ref_url')

    @ref_url.setter
    def ref_url_setter(self, value: str):
        self.raw['ref_url'] = value

    def as_dict(self, detail=False):
        ret = super(TestCase, self).as_dict(detail=detail)
        ret['name'] = self.name
        ret['results'] = self.results
        ret['ref_url'] = self.ref_url
        return ret

    def _delete(self):
        raise NotImplementedError()

    def _save(self):
        API.create_testcase(self.name, ref_url=self.ref_url)

    def _update(self):
        API.update_testcase(self.name, ref_url=self.ref_url)


@provide('testresult')
class TestResult(EntityModel):
    """
    Reference to a Test Result on ResultDB
    Used to maintain local constraints, and make metadata tracking easier
    """
    __tablename__ = __alias__ = __namespace__ = 'testresult'

    RESULTS_MAP = ['PASSED', 'FAILED', 'INFO', 'NEEDS_INSPECTION']  # Just reminder

    # Track id in ResultsDB
    id = db.Column(db.Integer, primary_key=True, index=True)

    @cached_property
    @handle_404
    def raw(self):
        return API.get_result(self.uuid) if self.uuid else {}

    @property
    def data(self):
        # TODO: integrate after composive proxy is done
        return self.raw['data']

    @property
    def outcome(self):
        return self.raw['outcome']

    @property
    def submit_time(self):
        return self.raw['submit_time']

    @outcome.setter
    def outcome(self, value: str):
        self.raw['outcome'] = value

    @property
    def testcase(self):
        return self.raw.get('testcase', {}).get('name')

    @testcase.setter
    def testcase(self, value: str):
        session = Session.object_session(self)
        get_or_create(session, TestCase, name=value)
        self.raw['testcase'] = value

    @cached_property
    def ref_url(self):
        return self.raw.get('ref_url')

    @ref_url.setter
    def ref_url(self, value: str):
        self.raw['ref_url'] = value

    @property
    def testgroups(self) -> List[str]:
        return self.raw['groups']

    def as_dict(self, detail=False):
        ret = super(TestResult, self).as_dict(detail)
        ret['id'] = self.id
        ret['outcome'] = self.outcome
        ret['testcase'] = self.testcase
        ret['testgroups'] = self.testgroups
        ret['ref_url'] = self.ref_url
        return ret

    def _delete(self):
        raise NotImplementedError()

    def _save(self):
        ret = API.create_result(self.outcome, self.testcase, groups=self.testgroups, ref_url=self.ref_url)
        self.id = ret['id']

    def _update(self):
        raise NotImplementedError()


@provide('testgroup')
class TestGroup(BareEntityModel):
    """
    Reference to a Test Group on ResultDB
    Used to maintain local constraints, and make metadata tracking easier
    """
    __tablename__ = __alias__ = __namespace__ = 'testgroup'

    @cached_property
    @handle_404
    def raw(self):
        return API.get_group(self.uuid) if self.uuid else {}

    @cached_property
    def description(self):
        return self.raw.get('description')

    @description.setter
    def description(self, value):
        self.raw['description'] = value

    @cached_property
    def ref_url(self):
        return self.raw.get('ref_url')

    @ref_url.setter
    def ref_url_setter(self, value: str):
        self.raw['ref_url'] = value

    @cached_property
    @defered
    def results(self) -> List[str]:
        return API.get_results(groups=self.uuid, limit=FOREIGN_OBJECT_LIMIT)['data']

    def as_dict(self, detail=False):
        ret = super(TestGroup, self).as_dict()
        ret['ref_url'] = self.ref_url
        ret['results'] = self.results
        ret['description'] = self.description
        return ret

    def _delete(self):
        raise NotImplementedError()

    def _save(self):
        self.uuid = API.create_group(uuid=self.uuid, ref_url=self.ref_url, description=self.description)['uuid']

    def _update(self):
        API.update_group(uuid=self.uuid, ref_url=self.ref_url, description=self.description)


# TODO: some helper can make this more clear
@event.listens_for(TestResult, 'before_insert')
def _testresult_before_insert(mapper, connection, target):
    target._save()


@event.listens_for(TestResult, 'after_update')
def _testresult_after_update(mapper, connection, target):
    target._update()


@event.listens_for(TestGroup, 'before_insert')
def _testgroup_before_insert(mapper, connection, target):
    target._save()


@event.listens_for(TestGroup, 'after_update')
def _testgroup_after_update(mapper, connection, target):
    target._update()


@event.listens_for(TestCase, 'before_insert')
def _testcase_before_insert(mapper, connection, target):
    target._save()


@event.listens_for(TestCase, 'after_update')
def _testcase_after_update(mapper, connection, target):
    target._update()


@event.listens_for(TestResult, 'after_delete')
def _testresult_after_delete(mapper, connection, target):
    target._delete()


@event.listens_for(TestGroup, 'after_delete')
def _testgroup_after_delete(mapper, connection, target):
    target._delete()


@event.listens_for(TestCase, 'after_delete')
def _testcase_after_delete(mapper, connection, target):
    target._delete()
