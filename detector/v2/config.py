import yaml
import os

class Config:

    def __init__(self):
        with open('config.yaml', 'r') as file:
            self._data = yaml.load(file, Loader=yaml.FullLoader)

    def get(self, key):
        if (key in self._data.keys()):
            return self._data[key]
        else:
            return None if os.getenv(key.upper()) is None else os.getenv(key.upper())