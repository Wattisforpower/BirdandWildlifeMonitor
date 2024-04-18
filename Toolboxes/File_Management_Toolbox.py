import os

class FileManagement:
    def __init__(self):
        pass

    def CopyAndRenameFile(self, src, dest, name):
        os.copyfile(src, f"{dest}/{name}")

