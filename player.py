from abc import ABC, abstractmethod
import random
import board
import numpy as np
import enums

class Player (ABC):
    def __init__ (self, is_AI, tile_type):
        self.is_AI_ = is_AI
        self.tyle_type = tile_type

    def Is_AI (self):
        return self.is_AI_

    @abstractmethod
    def Take_Turn (self, board):
        pass

class HumanPlayer (Player):
    def Take_Turn (self, board):
        print("-----------------------------------------------------")
        current_input = input("Type \"p\" to pass: ")
        if (current_input == "p"):
            return True, None
        else:
            return False, None

class RandomAIPlayer (Player):
    def Take_Turn (self, board):
        random.seed()
        x = random.randint(0, board.getSize())
        y = random.randint(0, board.getSize())

        while (board.getPiece(x, y) != enums.TileType.NO_TILE):
            x = random.randint(0, constants.GO_BOARD_LENGTH)
            y = random.randint(0, constants.GO_BOARD_LENGTH)
        
        will_pass = random.randint(0, 30) # Note That these numbers are chosen randomly
        if (will_pass == 1):
            return True, np.array([x, y])
        return False, np.array([x, y])