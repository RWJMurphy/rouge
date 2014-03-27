import collections

from rouge.terrain import Terrain

class TerrainRow(collections.MutableSequence):
    @classmethod
    def null(cls):
        return cls([])

    def __init__(self, terrain_iter):
        self._row = [t for t in terrain_iter]

    def __getitem__(self, i):
        if i < 0 or i >= len(self._row):
            return Terrain.null()
        else:
            return self._row[i]

    def __setitem__(self, i, value):
        self._row[i] = value

    def __delitem__(self, i):
        del self._row[i]

    def __len__(self):
        return len(self._row)

    def insert(self, where, value):
        return self._row.insert(where, value)

class Map(object):
    def __init__(self):
        self.terrain = []
        self.objects = []
        self.player_pos = (None, None)

    @staticmethod
    def from_dict(map_dict, terrains):
        the_map = Map()
        for line in map_dict['terrain']:
            row = []
            the_map.terrain.append(row)
            for c in line:
                row.append(Terrain.from_char(c, terrains))
        the_map.player_pos = map_dict['spawn']
        return the_map

    def at(self, x, y):
        if y < 0:
            row = TerrainRow.null()
        else:
            try:
                row = TerrainRow(self.terrain[y])
            except IndexError:
                row = TerrainRow.null()

        return row[x]
    
    def __str__(self):
        return "\n".join([''.join([t.char for t in row]) for row in self.terrain])
