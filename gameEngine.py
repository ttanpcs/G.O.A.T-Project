import enums, constants, player, board

class GameEngine (object):
    def __init__ (self):
        self.black_player_ = player.Player(False)
        self.white_player_ = player.Player(False)
        self.current_player_ = self.black_player_
        self.current_player_tile_ = enums.TileType.BLACK_TILE
        self.board_queue_ = []
        self.Initialize_Board_Queue

    def Initialize_Board_Queue (self):
        self.board_queue_.add(0, board.Board())
        self.board_queue_.add(0, board.Board())
        self.board_queue_.add(0, board.Board())

    def Validate_Board (self, new_board):
        self.Find_Current_Player_Tile
        difference_count = self.Count_Board_Differences
        
        # easy invalid changes
        if difference_count[0] == 0:
            return enums.ChangeType.NO_CHANGE # no new tiles
        elif difference_count[1] != 1:
            return enums.ChangeType.INVALID_CHANGE # incorrect number of new tiles of current player
        elif difference_count[2] != 0:
            return enums.ChangeType.INVALID_CHANGE # incorrect number of new tiles of other player
        elif difference_count[3] != 0:
            return enums.ChangeType.INVALID_CHANGE # incorrect number of swapped tiles
        elif difference_count[4] != 0:
            return enums.ChangeType.INVALID_CHANGE # incorrect number of removed tiles of current players

        # check if new pieces are within the player's possible moves

        # check if removed pieces should have been removed

        # check if there are pieces that were not removed that should have been removed

        return enums.ChangeType.VALID_CHANGE
        
        

    def Process_Turn (self, new_board):
        # add new board to queue and remove old board
        self.board_queue_.add(0, new_board)
        self.board_queue_.pop()

        self.Swap_Current_Player()

        self.Find_Possible_Moves(self.current_player_)

        # AI take turn
        if self.current_player_.Is_AI:
            self.current_player_.Take_Turn

    def Find_Possible_Moves (self, player):
        pass

    def Count_Board_Differences (self):
        current_board = self.board_queue_[0]
        previous_board = self.board_queue_[1]

        # difference_count [total (0), current new (1), other new (2), swapped (3), current removed (4), other removed (5)]
        difference_count = []
        for x in range(6):
            difference_count.add(0)
        
        for row in range(constants.GO_BOARD_LENGTH):
            for col in range(constants.GO_BOARD_LENGTH):
                current_tile = current_board[row][col]
                if current_tile == previous_board[row][col]:
                    break
                else:
                    difference_count[0] += 1 # total
                    previous_tile = previous_board[row][col]
                    if previous_tile == enums.TileType.NO_TILE:
                        if current_tile == self.current_player_tile_:
                            difference_count[1] += 1 # current new
                        else:
                            difference_count[2] += 1 # other new
                    elif previous_tile != enums.TileType.NO_TILE and current_tile != enums.TileType.NO_TILE:
                        difference_count[3] += 1 # swapped
                    elif previous_tile == self.current_player_tile_:
                        difference_count[4] += 1 # current removed
                    else:
                        difference_count[5] += 1 # other removed
        
        return difference_count

    def Find_Current_Player_Tile(self):
        if self.current_player_ == self.black_player_:
            self.current_player_tile_ = enums.TileType.BLACK_TILE
        else:
            self.current_player_tile_ = enums.TileType.WHITE_TILE

    def Take_Turn_Override(self):
        if self.current_player_.Is_AI:
            self.current_player_.Take_Turn
        else:
            self.Swap_Current_Player()

    def Swap_Current_Player(self):
        if self.current_player_ == self.black_player_:
            self.current_player_ = self.white_player_
        else:
            self.current_player_ = self.black_player_

