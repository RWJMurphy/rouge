class Terrain(object):
    def __init__(self, char):
        self.char = bytes(char, 'utf_8')

    @staticmethod
    def from_dict(terrain_dict):
        t = Terrain(terrain_dict['char'])
        return t

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
