class Terrain(object):
    def __init__(self):
        pass

    def from_dict(terrain_dict):
        t = Terrain()
        t.char = terrain_dict['char']
        return t

    def from_char(char, terrains_by_id):
       return Terrain.from_dict(Terrain.by_char(terrains_by_id)[char])

    _by_char = {}
    def by_char(terrains_by_id):
        if not Terrain._by_char:
            for terrain in terrains_by_id.values():
                Terrain._by_char[terrain['char']] = terrain
        return Terrain._by_char
