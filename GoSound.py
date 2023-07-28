import subprocess

class GoSound():
    def __init__(self, dir_file_path = None, sound_type = "default"):
        if (dir_file_path is not None):
            self.dir_file_path = dir_file_path
        elif (sound_type == "default"):
            self.dir_file_path = "./resources/default"
        elif (sound_type == "pg"):
            self.dir_file_path = "./resources/pg"

    def playStartSound(self):
        subprocess.run(["aplay", self.dir_file_path + "/Start.wav"])

    def playCheatSound(self):
        subprocess.run(["aplay", self.dir_file_path + "/Cheat.wav"])

    def playWinSound(self):
        subprocess.run(["aplay", self.dir_file_path + "/Win.wav"])

    def playLoseSound(self):
        subprocess.run(["aplay", self.dir_file_path + "/Lose.wav"])
        
    def playEndSound(self):
        subprocess.run(["aplay", self.dir_file_path + "/End.wav"])

    def playPassSound(self):
        subprocess.run(["aplay", self.dir_file_path + "/Pass.wav"])