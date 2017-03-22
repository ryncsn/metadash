#!/bin/env python
import sys
import os
import math
import random
import unittest
import datetime
import tempfile
import argparse

from flask import json, jsonify
from metadash import app, db

class BasicTestCase(unittest.TestCase):
    keep_data = False
    def setUp(self):
        if self.keep_data:
            return self.setUpDev()
        else:
            return self.setUpTest()

    def tearDown(self):
        if self.keep_data:
            return self.tearDownDev()
        else:
            return self.tearDownTest()

    def setUpDev(self):
        self.app = app.test_client()
        db.create_all()

    def tearDownDev(self):
        pass

    def setUpTest(self):
        (self.db_fd, self.db_fn) = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_fn
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDownTest(self):
        os.close(self.db_fd)
        os.unlink(self.db_fn)


class EmptyDBTest(BasicTestCase):
    def test_empty_db(self):
        rv = self.app.get('/')
        assert rv is not None
