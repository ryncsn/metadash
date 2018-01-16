"""
ResultsDB plugin

Help to view and submit results to/from ResultsDB,
and store extra metadata to make it possible and easier to do some statistic job,
and make other automation workflow easier.

(Maybe) async and local copy
"""

from resultsdb_api import ResultsDBapi, ResultsDBapiException
from typing import List

from metadash.cache import cached_property, cached_entity_property
from metadash.models import db
from metadash.models.base import BareEntityModel, EntityModel
from metadash.config import Config


# Restful API is not ACID, so use a high limit for bulk operation
FOREIGN_OBJECT_LIMIT = 65535


def API():
    return ResultsDBapi(Config.get("RESULTSDB_API_URL"))


def handle_404(func):
    def fn(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ResultsDBapiException as error:
            if error.response.status_code == 404:
                return {}
            raise
    return fn


class ResultsDBTestCase(EntityModel):  # Inherit from EntityModel, so have a UUID
    """
    Stands for a test case
    """
    __tablename__ = __alias__ = __namespace__ = 'resultsdb-testcase'

    # Key in resultsdb
    name = db.Column(db.Integer, primary_key=True, unique=True, index=True)

    @cached_property
    @handle_404
    def raw(self):
        return API().get_testcase(self.name) if self.name else {}

    @cached_entity_property
    def results(self) -> List[str]:
        return API().get_results(testcases=self.name, limit=FOREIGN_OBJECT_LIMIT)['data']

    @cached_property
    def ref_url(self):
        return self.raw.get('ref_url')

    @ref_url.setter
    def ref_url_setter(self, value: str):
        self.raw['ref_url'] = value

    def as_dict(self, detail=True):
        ret = super(ResultsDBTestCase, self).as_dict(detail=detail)
        ret['name'] = self.name
        ret['results'] = self.results
        ret['ref_url'] = self.ref_url
        return ret


class ResultsDBTestResult(EntityModel):
    """
    Reference to a Test Result on ResultDB
    Used to maintain local constraints, and make metadata tracking easier
    """
    __tablename__ = __alias__ = __namespace__ = 'resultsdb-testresult'

    RESULTS_MAP = ['PASSED', 'FAILED', 'INFO', 'NEEDS_INSPECTION']  # Just reminder

    # Key in resultsdb
    id = db.Column(db.Integer, primary_key=True, index=True)

    @classmethod
    def fetch(cls, *args, **kwargs):
        kwargs.setdefault('testcases:like', Config.get('TESTCASE_NAMESPACE'))
        results = API().get_results(*args, **kwargs)
        return results

    @cached_property
    @handle_404
    def raw(self):
        return API().get_result(self.id) if self.id else {}

    @property
    def data(self):
        # TODO: integrate after composive proxy is done
        return self.raw['data']

    @property
    def outcome(self):
        return self.raw['outcome']

    def from_raw(self, dict_):
        """
        Update from raw ResultsDB API data
        """
        self.properties = dict_['data']
        self.groups = dict_['groups']
        self.id = dict_['id']
        self.outcome = dict_['outcome']
        self.ref_url = dict_['ref_url']
        self.testcase = dict_['testcase']['name']

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
        self.raw['testcase'] = {"name": value}

    @cached_property
    def ref_url(self):
        return self.raw.get('ref_url')

    @ref_url.setter
    def ref_url(self, value: str):
        self.raw['ref_url'] = value

    @property
    def testgroups(self) -> List[str]:
        return self.raw['groups']

    @testgroups.setter
    def testgroups(self, value: List[str]):
        self.raw['groups'] = value

    def as_dict(self, detail=True):
        ret = super(ResultsDBTestResult, self).as_dict(detail)
        ret['id'] = self.id
        ret['outcome'] = self.outcome
        ret['testcase'] = self.testcase
        ret['testgroups'] = self.testgroups
        ret['ref_url'] = self.ref_url
        return ret


class ResultsDBTestGroup(BareEntityModel):
    """
    Reference to a Test Group on ResultDB
    Used to maintain local constraints, and make metadata tracking easier
    """
    __tablename__ = __alias__ = __namespace__ = 'resultsdb-testgroup'

    @cached_property
    @handle_404
    def raw(self):
        return API().get_group(self.uuid) if self.uuid else {}

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

    @cached_entity_property
    def results(self) -> List[ResultsDBTestResult]:
        return API().get_results(groups=self.uuid, limit=FOREIGN_OBJECT_LIMIT)['data']

    def as_dict(self, detail=True):
        ret = super(ResultsDBTestGroup, self).as_dict()
        ret['ref_url'] = self.ref_url
        ret['results'] = self.results
        ret['description'] = self.description
        return ret
