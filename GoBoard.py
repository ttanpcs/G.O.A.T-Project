# This class will likely be deleted/modified in the future
import numpy as np

class GoBoard():
    def countNumPieces(self):
        self.num_pieces = 0
        for i in self.board:
            for j in i:
                if (j != 0):
                    self.num_pieces += 1

    def __init__(self, size = 19, board = None, num_pieces = 0):
        if (board is not None):
            self.board = board
            if (num_pieces != 0):
                self.num_pieces = num_pieces
            else:
                self.countNumPieces()
        else:
            self.board = np.zeros((size, size), dtype = int)
            self.num_pieces = 0

    def setPiece(self, x, y, value):
        self.board[x][y] = value

    def getPiece(self, x, y):
        return self.board[x][y]

    def getBoard(self):
        return self.board
    
    def getNumPieces(self):
        return self.num_pieces