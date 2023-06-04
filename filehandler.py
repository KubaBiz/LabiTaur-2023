# Zapisywanie i odczytywanie pliku

def newfile(length: int):
    file = open(".\\data\\save.txt", "w") 

    file.write("0\n") 
    file.write("0\n")
    file.write("0\n")
    file.write("0\n")
    file.write("0\n")
    upgrades = ""
    for _ in range(length):
        upgrades += "00"
    upgrades += "\n"
    file.write(upgrades)

    file.close() 


def savefile(
        money: int,
        difficulty: int,
        statistics: list[int],
        upgrades: dict):
    file = open(".\\data\\save.txt", "w") 

    file.write(str(money) + "\n") 
    file.write(str(difficulty) + "\n")

    file.write(str(statistics[0]) + "\n")
    file.write(str(statistics[1]) + "\n")
    file.write(str(statistics[2]) + "\n")
    line = ""
    # str.format
    for _, upgrade in upgrades.items(): 
        temp = str(upgrade)
        if len(temp) == 1:
            temp = "0" + temp
        line += temp
    line += "\n"
    file.write(line)

    file.close() 


def readfile():
    try:
        file = open(".\\data\\save.txt", "r") 

        statistics = []
        money = int(file.readline()) 
        difficulty = int(file.readline())
        statistics.append(int(file.readline()))
        statistics.append(int(file.readline()))
        statistics.append(int(file.readline()))
        line = file.readline()

        upgrades_temp = []
        for i in range(len(line) // 2):
            upgrades_temp.append(int(line[2 * i:2 * i + 2]))

        upgrades = {
            "trap_chance": 0, 
            "lootrooms": 0, 
            "traps": 0, 
            "die_chance": 0, 
            "thread_chance": 0, 
            "torch_time": 0}     
        i = 0
        for keys in upgrades:
            upgrades[keys] = upgrades_temp[i]
            i += 1
    except ValueError:
        print("Corrupted File, starting new game with normal difficulty")
        return 0, 0, [0, 0, 0], {"trap_chance": 0, "lootrooms": 0, 
                                 "traps": 0, "die_chance": 0, "thread_chance": 0, "torch_time": 0}
    finally:
        file.close()

    return money, difficulty, statistics, upgrades
