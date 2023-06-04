# Generacja mapy
import random


class Room():
    def __init__(self):
        self.state = 0
        self.visited = False
        self.interacted = False
        self.generated = False
 
    def reset(self):
        self.state = 0
        self.visited = False
        self.interacted = False
        self.generated = False


class Map():
    def __init__(self):
        self.matrix = [[Room() for _ in range(12)] for _ in range(12)]
        self.playerposition = [None, 11]

    def set_generation(self, upgrades: dict):
        self.trap_chance = 90 - upgrades["trap_chance"]  # maksimum 90
        self.lootrooms = 10 + upgrades["lootrooms"]  # maksimum 50
        self.traps = 50 - upgrades["traps"]  # maksimum 50
        self.die_chance = 80 - upgrades["die_chance"]  # maksimum 80
        self.thread_chance = 40 + upgrades["thread_chance"]  # maksimum 60
        for _ in range(40):
            if random.randint(1, 100) > self.trap_chance:
                self.lootrooms += 1
            else:
                self.traps += 1
        self.basics = 140 - self.traps - self.lootrooms

    def generate_new_map(self):
        x = random.randint(0, 11)  # boss room generation
        self.matrix[x][0].state = 3
        self.matrix[x][0].generated = True
        spawn = random.randint(0, 11)  # spawn generation
        self.playerposition[0] = spawn
        self.playerposition[1] = 11
        self.matrix[spawn][11].visited = True
        self.matrix[spawn][11].generated = True

        escapes = [(i, j) for i in range(12) 
                   for j in range(2) if not self.matrix[i][j].generated]
        random.shuffle(escapes)
        for i in range(2):  # escapes generation
            self.matrix[escapes[i][0]][escapes[i][1]].state = 4
            self.matrix[escapes[i][0]][escapes[i][1]].generated = True

        everything_else = [(i, j) for i in range(12) 
                           for j in range(12) if not self.matrix[i][j].generated]
        random.shuffle(everything_else)

        for i in range(self.basics):  # basic room generation
            if self.matrix[everything_else[i][0]][everything_else[i][1]].generated:
                print("Błąd podczas generacji")
            self.matrix[everything_else[i][0]][everything_else[i][1]].generated = True

        for i in range(self.basics, 
                       self.basics + self.lootrooms): #loot room generation
            if self.matrix[everything_else[i][0]][everything_else[i][1]].generated:
                print("Błąd podczas generacji")
            self.matrix[everything_else[i][0]][everything_else[i][1]].state = 1
            self.matrix[everything_else[i][0]][everything_else[i][1]].generated = True

        for i in range(self.basics + self.lootrooms, 
                       self.basics + self.lootrooms + self.traps):  # traps generation
            if self.matrix[everything_else[i][0]][everything_else[i][1]].generated:
                print("Błąd podczas generacji")
            self.matrix[everything_else[i][0]][everything_else[i][1]].state = 2
            self.matrix[everything_else[i][0]][everything_else[i][1]].generated = True
            
    def reset_map(self):
        for i in range(12):
            for j in range(12):
                self.matrix[i][j].reset()

    def visit(self):
        visited_room = self.matrix[self.playerposition[0]][self.playerposition[1]]
        if not visited_room.visited:
            visited_room.visited = True

            if visited_room.state == 2:
                if random.randint(1, 100) < self.die_chance:
                    return True
                return False
            
    def interact(self):
        interacted_room = self.matrix[self.playerposition[0]][self.playerposition[1]]
        if not interacted_room.interacted:
            interacted_room.interacted = True
            if interacted_room.state == 0:
                if random.randint(1, 100) < self.thread_chance:
                    return 1
                return 0
            if interacted_room.state == 1:
                number = random.randint(1, 100)
                if number < 10:
                    return 11
                return 2
            if interacted_room.state == 2:
                if random.randint(1, 100) < self.die_chance:
                    return 3
                return 1
            if interacted_room.state == 3:
                return 4
            if interacted_room.state == 4:
                return 5
            