import copy
import draw
import inputbox
import random
import pygame
from time import sleep


class Menu(object):
    menu_rect = (200, 150, 450, 430)
    param={"color": (184, 138, 0), "border":4, "margin_x":50, "margin_y":5, "text_size":70, "size_y":70, "space":10}

    def __init__(self, data, draw):
        self.data = data
        self.draw = draw
        self.butons = []
        self.button_list = [{"text": "New Game"}, {"text": "High Scores"}, {"text": "Music"}, {"text": "Quit"}]
        self.buttons = []
        self.animation_max_numb_cell = 52
        self.animation_current_pos = 0
        self.animation_change_numb = 4
        self.animation_content = []
        self.music = True
        i = Menu.menu_rect[1] + Menu.param["text_size"] + 2*Menu.param["margin_y"]+Menu.param["space"]
        for button in self.button_list:
            button_rect = (Menu.menu_rect[0]+Menu.param["margin_x"], i, Menu.menu_rect[2]-Menu.param["margin_x"]-50, Menu.param["size_y"])
            self.buttons.append(button_rect)
            i += Menu.param["size_y"]+Menu.param["space"]
        pygame.display.flip()

    def get_high_scores(self):
        f = open("high scores")
        records = []
        counter = 1
        for line in f:
            if counter > 10:
                break
            i = line.find(";")
            if i != -1:
                records.append([line[:i], line[i+1:].strip()])
                counter += 1
        return records

    def high_scores(self):
        exit_menu = False
        while not exit_menu and not self.data.exit:
            self.animation_change()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.data.exit = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    exit_menu = True
            self.draw.high_scores((200, 150, 450, 530), self.get_high_scores(), self.animation_content)
            sleep(0.04)


    def animation_cell(self):
        cell = []
        cell.append(random.randint(0,23))
        if cell[0] >4 and cell[0] < 20:
            cell.append(random.choice(range(6)+range(20, 26)))
        else:
            cell.append(random.randint(0,25))
        cell.append(random.randint(0, self.data.colors_number - 1))
        return cell

    def animation_init(self):
        for i in range(self.animation_max_numb_cell):
            self.animation_content.append(self.animation_cell())
        for i in range(self.animation_max_numb_cell):
            cell_rect = (self.animation_content[i][0]*30, self.animation_content[i][1]*30, 30, 30)
            self.draw.cell(cell_rect, self.data.colors[self.animation_content[i][2]])

    def animation_change(self):
        for i in range(self.animation_current_pos, self.animation_current_pos+self.animation_change_numb):
            self.animation_content[i] = self.animation_cell()
            self.animation_current_pos += self.animation_change_numb
            self.animation_current_pos %= self.animation_max_numb_cell

    def music_play(self, name = "music.ogg", type = -1):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(type)

    def interval(self,a, l, x):
        if x >= a and x <= a+l:
            return True
        return False

    def menu_option_choose2(self, pos, buttons):
        for i in range(len(buttons)):
            rect = buttons[i]
            if self.interval(rect[0], rect[2], pos[0]) and self.interval(rect[1], rect[3], pos[1]):
                return i+1
        return 0

    def menu_option_choose(self, pos):
        buttons = self.buttons
        for i in range(len(buttons)):
            rect = buttons[i]
            if self.interval(rect[0], rect[2], pos[0]) and self.interval(rect[1], rect[3], pos[1]):
                return i+1
        return 0

    def music_control(self):
        exit_menu = False
        buttons = [(220, 240, 120, 70), (340, 240, 120, 70)]
        while not exit_menu and not self.data.exit:
            self.animation_change()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.data.exit = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    exit_menu = True
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    pos_menu = self.menu_option_choose2(pos, buttons)
                    if pos_menu >0:
                        if pos_menu == 1 and not self.music:
                            self.music = True
                            self.music_play()
                        elif pos_menu == 2 and self.music:
                            self.music = False
                            pygame.mixer.music.stop()
            choose = self.menu_option_choose2(pygame.mouse.get_pos(), buttons)
            self.draw.music_control((200, 150, 450, 430), self.music, choose, self.animation_content)
            sleep(0.04)

    def menu_option(self, option):
        if option == 1:
            self.data = Data(self.data.screen)
            self.draw = draw.Draw(self.data)
            Game(self.data, self.draw).start()
            self.music_play()
        if option == 2:
            self.high_scores()
        if option == 3:
            self.music_control()
        if option == 4:
            self.data.exit = True

    def run(self):
        self.animation_init()
        if self.music:
            self.music_play()
        while not self.data.exit:
            self.animation_change()
            self.draw.menu(self.menu_rect, self.button_list, self.menu_option_choose(pygame.mouse.get_pos()),self.animation_content)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.data.exit = True
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    pos_menu = self.menu_option_choose(pos)
                    if pos_menu >0:
                        self.menu_option(pos_menu)
            sleep(0.04)


