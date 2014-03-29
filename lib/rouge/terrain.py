import re

from rouge.containers import AttrDict

class Terrain(object):
    def __init__(self, char, name=None, flags=None, receivers=None):
        self.char = bytes(char, 'utf_8')
        self.name = name or char
        self.set_flags(flags)
        self.set_receivers(receivers)

    def from_dict(self, terrain_dict):
        self.__init__(
            terrain_dict['char'],
            name=terrain_dict['name'],
            flags=terrain_dict.get('flags', {}),
            receivers=terrain_dict.get('receives', {}),
        )
        return self

    def set_flags(self, flags=None):
        flags = flags or {}
        self.flags = {}
        for flag, arg in flags.items():
            if arg is None:
                arg = {}
            self.flags[flag] = AttrDict(arg)

    def set_receivers(self, receivers=None):
        receivers = receivers or {}
        self.receivers = {}
        for message, args in receivers.items():
            self.receivers[message] = self.build_receiver(message, args)

    def build_receiver(self, message, args={}):
        if message in ["OPEN", "CLOSE"]:
            def toggle():
                old_name = self.name
                self.become(args['becomes'])
                return args['verb'], old_name
            return toggle
        elif message == "BLOCKS_MOVEMENT":
            def block_movement():
                return "bump into", self.name
            return block_movement
        elif message == "DEFAULT":
            def default():
                return self.receive(args['as'])
            return default
        return None

    def can_receive(self, message):
        return message in self.receivers

    def receive(self, message):
        return self.receivers[message]()

    def get_flag(self, flag):
        return self.flags.get(flag, None)

    def become(self, other_id):
        self.from_dict(self.terrain_by_id[other_id])

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
