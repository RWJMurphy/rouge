from copy import copy
import os.path

import yaml

from rouge.map import Map
from rouge.ui import UrwidUI

class Game(object):
    def __init__(self, game_dir):
        game_yaml = os.path.join(game_dir, 'game.yml')
        config = {}
        with open(game_yaml, 'r') as game_yaml_fh:
            config = yaml.load(game_yaml_fh.read())['game']

        self.name = config['name']
        self.db = {}
        for key in ['terrains', 'objects', 'items', 'monsters']:
            self.db[key] = copy(config[key])

        self.maps = []
        for map in config['maps']:
            self.maps.append(Map.from_dict(map, self.db['terrains']))

        self.ui = UrwidUI(game=self)

    def run(self):
        self.ui.run()
