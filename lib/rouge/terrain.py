import re

from rouge.containers import AttrDict

class Terrain(object):
    def __init__(self, char, name=None, flags=None):
        self.char = bytes(char, 'utf_8')
        self.name = name or char
        self.set_flags(flags)

    def set_flags(self, flags=None):
        flags = flags or {}
        self.flags = {}
        for flag, arg in flags.items():
            if arg is None:
                arg = {}
            self.flags[flag] = AttrDict(arg)

    def get_flag(self, flag):
        return self.flags.get(flag, None)

    def toggle(self):
        toggle = self.get_flag('TOGGLE')
        if toggle:
            old_name = self.name
            self.from_dict(self.terrain_by_id[toggle.to])
            return toggle.verb, old_name
        else:
            return None, None

    @classmethod
    def load_definitions(cls, terrain_dict):
        cls.terrain_by_id = terrain_dict
        cls.terrain_by_char = cls.by_char(terrain_dict)

    def from_dict(self, terrain_dict):
        self.__init__(
            terrain_dict['char'],
            name=terrain_dict['name'],
            flags=terrain_dict.get('flags', [])
        )
        return self

    @classmethod
    def from_char(cls, char):
        assert(cls.terrain_by_char is not None)
        return cls.null().from_dict(cls.terrain_by_char[char])

    @classmethod
    def from_id(cls, terrain_id):
        assert(cls.terrain_by_id is not None)
        return cls.null().from_dict(cls.terrain_by_id[terrain_id])

    @classmethod
    def null(cls):
        return cls(' ')

    @staticmethod
    def by_char(terrains_by_id):
        by_char = {}
        for terrain in terrains_by_id.values():
            by_char[terrain['char']] = terrain
        return by_char
