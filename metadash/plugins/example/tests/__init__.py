import unittest
import json

from metadash.test.api import BasicTestCase


class ExampleTestCase(BasicTestCase):
    def test_empty_db(self):
        rv = self.app.get('/api/example/')
        data = json.loads(rv.data)
        assert len(data) == 1
        assert "name" in data[0].keys()
        assert "cached_function" in data[0].keys()
        assert "cached_property" in data[0].keys()
        assert data[0]["name"] == "Plugin: Hello, World!"


if __name__ == '__main__':
    unittest.main()
