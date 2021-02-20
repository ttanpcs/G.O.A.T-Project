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
        subprocess.run(["aplay", self.dir_file_path + "/start.wav"])

    def playCheatSound(self):
        subprocess.run(["aplay", self.dir_file_path + "/cheat.wav"])

    def playWinSound(self):
        subprocess.run(["aplay", self.dir_file_path + "/win.wav"])

    def playLoseSound(self):
        subprocess.run(["aplay", self.dir_file_path + "/lose.wav"])
        
    def playEndSound(self):
        subprocess.run(["aplay", self.dir_file_path + "/end.wav"])

    def playPassSound(self):
        subprocess.run(["aplay", self.dir_file_path + "/pass.wav"])