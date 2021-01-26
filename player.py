from abc import ABC, abstractmethod

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

    def Update_Possible_Moves(self, new_moves):
        self.possible_moves_ = new_moves