#!/bin/env python
import os
import random
import datetime
import unittest
import tempfile
import json

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
        with app.app_context():
            db.create_all()

    def tearDownDev(self):
        pass

    def setUpTest(self):
        (self.db_fd, self.db_fn) = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_fn
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDownTest(self):
        os.close(self.db_fd)
        os.unlink(self.db_fn)


NAME_CANDIDATE = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'iota', 'kappa', 'lambda']
FUNCTION_CANDIDATE = ['compress', 'extract', 'erase', 'install', 'revert', 'delete', 'copy']


def random_name(prefix,
                candidates,
                length=3,
                delim='_'):
    return "{}{}{}".format(prefix, delim, delim.join([random.choice(candidates) for _ in range(length)]))


class FixtureTest(BasicTestCase):
    keep_data = True

    def generate_legal_testruns(self):
        for i in range(150):
            testrun_name = random_name("testrun", NAME_CANDIDATE)
            testrun_data = {
                "name": testrun_name,
                "ref_url": "#" + testrun_name + datetime.datetime.now().isoformat(),
                "details": {
                    "console": (
                        "\033[94mINFO\033[0m: Hello world!\n"
                        "\033[93mWARN\033[0m: Warning!\n"
                        "\033[91mERROR\033[0m: Nothing went wrong, but still giving an error.!\n"
                    ) * 300,
                },
                "properties": {
                    "build": random_name("release", "123456789", 1),
                    "component": random.choice(["python-api", "c-api", "web-api", "java-api"]),
                    "arch": random.choice(["x86_64", "i386", "ppc64le", "arm"]),
                    "type": random.choice(["function1", "function2", "acceptance", "installation"]),
                    "sub_type": random.choice(["windows", "centos", "debian", "suse"]),
                },
                "status": "FINISHED",
            }

            testrun_rv = self.app.post('/api/testruns/', data=json.dumps(
                testrun_data
            ), content_type='application/json')
            testrun_rv_data = json.loads(testrun_rv.data)
            assert testrun_rv_data['uuid']
            for key in testrun_data:
                assert testrun_rv_data[key] == testrun_data[key]

            print("Testrun Created")
            testcase_names = list(set([random_name("testcase", FUNCTION_CANDIDATE, 3) for i in range(random.randrange(200))]))
            for testcase_name in testcase_names:
                testresult_data = {
                    "testrun_uuid": testrun_rv_data['uuid'],
                    "testcase_name": testcase_name,
                    "result": random.choice(["PASSED"] * 100 + ["FAILED"] * 5 + ["SKIPPED"] * 3),
                    "duration": random.random() * 10,
                    "ref_url": "#/" + testrun_rv_data['uuid'] + "/" + testcase_name,
                }
                testresult_rv = self.app.post('/api/testresults/', data=json.dumps(
                    testresult_data), content_type='application/json')
                testresult_rv_data = json.loads(testresult_rv.data)
                print(testresult_rv_data)
                assert testresult_rv_data['uuid']
                for key in testresult_data:
                    assert testresult_rv_data[key] == testresult_data[key]


if __name__ == '__main__':
    test = FixtureTest("generate_legal_testruns")
    test.debug()
