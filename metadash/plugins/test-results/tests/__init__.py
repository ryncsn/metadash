#!/bin/env python
import argparse
import random
import datetime
import json

from metadash.test.api import BasicTestCase

NAME_CANDIDATE = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'iota', 'kappa', 'lambda']
FUNCTION_CANDIDATE = ['compress', 'extract', 'erase', 'install', 'revert', 'delete', 'copy']

MOCK_TESTRECORDS_NUMBER = 5
MOCK_TESTCASE_NUMBER = 10


def random_name(prefix,
                random_token_candidates,
                length=3,
                delim='_'):
    return "{}{}{}".format(prefix, delim, delim.join([random.choice(random_token_candidates) for _ in range(length)]))


class FixtureTest(BasicTestCase):
    keep_data = False

    def test_testrun_submitting(self):
        for i in range(MOCK_TESTRECORDS_NUMBER):
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
            print('Testrun created %s' % i)

            testrun_rv = self.app.post('/api/testruns/', data=json.dumps(
                testrun_data
            ), content_type='application/json')
            if isinstance(testrun_rv.data, bytes):
                testrun_rv_data = json.loads(testrun_rv.data.decode('utf-8'))
            else:
                testrun_rv_data = json.loads(str(testrun_rv.data))
            assert testrun_rv_data['uuid']

            for key in testrun_data:
                assert testrun_rv_data[key] == testrun_data[key]

            testcase_names = list(set([random_name("testcase", FUNCTION_CANDIDATE, 3) for i in range(random.randrange(MOCK_TESTCASE_NUMBER))]))
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
                if isinstance(testresult_rv.data, bytes):
                    testresult_rv_data = json.loads(testresult_rv.data.decode('utf-8'))
                else:
                    testresult_rv_data = json.loads(str(testresult_rv.data))
                assert testresult_rv_data['uuid']
                for key in testresult_data:
                    assert testresult_rv_data[key] == testresult_data[key]


if __name__ == '__main__':
    test = FixtureTest("test_testrun_submitting")
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--testrun-count', type=int, default=20,
                        help='How many mock record to generate')
    parser.add_argument('--testcase-per-testrun', type=int, default=50,
                        help='Size of each mock record')
    args = parser.parse_args()

    MOCK_TESTCASE_NUMBER = args.testcase_per_testrun
    MOCK_TESTRECORDS_NUMBER = args.testrun_count

    FixtureTest.keep_data = True

    test.debug()
