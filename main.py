# Uruchamianie programu

from os import path

if not path.exists(".\\data"):
    import installer
    installer.makeDir()
    installer.moveData()

import gui


def main():
    Game = gui.Application("start_menu")
    Game.run()


if __name__ == "__main__":
    main()
    