from copy import copy

import yaml

from rouge.containers import AttrDict
from rouge.map import Map

def invert(dictionary):
    return {v: k for k, vl in dictionary.items() for v in vl}

class Config:
    def __init__(self, game_yaml):
        with open(game_yaml, 'r') as game_yaml_fh:
            self.config = AttrDict(yaml.load(game_yaml_fh.read())['game'])

        self.name = self.config['name']
        self.db = {}
        for key in ['terrains', 'objects', 'items', 'monsters']:
            self.db[key] = copy(self.config[key])

        self.maps = []
        for map in self.config['maps']:
            self.maps.append(Map.from_dict(map, self.db['terrains']))
        self.keymap = invert(self.config.keymap)
