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

    directions = {
        'N':  (0, -1),
        'NE': (1, -1),
        'E':  (1, 0),
        'SE': (1, 1),
        'S':  (0, 1),
        'SW': (-1, 1),
        'W':  (-1, 0),
        'NW': (-1, -1),
    }
    def keypress(self, key):
        if key in self.config.keymap:
            command = self.config.keymap[key]
            if command == "QUIT":
                self.exit()
            elif command.startswith("MOVE_"):
                direction = command[5:]
                d_x, d_y = Game.directions[direction]
                player_x, player_y = self.current_map.player_pos
                dest_x, dest_y = player_x + d_x, player_y + d_y
                dest_terrain = self.current_map.at(dest_x, dest_y)
                if dest_terrain.get_flag('TOGGLE'):
                    verb, old_name = dest_terrain.toggle()
                    self.log.info("You {} the {}.".format(verb, old_name))
                elif dest_terrain.get_flag('BLOCKS_MOVEMENT'):
                    self.log.info("You bump into the {}!".format(dest_terrain.name))
                else:
                    self.current_map.player_pos = dest_x, dest_y
            else:
                self.log.error("Unhandled command: {}".format(command))
            self.ui.invalidate()
        else:
            self.log.debug("Unhandled key: {}".format(key))
