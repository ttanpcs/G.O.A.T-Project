class Group (object):
    def __init__ (self, color):
        self.color_ = color
        self.tile_array_ = []

    def Add_Tile (self, coordinates):
        self.tile_array_.add(coordinates)

    def Get_Tiles(self):
        return tile_array_