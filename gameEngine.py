import enums, constants, player, board, group

class GameEngine (object):
    def __init__ (self):
        self.black_player_ = player.Player(False)
        self.white_player_ = player.Player(False)
        self.current_player_ = self.black_player_
        self.current_player_tile_ = enums.TileType.BLACK_TILE
        self.other_player_tile_ = enums.TileType.WHITE_TILE
        self.board_queue_ = []
        self.group_array_ = []
        self.temp_group_array_ = []
        self.Initialize_Board_Queue

    def Initialize_Board_Queue (self):
        self.board_queue_.add(0, board.Board())
        self.board_queue_.add(0, board.Board())
        self.board_queue_.add(0, board.Board())

    def Validate_Board (self, new_board):
        self.Find_Current_Player_Tile
        self.board_queue_.add(0, new_board)
        difference_count = self.Count_Board_Differences()
        
        # easy invalid changes
        if difference_count[0] == 0:
            self.board_queue_.pop(0)
            return enums.ChangeType.NO_CHANGE # no new tiles
        elif difference_count[1] != 1:
            self.board_queue_.pop(0)
            return enums.ChangeType.INVALID_CHANGE # incorrect number of new tiles of current player
        elif difference_count[2] != 0:
            self.board_queue_.pop(0)
            return enums.ChangeType.INVALID_CHANGE # incorrect number of new tiles of other player
        elif difference_count[3] != 0:
            self.board_queue_.pop(0)
            return enums.ChangeType.INVALID_CHANGE # incorrect number of swapped tiles
        elif difference_count[4] != 0:
            self.board_queue_.pop(0)
            return enums.ChangeType.INVALID_CHANGE # incorrect number of removed tiles of current players

        if difference_count[5] > 0:
            if not self.Is_Valid_Removal():
                self.board_queue_.pop(0)
                return enums.ChangeType.INVALID_CHANGE

        new_piece = self.Find_New_Piece()
        self.Update_Groups(new_piece)
        #FINISH LATER
        
        self.board_queue_.pop(0)
        return enums.ChangeType.VALID_CHANGE
        
        
    def Is_Valid_Removal (self):
        current_board = self.board_queue_[0]
        removed_piece_array = self.Find_Removed_Pieces()
        if len(removed_piece_array) == 1:
            tile_coordinates = removed_piece_array[0]
            if not self.Check_Single_Piece_Removal(tile_coordinates):
                return False
        else:
            groups_to_check = []
            for tile in removed_piece_array:
                current_group = self.Find_Group_For_Piece(tile)
                if current_group.Get_Size == 1:
                    if not self.Check_Single_Piece_Removal(tile):
                        return False
                else:
                    is_group_already_seen = False
                    for group in groups_to_check:
                        if group == current_group:
                            is_group_already_seen = True
                    if not is_group_already_seen:
                        for group_tile in current_group:
                            is_in_removed_piece_array = False
                            for removed_tile in removed_piece_array:
                                if group_tile == removed_tile:
                                    is_in_removed_piece_array = True
                            if not is_in_removed_piece_array:
                                return False
                        groups_to_check.append(current_group)
            
            for group in groups_to_check:
                if not Check_Group_Removal (group):
                    return False

        return True

    def Check_Group_Removal (self, group):
        current_board = self.board_queue_[0]
        group_tiles = group.Get_Tiles
        for tile in group_tiles:
            tile_row, tile_col = tile
            if tile_row == 0:
                if current_board[tile_row + 1][tile_col] != self.current_player_tile_:
                    if current_board[tile_row + 1][tile_col] == enums.TileType.NO_TILE:
                        empty_tile_coordinates = (tile_row + 1, tile_col)
                        if not self.Is_Piece_Part_Of_Group(empty_tile_coordinates, group):
                            return False
                else:
                    return False
            elif tile_row == constants.GO_BOARD_LENGTH - 1:
                if current_board[tile_row - 1][tile_col] != self.current_player_tile_:
                     if current_board[tile_row - 1][tile_col] == enums.TileType.NO_TILE:
                        empty_tile_coordinates = (tile_row - 1, tile_col)
                        if not self.Is_Piece_Part_Of_Group(empty_tile_coordinates, group):
                            return False
                else:
                    return False
            else:
                if current_board[tile_row + 1][tile_col] != self.current_player_tile_:
                    if current_board[tile_row + 1][tile_col] == enums.TileType.NO_TILE:
                        empty_tile_coordinates = (tile_row + 1, tile_col)
                        if not self.Is_Piece_Part_Of_Group(empty_tile_coordinates, group):
                            return False
                else:
                    return False
                if current_board[tile_row - 1][tile_col] != self.current_player_tile_:
                     if current_board[tile_row - 1][tile_col] == enums.TileType.NO_TILE:
                        empty_tile_coordinates = (tile_row - 1, tile_col)
                        if not self.Is_Piece_Part_Of_Group(empty_tile_coordinates, group):
                            return False
                else:
                    return False

            if tile_col == 0:
                if current_board[tile_row][tile_col + 1] != self.current_player_tile_:
                    if current_board[tile_row][tile_col + 1] == enums.TileType.NO_TILE:
                        empty_tile_coordinates = (tile_row, tile_col + 1)
                        if not self.Is_Piece_Part_Of_Group(empty_tile_coordinates, group):
                            return False
                else:
                    return False
            elif tile_col == constants.GO_BOARD_LENGTH - 1:
                if current_board[tile_row][tile_col - 1] != self.current_player_tile_:
                     if current_board[tile_row][tile_col - 1] == enums.TileType.NO_TILE:
                        empty_tile_coordinates = (tile_row, tile_col - 1)
                        if not self.Is_Piece_Part_Of_Group(empty_tile_coordinates, group):
                            return False
                else:
                    return False
            else:
                if current_board[tile_row][tile_col + 1] != self.current_player_tile_:
                    if current_board[tile_row][tile_col + 1] == enums.TileType.NO_TILE:
                        empty_tile_coordinates = (tile_row, tile_col + 1)
                        if not self.Is_Piece_Part_Of_Group(empty_tile_coordinates, group):
                            return False
                else:
                    return False
                if current_board[tile_row][tile_col - 1] != self.current_player_tile_:
                     if current_board[tile_row][tile_col - 1] == enums.TileType.NO_TILE:
                        empty_tile_coordinates = (tile_row, tile_col - 1)
                        if not self.Is_Piece_Part_Of_Group(empty_tile_coordinates, group):
                            return False
                else:
                    return False

        return True

    def Check_Single_Piece_Removal (self, coordinates):
        current_board = self.board_queue_[0]
        tile_row, tile_col = coordinates
        if tile_row == 0:
            if current_board[tile_row + 1][tile_col] != self.other_player_tile_:
                return False
        elif tile_row == constants.GO_BOARD_LENGTH - 1:
            if current_board[tile_row - 1][tile_col] != self.other_player_tile_:
                return False
        else:
            if current_board[tile_row + 1][tile_col] != self.other_player_tile_ and current_board[tile_row - 1][tile_col] != self.other_player_tile_:
                return False

        if tile_col == 0:
            if current_board[tile_row][tile_col + 1] != self.other_player_tile_:
                return False
        elif tile_col == constants.GO_BOARD_LENGTH - 1:
            if current_board[tile_row][tile_col - 1] != self.other_player_tile_:
                return False
        else:
            if current_board[tile_row][tile_col + 1] != self.other_player_tile_ and current_board[tile_row][tile_col - 1] != self.other_player_tile_:
                return False

        return True

    def Find_Removed_Pieces (self):
        current_board = self.board_queue_[0]
        previous_board = self.board_queue_[1]
        removed_piece_array = []

        for row in range(constants.GO_BOARD_LENGTH):
            for col in range(constants.GO_BOARD_LENGTH):
                current_tile = current_board[row][col]
                if current_tile == enums.TileType.NO_TILE:
                    previous_tile = previous_board[row][col]
                    if previous_tile == self.other_player_tile_:
                        coordinates = (row, col)
                        removed_piece_array.append(coordinates)

        return removed_piece_array

    def Find_New_Piece (self):
        current_board = self.board_queue_[0]
        previous_board = self.board_queue_[1]

        for row in range(constants.GO_BOARD_LENGTH):
            for col in range(constants.GO_BOARD_LENGTH):
                previous_tile = previous_board[row][col]
                if previous_tile == enums.TileType.NO_TILE:
                    current_tile = current_board[row][col]
                    if current_tile == self.current_player_tile_:
                        coordinates = (row, col)
                        return coordinates

    def Update_Groups (self, new_piece):
        self.temp_group_array_ = self.group_array_
        #FINISH LATER

    def Find_Group_For_Piece (self, coordinates):
        for group in self.group_array_:
            group_tiles = group.Get_Tiles()
            for tile in group_tiles:
                if tile == coordinates:
                    return group

    def Is_Piece_Part_Of_Group (self, coordinates, group):
        current_group = Find_Group_For_Piece (coordinates)
        return current_group == group

    def Process_Turn (self, new_board):
        # add new board to queue and remove old board
        self.board_queue_.add(0, new_board)
        self.board_queue_.pop()

        self.group_array_ = self.temp_gorup_array_

        self.Update_Board_State()

        self.Swap_Current_Player()

        self.Find_Possible_Moves(self.current_player_)

        # AI take turn
        if self.current_player_.Is_AI():
            #self.current_player_.Take_Turn
            self.current_player_.Take_Random_Turn(board_queue_[0])

    def Update_Board_State (self):
        #FINISH LATER
        pass

    def Find_Possible_Moves (self, player):
        #FINISH LATER
        pass

    def Count_Board_Differences (self):
        current_board = self.board_queue_[0]
        previous_board = self.board_queue_[1]

        # difference_count [total (0), current new (1), other new (2), swapped (3), current removed (4), other removed (5)]
        difference_count = []
        for x in range(6):
            difference_count.append(0)
        
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
            self.other_player_tile_ = enums.TileType.WHITE_TILE
        else:
            self.current_player_tile_ = enums.TileType.WHITE_TILE
            self.other_player_tile_ = enums.TileType.BLACK_TILE

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
