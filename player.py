from abc import ABC, abstractmethod
import random
import constants, enums

class Player (ABC):
    def __init__ (self, is_AI):
        self.is_AI_ = is_AI
        self.possible_moves_ = [[True] * 19] * 19
        self.captured_pieces_ = 0

    def Is_AI (self):
        return self.is_AI_

    def Take_Turn(self):
        """
        Potential AI stuff goes here.
        """
        pass

    def Take_Random_Turn (self, board):
        random.seed()
        x = random.randint(0, constants.GO_BOARD_LENGTH)
        y = random.randint(0, constants.GO_BOARD_LENGTH)
        while (board.Find_Tile(x, y) != enums.TileType.NO_TILE):
            x = random.randint(0, constants.GO_BOARD_LENGTH)
            y = random.randint(0, constants.GO_BOARD_LENGTH)
        
        coords = (x, y)
        return coords

        

    def Update_Possible_Moves(self, new_moves):
        self.possible_moves_ = new_moves