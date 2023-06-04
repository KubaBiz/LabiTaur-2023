# Graficzny interfejs gry

import map
import filehandler
import pygame
import data.hollow
from os import environ, path
import random
from time import sleep
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


pygame.init()

font = pygame.font.SysFont('Impact', 45)

screen_width = 1100
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


class Button():
    # współrzędne lewego górnego rogu, szerokość i długość, lista do której przypisujemy, 
    # tekst na przycisku, kolor tekstu, funkcja po kliknięciu
    def __init__(self, x, y, width, height, buttons, buttonText='Button', 
                 textColor=(20, 20, 20), onclickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.alreadyPressed = False

        self.fillColors = {
            'normal': (0, 0, 0),
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, textColor)
        buttons.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

    def returnXY(self):
        return (self.x, self.y)


class Application():
    flag = True

    def __init__(self, game_state):
        self.game_state = game_state
        self.start_buttons = []
        self.confirmation_buttons = []
        self.preparation_buttons = []
        self.shop_buttons = []
        self.escape_buttons = []
        self.game_over_buttons = []
        self.game_over = False
        self.running = True
        self.event_active = False
        self.rooms = map.Map()
        self.tempmoney = 0
        self.torch = None
        self.totalmoney = None
        self.difficulty = None
        self.upgrades = {}
        self.statistics = []

        start_button_width = 250

        if path.exists(".\\data\\save.txt"):
            Button(screen_width / 2 - start_button_width / 2, screen_height / 2 - 120, start_button_width, 80, 
                   self.start_buttons, 'Continue', (255,  255,  255), self.continuegameFunction)

        Button(screen_width / 2 - start_button_width / 2, screen_height / 2 + 15, start_button_width, 80, 
               self.start_buttons, 'New Game', (255,  255,  255), self.newstartFunction)
        Button(screen_width / 2 - start_button_width / 2, screen_height / 2 + 150, start_button_width, 80, 
               self.start_buttons, 'Quit', (255,  255,  255), self.quitFunction)

        preparation_button_width = 360

        Button(screen_width / 2 - preparation_button_width / 2, screen_height / 2 - 30, preparation_button_width, 80, 
               self.preparation_buttons, 'Enter labirynth - E', (255,  255,  255), self.enterLabirynthFunction)
        Button(screen_width / 2 - preparation_button_width / 2, screen_height / 2 + 70, preparation_button_width, 80, 
               self.preparation_buttons, 'Shop - S', (255,  255,  255), self.shopFunction)
        Button(screen_width / 2 - preparation_button_width / 2, screen_height / 2 + 170, preparation_button_width, 80, 
               self.preparation_buttons, 'Quit - Q', (255,  255,  255), self.quitFunction)

        Button(screen_width / 2 - start_button_width / 2, screen_height / 2, start_button_width, 80, 
               self.escape_buttons, 'Continue - C', (255,  255,  255), self.afterlabirynthFunction)
        Button(screen_width / 2 - start_button_width / 2, screen_height / 2 + 100, start_button_width, 80, 
               self.escape_buttons, 'Quit - Q', (255,  255,  255), self.quitFunction)

        Button(screen_width / 2 - start_button_width / 2, screen_height / 2 + 10, start_button_width, 80, 
               self.game_over_buttons, 'Restart - R', (255,  255,  255), self.afterlabirynthFunction)
        Button(screen_width / 2 - start_button_width / 2, screen_height / 2 + 100, start_button_width, 80, 
               self.game_over_buttons, 'Quit - Q', (255,  255,  255), self.quitFunction)

        Button(screen_width / 2 - start_button_width - 5, screen_height / 2 - 10, start_button_width, 80, 
               self.confirmation_buttons, 'Normal', (0,  255,  0), self.choosenormalFunction)
        Button(screen_width / 2 + 5, screen_height / 2 - 10, start_button_width, 80, 
               self.confirmation_buttons, 'Hard', (255,  0,  0), self.choosehardFunction)
        Button(screen_width / 2 - start_button_width / 2, screen_height / 2 + 80, start_button_width, 80, 
               self.confirmation_buttons, 'Cancel', (255,  255,  255), self.cancelFunction)

        shop_button_width = 100

        Button(screen_width / 2 - preparation_button_width / 2, screen_height / 2 + 170, preparation_button_width, 80, 
               self.shop_buttons, 'Return - R', (255,  255,  255), self.returnFunction)
        Button(screen_width / 2 - 3.5 * shop_button_width, screen_height / 2 - 120, shop_button_width, 60, 
               self.shop_buttons, 'Buy', (255,  255,  255), self.oneproductFunction)
        Button(screen_width / 2 - 0.5 * shop_button_width, screen_height / 2 - 120, shop_button_width, 60, 
               self.shop_buttons, 'Buy', (255,  255,  255), self.twoproductFunction)
        Button(screen_width / 2 + 2.5 * shop_button_width, screen_height / 2 - 120, shop_button_width, 60, 
               self.shop_buttons, 'Buy', (255,  255,  255), self.threeproductFunction)
        Button(screen_width / 2 - 3.5 * shop_button_width, screen_height / 2 + 80, shop_button_width, 60, 
               self.shop_buttons, 'Buy', (255,  255,  255), self.fourproductFunction)
        Button(screen_width / 2 - 0.5 * shop_button_width, screen_height / 2 + 80, shop_button_width, 60, 
               self.shop_buttons, 'Buy', (255,  255,  255), self.fiveproductFunction)
        Button(screen_width / 2 + 2.5 * shop_button_width, screen_height / 2 + 80, shop_button_width, 60, 
               self.shop_buttons, 'Buy', (255,  255,  255), self.sixproductFunction)

    def _draw_start_menu(self):
        screen.fill((0, 0, 0))
        for button in self.start_buttons:
            button.process()

        title_font = pygame.font.SysFont('Impact', 65, italic=True)
        title = data.hollow.textOutline(title_font, 'L a b i T a u r', (200, 200, 255), (255, 0, 0))
        screen.blit(title, (screen_width / 2 - title.get_width() / 2, title.get_height() / 2 - 10))
        pygame.display.flip()

    def _draw_confirmation(self):
        screen.fill((0, 0, 0))
        for button in self.confirmation_buttons:
            button.process()
        confirm = font.render("Choose difficulty", True, (255, 255, 255))
        screen.blit(confirm, (screen_width / 2 - confirm.get_width() / 2, screen_height / 2 - 90))
        pygame.display.flip()

    def _draw_preparation_room(self):
        screen.fill((0, 0, 0))
        for button in self.preparation_buttons:
            button.process()

        font_type = 'Arial'
        info_font = pygame.font.SysFont(font_type, 36)
        ariadne = info_font.render('Total pieces: ' +
                                   str(self.totalmoney), True, (255, 255, 255))
        screen.blit(ariadne, (10, 10))
        deaths = info_font.render('Minotaurs killed: ' +
                                  str(self.statistics[2]), True, (255, 255, 255))
        screen.blit(deaths, (800, 10))
        escapes = info_font.render(' Times escaped: ' +
                                   str(self.statistics[1]), True, (255, 255, 255))
        screen.blit(escapes, (800, 50))
        kills = info_font.render('      Total deaths: ' +
                                 str(self.statistics[0]), True, (255, 255, 255))
        screen.blit(kills, (800, 90))

        pygame.display.flip()

    def _draw_shop(self):
        maximum_upgrades = [90, 50, 50, 80, 60, 90]
        screen.fill((0, 0, 0))
        self.shop_buttons[0].process()

        image = pygame.image.load("data\\shield.png")
        image = pygame.transform.scale(image, (200, 218))
        image = pygame.transform.rotate(image, 350)
        screen.blit(image, (870, 353))

        image = pygame.image.load("data\\sword.png")
        image = pygame.transform.scale(image, (85, 412))
        image = pygame.transform.rotate(image, 12)
        screen.blit(image, (10, 80))

        i = 0
        for keys in self.upgrades:
            if self.upgrades[keys] < maximum_upgrades[i]:
                self.shop_buttons[i + 1].process()
            else:
                button = self.shop_buttons[i + 1]
                limit = font.render('Max', True, (255, 255, 255))
                screen.blit(limit, (button.returnXY()[0] + 10, button.returnXY()[1] + 4))
            i += 1

        # opis kupowanych przedmiotów, wyliczanie ceny
        font_type = 'Arial'
        info_font = pygame.font.SysFont(font_type, 24)

        trap_chance = info_font.render('Less chance to spawn traps', True, (255, 255, 255))
        screen.blit(trap_chance, (135, 115))
        if self.upgrades["trap_chance"] < maximum_upgrades[0]:
            trap_chance_cost = info_font.render('Cost: ' + str(40 + 20 * self.upgrades["trap_chance"]) +
                                                ' Level: ' + str(self.upgrades["trap_chance"]), True, (255, 255, 255))
            screen.blit(trap_chance_cost, (167, 145))
        lootrooms = info_font.render('Spawn more loot rooms', True, (255, 255, 255))
        screen.blit(lootrooms, (442, 115))
        if self.upgrades["lootrooms"] < maximum_upgrades[1]:
            lootrooms_cost = info_font.render('Cost: ' + str(int(10 + 1.25**self.upgrades["lootrooms"])) +
                                              ' Level: ' + str(self.upgrades["lootrooms"]), True, (255, 255, 255))
            screen.blit(lootrooms_cost, (460, 145))
        traps = info_font.render('Spawn less traps', True, (255, 255, 255))
        screen.blit(traps, (775, 115))
        if self.upgrades["traps"] < maximum_upgrades[2]:
            traps_cost = info_font.render('Cost: ' + str(int(40 * (1 + 0.12) ** (self.upgrades["traps"] - 1))) +
                                          ' Level: ' + str(self.upgrades["traps"]), True, (255, 255, 255))
            screen.blit(traps_cost, (760, 145))

        die_chance = info_font.render('Less chance to die from traps', True, (255, 255, 255))
        screen.blit(die_chance, (130, 315))
        if self.upgrades["die_chance"] < maximum_upgrades[3]:
            die_chance_cost = info_font.render('Cost: ' + str(int(10 * (1 + 0.12) ** (self.upgrades["die_chance"] - 1))) +
                                               ' Level: ' + str(self.upgrades["die_chance"]), True, (255, 255, 255))
            screen.blit(die_chance_cost, (167, 345))
        thread_chance = info_font.render('Better chance to get threads', True, (255, 255, 255))
        screen.blit(thread_chance, (430, 315))
        if self.upgrades["thread_chance"] < maximum_upgrades[4]:
            lootrooms_cost = info_font.render('Cost: ' + str(int(4 + 4 * self.upgrades["thread_chance"])) +
                                              ' Level: ' + str(self.upgrades["thread_chance"]), True, (255, 255, 255))
            screen.blit(lootrooms_cost, (465, 345))
        torch_time = info_font.render('More fuel on torch', True, (255, 255, 255))
        screen.blit(torch_time, (770, 315))
        if self.upgrades["torch_time"] < maximum_upgrades[5]:
            torch_time_cost = info_font.render('Cost: ' + str(int(2 + 1.11 * self.upgrades["torch_time"])) +
                                               ' Level: ' + str(self.upgrades["torch_time"]), True, (255, 255, 255))
            screen.blit(torch_time_cost, (770, 345))

        money_font = pygame.font.SysFont(font_type, 36)
        ariadne = money_font.render('Total pieces: ' + str(self.totalmoney), True, (255, 255, 255))
        screen.blit(ariadne, (100, 490))

        pygame.display.flip()

    def _draw_game_over_screen(self):
        screen.fill((0, 0, 0))
        for button in self.game_over_buttons:
            button.process()
        title = font.render('You died', True, (255, 255, 255))
        screen.blit(title, (screen_width / 2 - title.get_width() / 2, screen_height / 2 - title.get_height() / 2 - 70))
        pygame.display.flip()

    def _draw_labirynth(self):
        screen.fill((0, 0, 0))
        player_position = self.rooms.playerposition

        radius = 120
        if self.torch < 10:
            radius = 12 * self.torch
        screen.set_clip(None)
        screen.fill(0)
        circularArea = pygame.Surface((520, 520), pygame.SRCALPHA)
        circularArea.fill((0, 0, 0, 255))
        pygame.draw.circle(circularArea, (0, 0, 0, 0), (player_position[1] * 42 + 29, player_position[0] * 42 + 29), radius)
        areaTopleft = (screen_width / 2 - 260, screen_height / 2 - 260)
        clipRect = pygame.Rect(areaTopleft, (520, 520))
        screen.set_clip(clipRect)

        for i in range(12):
            for j in range(12):
                room = self.rooms.matrix[i][j]
                if not room.visited:
                    pygame.draw.rect(screen, '#333333', 
                                     (screen_width / 2 - 249 + (j * 42), screen_height / 2 - 249 + (i * 42), 36, 36))
                elif room.state == 0:
                    pygame.draw.rect(screen, '#666666',
                                     (screen_width / 2 - 249 + (j * 42), screen_height / 2 - 249 + (i * 42), 36, 36))
                elif room.state == 1:
                    pygame.draw.rect(screen, '#999900',
                                     (screen_width / 2 - 249 + (j * 42), screen_height / 2 - 249 + (i * 42), 36, 36))
                elif room.state == 2:
                    pygame.draw.rect(screen, '#CC0000',
                                     (screen_width / 2 - 249 + (j * 42), screen_height / 2 - 249 + (i * 42), 36, 36))
                elif room.state == 3:
                    pygame.draw.rect(screen, '#703A3A',
                                     (screen_width / 2 - 249 + (j * 42), screen_height / 2 - 249 + (i * 42), 36, 36))
                elif room.state == 4:
                    pygame.draw.rect(screen, '#00CCCC',
                                     (screen_width / 2 - 249 + (j * 42), screen_height / 2 - 249 + (i * 42), 36, 36))

        pygame.draw.circle(screen, '#00DE00',
                           (screen_width / 2 - 231 + (player_position[1] * 42), 
                            screen_height / 2 - 231 + (player_position[0] * 42)), 12)
        font_type = 'Arial'
        fonty = pygame.font.SysFont(font_type, 78, bold=True)

        screen.blit(circularArea, areaTopleft)
        screen.set_clip(None)

        if not self.rooms.matrix[player_position[0]][player_position[1]].interacted:
            e_check = fonty.render('E', True, (255, 255, 255))
            screen.blit(e_check, (836, 478))
        w_check = fonty.render('W', True, (255, 255, 255))
        screen.blit(w_check, (128, 400))
        a_check = fonty.render('A', True, (255, 255, 255))
        screen.blit(a_check, (63, 478))
        s_check = fonty.render('S', True, (255, 255, 255))
        screen.blit(s_check, (140, 478))
        d_check = fonty.render('D', True, (255, 255, 255))
        screen.blit(d_check, (207, 478))
        info_font = pygame.font.SysFont(font_type, 36)
        ariadne = info_font.render('Collected pieces: ' + str(self.tempmoney), True, (255, 255, 255))
        screen.blit(ariadne, (10, 10))
        light = info_font.render('Hours left: ' + str(int(self.torch)), True, (255, 255, 255))
        screen.blit(light, (836, 10))

        pygame.display.flip()

    def _draw_escaped_screen(self, flag: bool):
        screen.fill((0, 0, 0))
        for button in self.escape_buttons:
            button.process()
        if not flag:
            escaped = font.render("You escaped!   Next time try to fight Minotaur", True, (170, 170, 255))
            screen.blit(escaped,
                (screen_width / 2 - escaped.get_width() / 2, screen_height / 2 - escaped.get_height() / 2 - 60))
        else:
            killed_minotaur = font.render("You killed Minotaur!", True, (150, 150, 255))
            screen.blit(killed_minotaur,
                (screen_width / 2 - killed_minotaur.get_width() / 2, screen_height / 2 - killed_minotaur.get_height() / 2 - 110))
            congratulations = font.render("Congratulations on completing my game", True, (150, 150, 255))
            screen.blit(congratulations,
                (screen_width / 2 - congratulations.get_width() / 2, screen_height / 2 - congratulations.get_height() / 2 - 45))
        pygame.display.flip()

    def _draw_boss_room(self):
        screen.fill((0, 0, 0))
        image = pygame.image.load("data\\minotaur.png")
        image = pygame.transform.scale(image, (600, 500))
        screen.blit(image, (250, 20))

    def newstartFunction(self):
        self.game_state = "confirmation"

    def choosenormalFunction(self):
        self._confirmationFunction(0)

    def choosehardFunction(self):
        self._confirmationFunction(1)

    def _confirmationFunction(self, difficulty: int):
        filehandler.newfile(6)
        self.totalmoney = 0
        self.upgrades = {"trap_chance": 0, "lootrooms": 0, "traps": 0, 
                         "die_chance": 0, "thread_chance": 0, "torch_time": 0}
        self.statistics = [0 for _ in range(3)]
        self.difficulty = difficulty
        self.game_state = "preparation_room"
        self.rooms.set_generation(self.upgrades)

    def cancelFunction(self):
        self.game_state = "start_menu"

    def continuegameFunction(self):
        self.totalmoney, self.difficulty, self.statistics, self.upgrades = filehandler.readfile()
        self.rooms.set_generation(self.upgrades)
        self.game_state = "preparation_room"

    def oneproductFunction(self):
        self._buyproductFunction(1)

    def twoproductFunction(self):
        self._buyproductFunction(2)

    def threeproductFunction(self):
        self._buyproductFunction(3)

    def fourproductFunction(self):
        self._buyproductFunction(4)

    def fiveproductFunction(self):
        self._buyproductFunction(5)

    def sixproductFunction(self):
        self._buyproductFunction(6)

    # kup przedmioty, wylicz cenę, odejmij kasę
    def _buyproductFunction(self, number: int):
        if number == 1 and 40 + 20 * self.upgrades["trap_chance"] <= self.totalmoney:
            self.totalmoney -= 40 + 20 * self.upgrades["trap_chance"]
            self.upgrades["trap_chance"] += 1
        elif number == 2 and int(10 + 1.25**self.upgrades["lootrooms"]) <= self.totalmoney:
            self.totalmoney -= int(10 + 1.25**self.upgrades["lootrooms"])
            self.upgrades["lootrooms"] += 1
        elif number == 3 and int(40 * (1 + 0.12) ** (self.upgrades["traps"] - 1)) <= self.totalmoney:
            self.totalmoney -= int(40 * (1 + 0.12) ** (self.upgrades["traps"] - 1))
            self.upgrades["traps"] += 1
        elif number == 4 and int(10 * (1 + 0.12) ** (self.upgrades["die_chance"] - 1)) <= self.totalmoney:
            self.totalmoney -= int(10 * (1 + 0.12) ** (self.upgrades["die_chance"] - 1))
            self.upgrades["die_chance"] += 1
        elif number == 5 and int(4 + 4 * self.upgrades["thread_chance"]) <= self.totalmoney:
            self.totalmoney -= int(4 + 4 * self.upgrades["thread_chance"])
            self.upgrades["thread_chance"] += 1
        elif number == 6 and int(2 + 1.11 * self.upgrades["torch_time"]) <= self.totalmoney:
            self.totalmoney -= int(2 + 1.11 * self.upgrades["torch_time"])
            self.upgrades["torch_time"] += 1

    def returnFunction(self):
        filehandler.savefile(self.totalmoney, self.difficulty, self.statistics, self.upgrades)
        self.rooms.set_generation(self.upgrades)
        self.game_state = "preparation_room"

    def afterlabirynthFunction(self):
        self.tempmoney = 0
        self.game_state = "preparation_room"
        Application.flag = True
        self.rooms.reset_map()
        self.event_active = False

    def shopFunction(self):
        self.game_state = "shop"

    def quitFunction(self):
        if self.statistics != []:
            filehandler.savefile(self.totalmoney, self.difficulty, self.statistics, self.upgrades)
        self.running = False
        pygame.quit()
        quit()

    def enterLabirynthFunction(self):
        self.game_state = "game"
        self.game_over = False
        self.torch = int(self.upgrades["torch_time"] * 1.2) + 12
        self.rooms.generate_new_map()

    def generateKeys(self):
        if self.difficulty == 0:
            return [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d]

        elif self.difficulty == 1:
            key_list = []
            for key_code in range(pygame.K_a, pygame.K_z + 1):
                key_list.append(key_code)

            return key_list

    def run(self):
        fps = 60
        fpsClock = pygame.time.Clock()
        fpsClock.tick(fps)

        pygame.display.set_caption('LabiTaur')

        Icon = pygame.image.load('.\\data\\icon.png')
        pygame.display.set_icon(Icon)

        event_duration = 1.8
        prompt_interval = 3.0
        prompt_timer = prompt_interval
        event_start_time = 0.0
        indicator = ""
        time_ended = False
        key_in_boss_fight = 0
        old_key = -1

        while self.running:

            w_key_pressed = False
            a_key_pressed = False
            s_key_pressed = False
            d_key_pressed = False
            e_key_pressed = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and self.event_active:
                    if event.key == key_prompt:
                        indicator = "1"
                    else:
                        indicator = "0"
                        self.game_over = True
                        self.game_state = "game_over"
                        self.event_active = False

                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_UP):
                    w_key_pressed = True
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_LEFT):
                    a_key_pressed = True
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN):
                    s_key_pressed = True
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                    d_key_pressed = True
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_e or event.key == pygame.K_SPACE):
                    e_key_pressed = True

            fpsClock.tick(fps)

            if self.game_state == "game":
                if w_key_pressed and self.rooms.playerposition[0] > 0:
                    self.rooms.playerposition[0] -= 1
                    self.torch -= 0.2
                    if self.rooms.visit():
                        self.game_state = "game_over"
                        self.game_over = True
                if a_key_pressed and self.rooms.playerposition[1] > 0:
                    self.rooms.playerposition[1] -= 1
                    self.torch -= 0.2
                    if self.rooms.visit():
                        self.game_state = "game_over"
                        self.game_over = True
                if s_key_pressed and self.rooms.playerposition[0] < 11:
                    self.rooms.playerposition[0] += 1
                    self.torch -= 0.2
                    if self.rooms.visit():
                        self.game_state = "game_over"
                        self.game_over = True
                if d_key_pressed and self.rooms.playerposition[1] < 11:
                    self.rooms.playerposition[1] += 1
                    self.torch -= 0.2
                    if self.rooms.visit():
                        self.game_state = "game_over"
                        self.game_over = True
                if e_key_pressed:
                    switch = self.rooms.interact()
                    if switch is not None:
                        self.torch -= 1
                    if switch == 1:
                        self.tempmoney += 1
                    elif switch == 2:
                        self.tempmoney += 2
                    elif switch == 3:
                        self.game_state = "game_over"
                        self.game_over = True
                    elif switch == 4:
                        self.game_state = "boss_room"
                    elif switch == 5:
                        self.game_state = "escaped"
                    elif switch == 11:
                        self.tempmoney = int(self.tempmoney * 1.2 + 2)
                if self.torch < 1 and self.game_state not in ["escaped", "boss_room"]:
                    self.game_over = True
                    self.game_state = "game_over"
                self._draw_labirynth()
                if self.game_state == "game_over" and self.game_over:
                    sleep(0.5)
            if self.game_state == "start_menu":
                self._draw_start_menu()
                if self.game_state == "confirmation":
                    sleep(0.2)

            elif self.game_state == "confirmation":
                self._draw_confirmation()
                if self.game_state in ["preparation_room", "start_menu"]:
                    sleep(0.2)

            elif self.game_state == "preparation_room":
                self._draw_preparation_room()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    self.enterLabirynthFunction()
                if keys[pygame.K_s]:
                    self.shopFunction()
                if keys[pygame.K_q]:
                    self.quitFunction()

                key_in_boss_fight = 0
                old_key = -1

                if self.game_state in ["shop"]:
                    sleep(0.2)

            elif self.game_state == "shop":
                self._draw_shop()
                if self.game_state == "preparation_room":
                    sleep(0.35)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.returnFunction()

            if self.game_state == "escaped":  # ucieczka przez niebieski portal
                if Application.flag:
                    self.statistics[1] += 1
                    self.totalmoney += self.tempmoney
                    filehandler.savefile(self.totalmoney, self.difficulty, self.statistics, self.upgrades)
                    Application.flag = False

                self._draw_escaped_screen(False)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_c]:
                    self.afterlabirynthFunction()
                if keys[pygame.K_q]:
                    self.quitFunction()

            elif self.game_state == "boss_room":  # walka z bossem
                self._draw_boss_room()
                amount_of_keys = self.difficulty * 10 + 10

                # generacja znaków do klawiatury (20 na hard całą klawiaturę, 10 na normal WASDE)
                available_keys = self.generateKeys()

                if self.event_active:
                    current_time = pygame.time.get_ticks() / 1000.0
                    elapsed_time = current_time - event_start_time
                    if elapsed_time >= event_duration:
                        self.event_active = False
                        prompt_timer = prompt_interval
                        indicator = ""
                        time_ended = True

                else:
                    prompt_timer -= pygame.time.get_ticks() / 1000.0
                    if prompt_timer <= 0.0:
                        self.event_active = True
                        prompt_timer = 0.0
                        event_start_time = pygame.time.get_ticks() / 1000.0
                        time_ended = False

                        key_in_boss_fight += 1
                        key_prompt = random.choice(available_keys)

                if self.event_active:
                    y_coordinate = 350
                    if key_in_boss_fight > old_key and key_in_boss_fight <= amount_of_keys:
                        old_key = key_in_boss_fight
                        x_coordinate = random.randint(100, 900)
                    side_length = 100

                    pygame.draw.circle(screen, (100, 100, 215),
                                       (x_coordinate + side_length // 2, y_coordinate + side_length // 2), 50)

                    font2 = pygame.font.SysFont('Verdana', 60)

                    text_surface = font2.render(pygame.key.name(key_prompt).capitalize(), True, (200, 0, 0))
                    text_x = x_coordinate + side_length // 2 - text_surface.get_width() // 2
                    text_y = y_coordinate + side_length // 2 - text_surface.get_height() // 2

                    screen.blit(text_surface, (text_x, text_y))

                if indicator:
                    if indicator == "1":
                        self.event_active = False
                        indicator = ""

                if time_ended:
                    self.event_active = False
                    self.game_over = True
                    self.game_state = "game_over"

                if key_in_boss_fight > amount_of_keys:
                    self.event_active = False
                    self.game_state = "killed_minotaur"

                pygame.display.flip()

            elif self.game_state == "game_over":
                if Application.flag:  # przypisanie monet do konta, zmiana statystyk, zapis do pliku
                    self.statistics[0] += 1
                    if self.tempmoney >= 4:
                        self.totalmoney = self.totalmoney + int(self.tempmoney * 0.3)
                    else:
                        self.totalmoney += 1
                    filehandler.savefile(self.totalmoney, self.difficulty, self.statistics, self.upgrades)
                    Application.flag = False
                self._draw_game_over_screen()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.afterlabirynthFunction()
                if keys[pygame.K_q]:
                    self.quitFunction()

            elif self.game_state == "killed_minotaur":  # zabicie minotaura, skończenie gry
                if Application.flag:
                    self.statistics[2] += 1
                    self.totalmoney += self.tempmoney + 1000
                    filehandler.savefile(self.totalmoney, self.difficulty, self.statistics, self.upgrades)
                    Application.flag = False

                self._draw_escaped_screen(True)
                if keys[pygame.K_c]:
                    self.afterlabirynthFunction()
                if keys[pygame.K_q]:
                    self.quitFunction()
