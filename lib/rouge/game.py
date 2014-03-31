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
        self.log.set_level('INFO')

    def run(self):
        self.ui.run()

    def exit(self):
        self.ui.exit()

    directions = {
        'DIRECTION_N':  (0, -1),
        'DIRECTION_NE': (1, -1),
        'DIRECTION_E':  (1, 0),
        'DIRECTION_SE': (1, 1),
        'DIRECTION_S':  (0, 1),
        'DIRECTION_SW': (-1, 1),
        'DIRECTION_W':  (-1, 0),
        'DIRECTION_NW': (-1, -1),
    }
    def terrain_by_direction(self, d_x, d_y):
        player_x, player_y = self.current_map.player_pos
        dest_x, dest_y = player_x + d_x, player_y + d_y
        dest_terrain = self.current_map.at(dest_x, dest_y)
        return dest_terrain

    def keypress(self, key):
        command = self.key_to_command(key)
        if command:
            verb = command.lower()
            if command == "QUIT":
                self.exit()
            elif command.startswith("DIRECTION_"):
                direction = self.command_to_direction(command)
                dest_terrain = self.terrain_by_direction(*direction)
                if dest_terrain.can_receive('DEFAULT'):
                    verb, noun = dest_terrain.receive('DEFAULT')
                    self.log.info("You {} the {}.".format(verb, noun))
                else:
                    d_x, d_y = direction
                    player_x, player_y = self.current_map.player_pos
                    dest_x, dest_y = player_x + d_x, player_y + d_y
                    self.current_map.player_pos = dest_x, dest_y
            elif command in ["OPEN", "CLOSED"]:
                direction = self.prompt_direction(verb)
                if direction:
                    dest_terrain = self.terrain_by_direction(*direction)
                    if dest_terrain.can_receive(command):
                        verb, noun = dest_terrain.receive(command)
                        self.log.info("You {} the {}.".format(verb, noun))
                    else:
                        self.log.info("You cannot {} the {}.".format(verb, dest_terrain.name))
            else:
                self.log.error("Unhandled command: {}".format(command))
            self.ui.invalidate()

    def key_to_command(self, key):
        if key not in self.config.keymap:
            self.log.debug("Unmapped key: {}".format(key))
        return self.config.keymap.get(key, None)

    def command_to_direction(self, command):
        if command not in Game.directions:
            self.log.warn("Not a direction: {}".format(command))
        return Game.directions.get(command, None)

    def prompt_direction(self, verb):
        key = self.ui.prompt("Enter a direction to {}".format(verb))
        command = self.key_to_command(key)
        return self.command_to_direction(command)
