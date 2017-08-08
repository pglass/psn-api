import json
import os


class BaseCache(object):

    def get(self, key):
        pass

    def put(self, key, value):
        pass

    def rm(self, key):
        pass


class LocalCache(BaseCache):
    """A basic, tiny, thread UNSAFE local cache implementation"""

    def __init__(self, filename='psn.json'):
        self.filename = os.path.join(os.getcwd(), filename)
        self._write_file({})
        print 'Initialized cache file: %s' % self.filename

    def _load_file(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def _write_file(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def get(self, key):
        data = self._load_file()
        return data.get(key)

    def put(self, key, value):
        data = self._load_file()
        data[key] = value
        self._write_file(data)

    def rm(self, key):
        data = self._load_file()
        try:
            del data[key]
        except KeyError:
            pass
        self._write_file(data)
