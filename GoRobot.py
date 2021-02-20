import GoCamera as gc
import GoModel as gm
import GoSound as gs
import time
import sys

def initialize(sound_type, board_size, board_offset, board_dimension):
    camera = gc.GoCamera()
    background_not_ready = True

    while (background_not_ready):
        current_response = input("Type \"r\" to take background photo...")
        if (current_response == "r"):
            background_not_ready = False

    background_photo = camera.capture()
    model = gm.GoModel(board_dimension, background_photo)
    sound = gs.GoSound(sound_type = sound_type)

    return camera, model, sound # arm, gameEngine

def main(sound_type, board_size, board_offset, board_dimension)):
    camera, model, sound = initialize(sound_type, board_size, board_offset, board_dimension) # arm, gameEngine
    game_ongoing = True # Change this later

    while (game_ongoing):
        time.sleep(15)
        current_response = input("Type \"p\" to pass (anything else to continue")
        if (current_response == "p"):
            # change the player 
        else:      
            current_image = camera.capture()
            current_board = model.readBoard(image) # ,the current player from gameEngine
            if (current_board is not None):
                # current_change_type = validateBoard(current_board)
                # if (current_change_type == ValidChange):
                #   Process_Turn()
                # elif (current_change_type == InvalidChange)
                # else: 
                #   print ("No change detected...") # DELETE LATER (Error Check # 2)
            else:
                print("Board is None") # DELETE LATER (Error Check # 1)



if __name__ == '__main__':
    bs = 0
    bo = 0
    bd = 19
    st = "."
    for i in len(sys.argv):
        if (sys.argv[i] == "--board_size" or sys.argv[i] == "-bs") and i + 1 < len(sys.argv):
            bs = sys.argv[i + 1]
        elif (sys.argv[i] == "--board_offset" or sys.argv[i] == "-bo") and i + 1 < len(sys.argv):
            bo = sys.argv[i + 1]
        elif (sys.argv[i] == "--sound_type" or sys.argv[i] == "-s") and i + 1 < len(sys.argv):
            st = sys.argv[i + 1]
        elif (sys.argv[i] == "--board_dimension" or sys.argv[i] == "-bd") and i + 1 < len(sys.argv):
            bd = sys.argv[i + 1]
    main(st, bs, bo, bd)
            