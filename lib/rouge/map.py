from rouge.terrain import Terrain

class Map(object):
    def __init__(self):
        self.terrain = []

    def from_dict(map_dict, terrains):
        the_map = Map()
        for line in map_dict['terrain']:
            row = []
            the_map.terrain.append(row)
            for c in line:
                row.append(Terrain.from_char(c, terrains))
        return the_map
    
    def __str__(self):
        return "\n".join([''.join([t.char for t in row]) for row in self.terrain])
