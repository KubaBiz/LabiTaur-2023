# Tworzenie katalogu na dane dla pierwszego wywołania

from shutil import move
from os import mkdir

def makeDir():
    mkdir("data")

def moveData():
    move("icon.png", "data")
    move("requirements.txt", "data")
    move("hollow.py", "data")
    move("minotaur.png", "data")
    move("sword.png", "data")
    move("shield.png", "data")