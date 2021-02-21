import GoCamera as gc
import GoModel as gm
import GoSound as gs
import gameEngine as ge
import player
import time
import enums
import sys

def playSound(is_black_turn, bp_is_ai, wp_is_ai, sound, sound_function):
    if ((is_black_turn and bp_is_ai) or ((not is_black_turn) and wp_is_ai)):
        sound_function(sound)

def findPlayerMapping(player_type, tile_type):
    if (player_type == "human_player"):
        return player.HumanPlayer(False, tile_type)
    elif (player_type == "random_ai_player"):
        return player.RandomAIPlayer(True, tile_type)

def initialize(sound_type, board_size, board_offset, board_dimension, black_player, white_player):
    camera = gc.GoCamera()
    background_not_ready = True
    white_player_type = findPlayerMapping(white_player, enums.TileType.WHITE_TILE) # Could be really cancer if pointers
    black_player_type = findPlayerMapping(black_player, enums.TileType.BLACK_TILE) # Could be really cancer if pointers
    background_photo = camera.capture()
    model = gm.GoModel(board_dimension, background_photo)
    sound = gs.GoSound(sound_type = sound_type)
    engine = ge.GameEngine(black_player_type, white_player_type, board_size)

    return camera, model, sound, engine # arm, 

def main(sound_type, board_size, board_offset, board_dimension, black_player, white_player):
    camera, model, sound, engine = initialize(sound_type, board_size, board_offset, board_dimension, black_player, white_player) # arm, gameEngine
    game_ongoing = True 
    is_black_turn = False
    black_passed = False
    white_passed = False
    # sound.playStartSound()
    print("Start")

    while (game_ongoing):
        if (black_passed and white_passed):
            game_ongoing = False
            # Figure out who won and do smth.... 
        else:      
            time.sleep(15)
            current_image = camera.capture()
            if (engine.Get_Current_Player_Tile == enums.TileType.BLACK_TILE):
                is_black_turn = True
            else:
                is_black_turn = False
            current_board = model.readBoard(current_image, is_black_turn)
            print(current_board)
            if (current_board is not None):
                current_change_type = engine.Validate_Board(current_board)
                if (current_change_type == enums.ChangeType.VALID_CHANGE):
                    coordinates = None
                    if (is_black_turn):
                        black_passed, coordinates = engine.Process_Turn(current_board)
                        if (black_passed):
                            # playSound(is_black_turn, ge.Is_Black_Player_AI(), ge.IsWhite_Player_AI(), sound, gs.GoSound.playPassSound)
                            print("black passed")
                        else:    
                            # playSound(is_black_turn, ge.Is_Black_Player_AI(), ge.IsWhite_Player_AI(), sound, gs.GoSound.playEndSound)
                            print("black end")
                    else:
                        white_passed, coordinates = engine.Process_Turn(current_board)
                        if (white_passed):
                            # playSound(is_black_turn, ge.Is_Black_Player_AI(), ge.IsWhite_Player_AI(), sound, gs.GoSound.playPassSound)
                            print("white passed")
                        else:    
                            # playSound(is_black_turn, ge.Is_Black_Player_AI(), ge.IsWhite_Player_AI(), sound, gs.GoSound.playEndSound)
                            print("white end")
                    print(coordinates) # DELETE LATER (Error Check # 4)
                elif (current_change_type == enums.ChangeType.INVALID_CHANGE):
                    print ("Invalid change detected") # DELETE LATER (Error Check # 3)
                    # playSound(is_black_turn, ge.Is_Black_Player_AI(), ge.IsWhite_Player_AI(), sound, gs.GoSound.playCheatSound)
                else: 
                    print ("No change detected") # DELETE LATER (Error Check # 2)
            else:
                print("Board is None according to vision") # DELETE LATER (Error Check # 1)
                # model.showBoard(current_image) # DELETE LATER (Error Check # 1.1)

if __name__ == '__main__':
    bs = 0
    bo = 0
    bd = 19
    st = "default"
    white_player = "random_ai_player"
    black_player = "human_player"

    for i in range(len(sys.argv)):
        if (sys.argv[i] == "--board_size" or sys.argv[i] == "-bs") and i + 1 < len(sys.argv):
            bs = sys.argv[i + 1]
        elif (sys.argv[i] == "--board_offset" or sys.argv[i] == "-bo") and i + 1 < len(sys.argv):
            bo = sys.argv[i + 1]
        elif (sys.argv[i] == "--sound_type" or sys.argv[i] == "-s") and i + 1 < len(sys.argv):
            st = sys.argv[i + 1]
        elif (sys.argv[i] == "--board_dimension" or sys.argv[i] == "-bd") and i + 1 < len(sys.argv):
            bd = sys.argv[i + 1]
        elif (sys.argv[i] == "--white_player" or sys.argv[i] == "-wp") and i + 1 < len(sys.argv):
            white_player = sys.argv[i + 1]
        elif (sys.argv[i] == "--black_player" or sys.argv[i] == "-bp") and i + 1 < len(sys.argv):
            black_player = sys.argv[i + 1]

    main(st, bs, bo, bd, black_player, white_player)