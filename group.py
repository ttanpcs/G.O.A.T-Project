class Group (object):
    def __init__ (self, color):
        self.color_ = color
        self.tile_array_ = []

    def __init__ (self, color, coordinates):
        self.color_ = color
        self.tile_array_ = []
        self.tile_array_.append(coordinates)

    def Add_Tile (self, coordinates):
        self.tile_array_.append(coordinates)

    def Get_Tiles(self):
        return tile_array_

    def Get_Size(self):
        return len(self.tile_array_)