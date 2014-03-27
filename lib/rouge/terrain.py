class Terrain(object):
    def __init__(self, char, name=None, flags=None):
        self.char = bytes(char, 'utf_8')
        self.name = name or char
        self.flags = flags or []

    def has_flag(self, flag):
        return flag in self.flags

    @staticmethod
    def from_dict(terrain_dict):
        terrain = Terrain(
            terrain_dict['char'],
            name=terrain_dict['name'],
            flags=terrain_dict.get('flags', [])
        )
        return terrain

    @staticmethod
    def from_char(char, terrains_by_id):
       return Terrain.from_dict(Terrain.by_char(terrains_by_id)[char])

    @staticmethod
    def null():
        t = Terrain(' ')
        return t

    _by_char = {}
    @staticmethod
    def by_char(terrains_by_id):
        if not Terrain._by_char:
            for terrain in terrains_by_id.values():
                Terrain._by_char[terrain['char']] = terrain
        return Terrain._by_char