class Data(object):
    def __init__(self, screen):
        self.blocks = [[2, [ [0,0], [0,1], [0,2],[0,3]], [[0,0], [1,0], [2,0], [3,0]]],
                    [4, [[0,0], [1,0], [0,1], [0,2]], [[0,0], [0,1], [1,1], [2,1]],[[0,0],[0,1],[0,2],[-1,2]], [[0, 0], [1, 0], [2, 0], [2, 1]]],
                    [2, [[0,0], [0,1], [-1, 1], [1, 0]], [[0, 0], [0, 1], [1, 1], [1, 2]]],
                    [1,  [[0, 0], [0, 1], [1,0], [1, 1] ]],
                    [4,  [[0, 0], [0, 1], [-1, 1], [0,2]], [[0,0], [-1, 0], [0, 1], [1, 0]], [[0, 0], [0,1], [1,1], [0,2]], [[0,0],[0,1], [-1,1], [1,1]]],
                    [2, [[0,0], [1,0], [1,1], [2,1]], [[0,0], [0,1], [-1,1],[-1,2]]],
                    [4, [[0,0], [-1,0], [0,1], [0,2]], [[0,0], [0,1], [-1,1], [-2,1]],[[0,0],[0,1],[0,2],[1,2]], [[0, 0], [-1, 0], [-2, 0], [-2, 1]]]]
        self.blocks_count = 7
        self.width = 10
        self.heigth = 20
        self.score = 0
        self.time = 0.5
        self.screen = screen
        self.table = [[False, False, False, False, False, False, False, False, False, False] for i in range(20)]
        self.table_empty = [[False, False, False, False, False, False, False, False, False, False] for i in range(20)]
        self.table_content = [[False, False, False, False, False, False, False, False, False, False] for i in range(20)]
        self.table_colors = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(20)]
        self.table_next_block = [[False, False, False, False] for i in range(4)]
        self.colors = [(128, 128, 0), (255, 255, 0), (255, 0, 0), (75, 0, 130), (0, 255, 255)]
        self.colors_number = 5
        self.next_block_param = {}
        self.block_param = self.next_block_param
        self.level = 0
        self.lines = 0
        self.speed_table = {0: 53, 1: 49, 2: 45, 3:	41, 4: 37, 5: 33, 6: 28, 7: 22, 8: 17, 9: 11, 10: 10, 11: 9, 12: 8, 13:	7, 14: 6, 15: 6, 16:	5, 17:	5, 18:	4, 19:	4, 20:	3}
        self.lines_per_level = 4
        self.exit = False
        self.high_scores = []


