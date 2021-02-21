import enums

import numpy as np

class Board():
    def countNumPieces(self):
        self.num_pieces = 0
        for i in self.board:
            for j in i:
                if (j != enums.TileType.NO_TILE):
                    self.num_pieces += 1
                    
    def __init__(self, size = 19, board = None, num_pieces = 0):
        self.size = size
        if (board is not None):
            self.board = board
            if (num_pieces != 0):
                self.num_pieces = num_pieces
            else:
                self.countNumPieces()
        else:
            self.board = np.full((size, size), enums.TileType.NO_TILE, dtype = enums.TileType)
            self.num_pieces = 0
    
    def getSize(self):
        return self.size

    def setPiece(self, x, y, value):
        self.board[x][y] = value

    def getPiece(self, x, y):
        return self.board[x][y]

    def getBoard(self):
        return self.board
    
    def getNumPieces(self):
        return self.num_pieces