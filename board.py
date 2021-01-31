import enums, constants

class Board (object):
    def __init__ (self):
        self.board_tiles_ = [[enums.TileType.NO_TILE] * constants.GO_BOARD_LENGTH] * constants.GO_BOARD_LENGTH

    def Find_Tile (self, x, y):
        return self.board_tiles_[x][y]

    def Set_Tile (self, x, y, tile_type):
        self.board_tiles_[x][y] = tile_type