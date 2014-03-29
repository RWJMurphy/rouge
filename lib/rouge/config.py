from copy import copy

import yaml

from rouge.containers import AttrDict
from rouge.map import Map
from rouge.terrain import Terrain

def invert(dictionary):
    return {v: k for k, vl in dictionary.items() for v in vl}

class Config:
    def __init__(self, game_yaml):
        with open(game_yaml, 'r') as game_yaml_fh:
            self.config = AttrDict(yaml.load(game_yaml_fh.read())['game'])

        self.name = self.config['name']
        self.db = AttrDict()
        for key in ['terrains', 'entities', 'items', 'monsters']:
            self.db[key] = self.config[key]
        Terrain.load_definitions(self.db['terrains'])

        self.maps = []
        for map in self.config['maps']:
            self.maps.append(Map.from_dict(map))
        self.keymap = invert(self.config.keymap)
