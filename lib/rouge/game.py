from copy import copy
import os.path

import yaml

from rouge.config import Config
from rouge.map import Map
from rouge.ui import UrwidUI as UI
from rouge.log import UrwidLog as Log

class Game(object):
    def __init__(self, game_dir):
        game_yaml = os.path.join(game_dir, 'game.yml')
        self.config = Config(game_yaml)
        self.current_map = self.config.maps[0]
        self.ui = UI(self)
        self.log = Log(self.ui)

    def run(self):
        self.ui.run()

    def exit(self):
        self.ui.exit()

    def keypress(self, key):
        if key in self.config.keymap:
            command = self.config.keymap[key]
            if command == "QUIT":
                self.exit()
        else:
            self.log.debug("Unhandled key: {}".format(key))