class Game(object):
    def __init__(self, data, draw):
        random.seed()
        self.data = data
        self.draw = draw
        self.exit_to_menu = False
        self.data.next_block_param = self.rand_block()

    def put_block(self):
        self.data.table = copy.deepcopy(self.data.table_empty)
        for i in range(0, 4):
            self.data.table[self.data.block_param["y"] - self.data.blocks[self.data.block_param["nr"]][self.data.block_param["v"]][i][1] ][self.data.block_param["x"] + self.data.blocks[self.data.block_param["nr"]][self.data.block_param["v"]][i][0] ] = True

    def rand_block(self):
        block_param = {}
        block_param["nr"] = random.randint(0, self.data.blocks_count-1)
        block_param["v"] = random.randint(1, self.data.blocks[ block_param["nr"] ][0])
        block_param["color"] = random.randint(0, len(self.data.colors) - 1)
        return block_param

    def new_block(self):
        maxy = 0
        for i in range(4):
            if self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"]][i][1] > maxy:
                maxy = self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"]][i][1]
        self.data.block_param["y"] = maxy
        maxy = 0
        minx = 0
        for i in range(4):
            if self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"]][i][0] > maxy:
                maxy = self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"]][i][0]
        for i in range(4):
            if self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"]][i][0] < minx:
                minx = self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"]][i][0]
        self.data.block_param["x"] = (self.data.width- maxy + minx)/2 - minx

    def check_stop(self):
        for i in range(4):
            if self.data.block_param["y"] - self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"] ][i][1] >= self.data.heigth-1:
                return True
            if self.data.table_content[self.data.block_param["y"] - self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"] ][i][1] + 1 ][self.data.block_param["x"] + self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"] ][i][0]]:
                return True
        return False

    def key_check(self, type):
        block = copy.copy(self.data.block_param)
        if type == "left":
            block["x"] -= 1
        if type == "right":
            block["x"] += 1
        if type == "rotate":
            block["v"] = block["v"] % self.data.blocks[ block["nr"] ][0] +1
        if type == "down":
            block["y"] += 1

        for i in range(4):
            if self.data.blocks[ block["nr"] ][ block["v"]][i][0] + block["x"] < 0 or self.data.blocks[ block["nr"] ][ block["v"]][i][0] + block["x"] >= self.data.width or  block["y"] - self.data.blocks[ block["nr"] ][ block["v"]][i][1] < 0 or  block["y"] - self.data.blocks[ block["nr"] ][ block["v"]][i][1] >= self.data.heigth or self.data.table_content[ block["y"] - self.data.blocks[ block["nr"] ][ block["v"]][i][1] ][ self.data.blocks[ block["nr"] ][ block["v"]][i][0] + block["x"] ] :
                return False
        return True

    def add_block(self):
        multiplier = self.data.level+1
        self.data.score += 4*multiplier
        for i in range(4):
            # DEBUG
            self.data.table_content[ self.data.block_param["y"] -self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"] ][i][1]  ][ self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"] ][i][0] + self.data.block_param["x"] ] = True
            self.data.table_colors[ self.data.block_param["y"] -self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"] ][i][1]  ][ self.data.blocks[ self.data.block_param["nr"] ][ self.data.block_param["v"] ][i][0] + self.data.block_param["x"] ] = self.data.block_param["color"]

    def empty_line(self, i):
        for j in range(self.data.width):
            if self.data.table_content[i][j]:
                return False
        return True

    def full_line(self, i):
        for j in range(self.data.width):
            if not self.data.table_content[i][j]:
                return False
        return True

    def erase_line(self):
        lines = []
        for i in range(self.data.heigth-1, -1, -1):
            if self.full_line(i):
                lines.append(i)
        lines_count = len(lines)
        self.data.lines += lines_count
        multiplier = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200 }.get(lines_count)
        self.data.score += multiplier * (self.data.level+1)
        self.draw.erase_line_animation((150, 50, 310, 610), lines)
        for i in lines:
            self.data.table_content[i] = copy.copy(self.data.table_empty[0])
        i = self.data.heigth -1
        empty_line_below = False
        empty_y = 0
        while i >= 0:
            if self.empty_line(i):
                if not empty_line_below:
                    empty_y = i
                    empty_line_below = True
            else:
                if empty_line_below:
                    self.data.table_content[empty_y] = copy.copy(self.data.table_content[i])
                    self.data.table_content[i] = copy.copy(self.data.table_empty[0])
                    empty_y -= 1
            i -= 1

    def not_dead(self):
        for i in self.data.table_content[0]:
            if i:
                return False
        return True

    def upgrade_next_block(self):
        self.data.table_next_block = [[False, False, False, False] for i in range(4)]
        minx = self.data.blocks[self.data.next_block_param["nr"]][self.data.next_block_param["v"]][0][0]
        maxx = self.data.blocks[self.data.next_block_param["nr"]][self.data.next_block_param["v"]][0][0]
        miny = self.data.blocks[self.data.next_block_param["nr"]][self.data.next_block_param["v"]][0][1]
        maxy = self.data.blocks[self.data.next_block_param["nr"]][self.data.next_block_param["v"]][0][1]
        for i in range(4):
            x = self.data.blocks[self.data.next_block_param["nr"]][self.data.next_block_param["v"]][i][0]
            y = self.data.blocks[self.data.next_block_param["nr"]][self.data.next_block_param["v"]][i][1]
            if minx > x:
                minx = x
            elif maxx < x:
                maxx = x
            if miny > y:
                miny = y
            elif maxy < y:
                maxy = y
        for i in range(4):
            x = self.data.blocks[self.data.next_block_param["nr"]][self.data.next_block_param["v"]][i][0] - minx + (4 - maxx + minx)/2
            y = maxy - self.data.blocks[self.data.next_block_param["nr"]][self.data.next_block_param["v"]][i][1] + (4 - maxy + miny)/2
            self.data.table_next_block[y][x] = True

    def upgrade_level(self):
        self.data.level = self.data.lines/self.data.lines_per_level
        if self.data.level > 20:
            self.data.level = 20
        self.data.time = float(self.data.speed_table.get(self.data.level, 53)) * 0.5/53.0

    def music_play(self, name = "music.ogg", type = -1):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(type)

    def count_digit(self, number):
        k = 0
        while number != 0:
            number/=10
            k += 1
        return k

    def get_high_scores(self):
        f = open("high scores")
        records = []
        counter = 1
        for line in f:
            if counter > 10:
                break
            i = line.find(";")
            if i != -1:
                records.append([line[:i], line[i+1:].strip()])
                counter += 1
        return records

    def pos_high_score(self, score):
        pos = 0
        for i in range(len(self.data.high_scores) -1, -1, -1):
            if score <= int(self.data.high_scores[i][1]):
                print self.data.high_scores[i][1]
                pos = i+1
                break
        return pos

    def upgrade_high_score(self, pos, new_record):
        for i in range(8, pos-1, -1):
            self.data.high_scores[i+1] = self.data.high_scores[i]
        self.data.high_scores[pos] = new_record
        f = open("high scores", "w")
        for record in self.data.high_scores:
            str =""
            for field in record:
                str+= field+";"
            str = str[:-1]+"\n"
            f.write(str)

    def game_over(self):
        self.music_play("game_over.mp3", 0)
        self.draw.message((160,150,400,200), "Game over")
        pygame.display.flip()
        sleep(5.2)
        self.draw.message((160,150,500 + 25*self.count_digit(self.data.score), 200), "Your score: "+str(self.data.score))
        pygame.display.flip()
        sleep(3.2)
        self.data.high_scores = self.get_high_scores()
        pos = self.pos_high_score(self.data.score)
        if pos < 10:
            self.draw.message((160,150,550, 200), "New high score!")
            pygame.display.flip()
            sleep(3.2)
            self.data.screen.fill((0, 0, 0))
            self.draw.add_panel((160, 150, 600, 250), (255, 255, 255), {"border": 2, "cborder": (0, 0, 0)})
            self.draw.text("New high score!",170, 160, 80)
            self.draw.text("Enter - Accept",170, 325, 50)
            name = inputbox.ask(self.data.screen, (170, 250, 500, 55), "Your name: ", self.data)
            new_record = [name, str(self.data.score)]
            self.upgrade_high_score(pos, new_record)

    def hard_drop(self):
        while not self.check_stop():
            self.data.block_param["y"] += 1
            self.put_block()

    def pause(self):
        self.draw.pause()
        pause = True
        while pause and not self.data.exit and not self.exit_to_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.data.exit = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.exit_to_menu = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pause = False
            sleep(0.04)

    def start(self):
        self.data.block_param = self.data.next_block_param
        self.data.next_block_param = self.rand_block()
        self.new_block()
        self.upgrade_next_block()
        push = 0
        push_fast = 30
        button = "K_ESCAPE"
        if_pressed = False
        while self.not_dead() and not self.data.exit and not self.exit_to_menu:
            while not self.check_stop() and not self.data.exit and not self.exit_to_menu:
                self.put_block()
                self.draw.game((150, 50, 310, 610))
                fps = 0
                while fps < 100 and not self.data.exit and not self.exit_to_menu:
                    change = False
                    sleep(self.data.time/100.0)
                    if button == "K_LEFT":
                        if_pressed = pygame.key.get_pressed()[pygame.K_LEFT]
                    elif button == "K_RIGHT":
                        if_pressed = pygame.key.get_pressed()[pygame.K_RIGHT]
                    elif button == "K_DOWN":
                        if_pressed = pygame.key.get_pressed()[pygame.K_DOWN]
                    if if_pressed:
                        push += 1
                        if push >= push_fast:
                            push = 0
                            if button == "K_LEFT" and self.key_check("left"):
                                self.data.block_param["x"] -= 1
                            elif button == "K_RIGHT" and self.key_check("right"):
                                self.data.block_param["x"] += 1
                            elif button == "K_DOWN" and self.key_check("down"):
                                self.data.block_param["y"] += 1
                            self.put_block()
                            self.draw.game((150, 50, 310, 610))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.data.exit = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT and self.key_check("left"):
                                push = 0
                                button = "K_LEFT"
                                self.data.block_param["x"] -= 1
                                change = True
                            if event.key == pygame.K_RIGHT and self.key_check("right"):
                                push = 0
                                button = "K_RIGHT"
                                self.data.block_param["x"] += 1
                                change = True
                            if event.key == pygame.K_UP and self.key_check("rotate"):
                                self.data.block_param["v"] = (self.data.block_param["v"] % self.data.blocks[ self.data.block_param["nr"] ][0]) + 1
                                change = True
                            if event.key == pygame.K_DOWN and self.key_check("down"):
                                push = 0
                                button = "K_DOWN"
                                self.data.block_param["y"] += 1
                                change = True
                            if event.key == pygame.K_RCTRL:
                                self.hard_drop()
                                change = True
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                self.exit_to_menu = True
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                                self.pause()
                        if change:
                            self.put_block()
                            self.draw.game((150, 50, 310, 610))
                    fps +=1
                if not self.check_stop():
                    self.data.block_param["y"] += 1
                self.put_block()
                self.draw.game((150, 50, 310, 610))
                fps = 0
                while fps < 50 and not self.data.exit and not self.exit_to_menu:
                    change = False
                    sleep(self.data.time/100.0)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.data.exit = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT and self.key_check("left"):
                                self.data.block_param["x"] -= 1
                                change = True
                            if event.key == pygame.K_RIGHT and self.key_check("right"):
                                self.data.block_param["x"] += 1
                                change = True
                            if event.key == pygame.K_UP and self.key_check("rotate"):
                                self.data.block_param["v"] = (self.data.block_param["v"] % self.data.blocks[ self.data.block_param["nr"] ][0]) + 1
                                change = True
                            if event.key == pygame.K_DOWN and self.key_check("down"):
                                self.data.block_param["y"] += 1
                                change = True
                        if change:
                            self.put_block()
                            self.draw.game((150, 50, 310, 610))
                    fps +=1
            self.add_block()
            self.data.table = copy.deepcopy(self.data.table_empty)
            self.draw.game((150, 50, 310, 610))
            self.erase_line()
            self.data.block_param = self.data.next_block_param
            self.data.next_block_param = self.rand_block()
            self.new_block()
            self.upgrade_next_block()
            self.upgrade_level()
        if not self.not_dead():
            self.game_over()


class Interface(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 740))
        pygame.display.set_caption("Tetris")
        self.data = Data(self.screen)
        self.draw = draw.Draw(self.data)
        self.menu = Menu(self.data, self.draw)
        self.menu.run()
        pygame.quit()


def main():
    Interface()

if __name__ == '__main__':
    main()
