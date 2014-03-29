import re

class Terrain(object):
    def __init__(self, char, name=None, flags=None):
        self.char = bytes(char, 'utf_8')
        self.name = name or char
        self.set_flags(flags)

    def set_flags(self, flags=None):
        flags = flags or []
        self.flags = {}
        for flag in flags:
            flag_arg = re.match('(.*)\[([^\]]*)\]', flag)
            if flag_arg:
                flag = flag_arg.group(1)
                flag_arg = flag_arg.group(2)
            else:
                flag_arg = True
            self.flags[flag] = flag_arg

    def get_flag(self, flag):
        return self.flags.get(flag, None)

    def toggle(self):
        toggles_to = self.get_flag('TOGGLE')
        if toggles_to:
            self.from_dict(self.terrain_by_id[toggles_to])
            return True
        else:
            return False

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
