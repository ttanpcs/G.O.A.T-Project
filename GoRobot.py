import GoCamera as gc
import GoModel as gm
import GoSound as gs
import time
import sys

def findPlayerMapping(player_type):
    if (player_type == "human_player"):
        return ... # Wtvr its called
    elif (player_type == "random_ai_player"):
        return ... # Wtvr its called 

def initialize(sound_type, board_size, board_offset, board_dimension, black_player, white_player):
    camera = gc.GoCamera()
    background_not_ready = True
    white_player_type = findPlayerMapping(white_player) # Could be really cancer if pointers
    black_player_type = findPlayerMapping(black_player) # Could be really cancer if pointers
    background_photo = camera.capture()
    model = gm.GoModel(board_dimension, background_photo)
    sound = gs.GoSound(sound_type = sound_type)

    return camera, model, sound # arm, gameEngine

def main(sound_type, board_size, board_offset, board_dimension, black_player, white_player):
    camera, model, sound = initialize(sound_type, board_size, board_offset, board_dimension, black_player, white_player) # arm, gameEngine
    game_ongoing = True 
    black_passed = False
    white_passed = False

    while (game_ongoing):
        if (black_passed and white_passed): # this comes from the tuple of Player take_turn.
            game_ongoing = False
            # Figure out who won and do smth.... 
        else:      
            time.sleep(15)
            current_image = camera.capture()
            current_board = model.readBoard(current_image) # ,the current player from gameEngine
            if (current_board is not None):
                # current_change_type = validateBoard(current_board)
                # if (current_change_type == ValidChange):
                #   Process_Turn()
                # elif (current_change_type == InvalidChange)
                # else: 
                #   print ("No change detected from ") # DELETE LATER (Error Check # 2)
            else:
                print("Board is None according to vision") # DELETE LATER (Error Check # 1)
                model.showBoard(current_image) # DELETE LATER (Error Check # 1.1)

if __name__ == '__main__':
    bs = 0
    bo = 0
    bd = 19
    st = "."
    white_player = "random_ai_player"
    black_player = "human_player"

    for i in len(sys.argv):
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