import unittest
import json

from metadash.test.api import BasicTestCase


class ExampleTestCase(BasicTestCase):
    def test_get(self):
        rv = self.app.get('/api/example/')
        data = json.loads(rv.data)
        assert len(data) == 1
        assert "name" in data[0].keys()
        assert "cached_function" in data[0].keys()
        assert "cached_property" in data[0].keys()
        assert data[0]["name"] == "Plugin: Hello, World!"

    def test_post(self):
        DATA = {
            "name": "Test Post: Hello, Word!"
        }
        rv = self.app.post('/api/example/', data=json.dumps(DATA),
                           content_type="application/json")
        data = json.loads(rv.data)

        self.assertDictContainsSubset(DATA, data)

    def test_get_config(self):
        rv = self.app.get('/api/configs/')
        data = json.loads(rv.data)
        self.assertTrue(any([
            conf['description'] == 'Example Config' and
            conf['key'] == 'EXAMPLE_CONFIG'
            for conf in data['data']
        ]))


if __name__ == '__main__':
    unittest.main()
