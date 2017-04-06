"""
Some basic metadata
"""
from .base import AttributeModel
from .results import TestResult, TestGroup, TestCase
from . import db

from ..utils import debounce


class TestGroupStatistic(AttributeModel):
    """
    Statistic info for a group of tests
    """
    __entity_only__ = [TestGroup.__namespace__]
    __unique_attr__ = True
    __alias__ = 'statistic'

    passed = db.Column(db.Integer())
    failed = db.Column(db.Integer())
    skipped = db.Column(db.Integer())
    error = db.Column(db.Integer())

    def _on_update(self):
        all_tests = self.entity.results
        for test in all_tests:
            if test.result == "PASS":
                self.passed += 1
            elif test.result == "FAIL":
                self.failed += 1
            elif test.result == "SKIP":
                self.skipped += 1
            elif test.result == "ERROR":
                self.error += 1

    @debounce(10)
    def on_entity_update(self):
        self._on_update()


class TestCaseStatistic(AttributeModel):
    """
    Statistic info for a test case
    """
    __entity_only__ = [TestCase.__namespace__]
    __unique_attr__ = True
    __alias__ = 'statistic'

    passed = db.Column(db.Integer())
    failed = db.Column(db.Integer())
    skipped = db.Column(db.Integer())
    error = db.Column(db.Integer())

    def _on_update(self):
        all_tests = self.entity.results
        for test in all_tests:
            if test.result == "PASS":
                self.passed += 1
            elif test.result == "FAIL":
                self.failed += 1
            elif test.result == "SKIP":
                self.skipped += 1
            elif test.result == "ERROR":
                self.error += 1

    @debounce(10)
    def on_entity_update(self):
        self._on_update()
