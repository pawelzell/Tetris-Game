import pygame
from time import sleep


class Draw(object):
    def __init__(self, data):
        self.data = data

    def menu_animation(self, cells):
        for cell in cells:
            cell_rect = cell[0]*30, cell[1]*30, 30, 30
            self.cell(cell_rect, self.data.colors[cell[2]])

    def button(self, rect, text,  param = {"color":(184,138,0) ,"border":4, "margin_x":15, "margin_y":5}):
        # PARAM: COLOR, BORDER, MARGIN
        pygame.draw.rect(self.data.screen, (255, 255, 255), rect)
        pygame.draw.rect(self.data.screen, param["color"], (rect[0] + param["border"], rect[1] + param["border"], rect[2] - 2*param["border"], rect[3] - 2*param["border"]))
        font = pygame.font.SysFont('Calibri', rect[3]-param["margin_y"])
        text_rendered = font.render(text, True, (0,0,0))
        self.data.screen.blit(text_rendered, (rect[0] +param["border"]+param["margin_x"],rect[1]+param["border"]+param["margin_y"]))

    def text(self, msg, x, y, size, color = (0,0,0)):
        font = pygame.font.SysFont('Calibri', size)
        text_rendered = font.render(msg, True, color)
        self.data.screen.blit(text_rendered, (x, y))

    def menu(self, rect, button_list, choose, cells, param={"color": (184, 138, 0), "border":4, "margin_x":50, "margin_y":5, "text_size":90, "size_y":70, "space":10}):
        # PARAM: COLOR, BORDER, MARGIN, TEXT_SIZE, SPACE, SIZE_Y
        # BUTTON_LIST - LIST OF DICT: TEXT
        self.data.screen.fill((0, 0, 0))
        self.menu_animation(cells)
        pygame.draw.rect(self.data.screen, (255, 255, 255), rect)
        pygame.draw.rect(self.data.screen, param["color"], (rect[0] + param["border"], rect[1] + param["border"], rect[2] - 2*param["border"], rect[3] - 2*param["border"]))
        pygame.draw.rect(self.data.screen, (255, 255, 255), (rect[0], rect[1], rect[2], rect[1] + param["text_size"] + 2*param["margin_y"]))
        pygame.draw.rect(self.data.screen, param["color"], (rect[0] + param["border"], rect[1] + param["border"]+ param["margin_y"], rect[2] - 2*param["border"], rect[1] + param["text_size"] + 2*param["margin_y"] - 2*param["border"]))
        font = pygame.font.SysFont('Calibri', param["text_size"])
        text_rendered = font.render("Menu", True, (0,0,0))
        self.data.screen.blit(text_rendered, (rect[0] + param["margin_x"],rect[1]+param["margin_y"]))
        i = rect[1] + param["text_size"] + 2*param["margin_y"]+param["space"] - 30
        counter = 1
        for button_p in button_list:
            button_rect = (rect[0]+param["margin_x"], i, rect[2]-param["margin_x"]-50, param["size_y"])
            if choose == counter:
                self.button(button_rect, button_p["text"], {"color":(0,255,0) ,"border":4, "margin_x":15, "margin_y":5})
            else:
                self.button(button_rect, button_p["text"])
            i += param["size_y"]+param["space"]
            counter += 1
        pygame.display.flip()

    def high_scores(self, rect, records, cells, param={"color": (184, 138, 0), "border":4, "margin_x":50, "margin_y":5, "text_size":90, "size_y":70, "space":10}):
        # PARAM: COLOR, BORDER, MARGIN, TEXT_SIZE, SPACE, SIZE_Y
        # BUTTON_LIST - LIST OF DICT: TEXT
        self.data.screen.fill((0, 0, 0))
        self.menu_animation(cells)
        pygame.draw.rect(self.data.screen, (255, 255, 255), rect)
        pygame.draw.rect(self.data.screen, param["color"], (rect[0] + param["border"], rect[1] + param["border"], rect[2] - 2*param["border"], rect[3] - 2*param["border"]))
        pygame.draw.rect(self.data.screen, (255, 255, 255), (rect[0], rect[1], rect[2], rect[1] + param["text_size"] + 2*param["margin_y"]))
        pygame.draw.rect(self.data.screen, param["color"], (rect[0] + param["border"], rect[1] + param["border"]+ param["margin_y"], rect[2] - 2*param["border"], rect[1] + param["text_size"] + 2*param["margin_y"] - 2*param["border"]))
        font = pygame.font.SysFont('Calibri', param["text_size"])
        text_rendered = font.render("Hall of fame", True, (0,0,0))
        self.data.screen.blit(text_rendered, (rect[0] + param["margin_x"],rect[1]+param["margin_y"]))
        counter = 1
        for record in records:
            self.text(str(counter)+". "+record[0], rect[0]+20, rect[1]+30 + 40*counter, 40)
            self.text(str(record[1]), rect[0]+320, rect[1]+30 + 40*counter, 40)
            counter += 1
        self.text("Esc - Main Menu", rect[0]+20, rect[1]+30 + 40*counter, 40)
        pygame.display.flip()

    def music_control(self, rect, music, choose, cells, param={"color": (184, 138, 0), "border":4, "margin_x":50, "margin_y":5, "text_size":90, "size_y":70, "space":10}):
        # PARAM: COLOR, BORDER, MARGIN, TEXT_SIZE, SPACE, SIZE_Y
        # BUTTON_LIST - LIST OF DICT: TEXT
        self.data.screen.fill((0, 0, 0))
        self.menu_animation(cells)
        pygame.draw.rect(self.data.screen, (255, 255, 255), rect)
        pygame.draw.rect(self.data.screen, param["color"], (rect[0] + param["border"], rect[1] + param["border"], rect[2] - 2*param["border"], rect[3] - 2*param["border"]))
        pygame.draw.rect(self.data.screen, (255, 255, 255), (rect[0], rect[1], rect[2], rect[1] + param["text_size"] + 2*param["margin_y"]))
        pygame.draw.rect(self.data.screen, param["color"], (rect[0] + param["border"], rect[1] + param["border"]+ param["margin_y"], rect[2] - 2*param["border"], rect[1] + param["text_size"] + 2*param["margin_y"] - 2*param["border"]))
        font = pygame.font.SysFont('Calibri', param["text_size"])
        text_rendered = font.render("Music", True, (0,0,0))
        self.data.screen.blit(text_rendered, (rect[0] + param["margin_x"],rect[1]+param["margin_y"]))
        if music:
            self.button((rect[0]+20, rect[1]+90, 120,70), "On", {"color":(0, 0, 255) ,"border":4, "margin_x":5, "margin_y":5})
        elif choose == 1:
            self.button((rect[0]+20, rect[1]+90, 120,70), "On", {"color":(0, 255, 0) ,"border":4, "margin_x":5, "margin_y":5})
        else:
            self.button((rect[0]+20, rect[1]+90, 120,70), "On", {"color":(184,138,0) ,"border":4, "margin_x":5, "margin_y":5})
        if not music:
            self.button((rect[0]+140, rect[1]+90, 120,70), "Off", {"color":(0, 0, 255) ,"border":4, "margin_x":5, "margin_y":5})
        elif choose == 2:
            self.button((rect[0]+140, rect[1]+90, 120,70), "Off", {"color":(0, 255, 0) ,"border":4, "margin_x":5, "margin_y":5})
        else:
            self.button((rect[0]+140, rect[1]+90, 120,70), "Off", {"color":(184,138,0) ,"border":4, "margin_x":5, "margin_y":5})
        self.text("Esc - Main Menu", rect[0]+20, rect[1]+190, 40)
        pygame.display.flip()

    def cell(self, rect, color, color_border = (255,255,255)):
        pygame.draw.rect(self.data.screen, color_border, rect)
        pygame.draw.rect(self.data.screen, color, (rect[0]+2,rect[1]+2,rect[2]-4, rect[3] - 4))

    def erase_line_animation(self, rect, lines, param = {"border":5}):
        if len(lines) == 0:
            return
        for k in range(2):
            for i in lines:
                heigth = rect[1]+param["border"]+ i*30
                width = rect[0]+param["border"]
                for j in range(len(self.data.table_content[i])):
                    self.cell((width, heigth, 30, 30), (255, 255, 255), (0, 0, 0))
                    width += 30
            pygame.display.flip()
            sleep(0.2)
            for i in lines:
                heigth = rect[1]+param["border"]+ i*30
                width = rect[0]+param["border"]
                for j in range(len(self.data.table_content[i])):
                    self.cell((width, heigth, 30, 30), self.data.colors[self.data.table_colors[i][j]])
                    width += 30
            pygame.display.flip()
            sleep(0.2)

    def message(self, rect, text):
        self.add_panel(rect, (255, 255, 255), {"border": 2, "cborder": (0, 0, 0)})
        self.text(text, rect[0]+10, rect[1]+50, 100)

    def add_panel(self, rect, color, param={"border":5, "cborder":(255, 255, 255)}):
        pygame.draw.rect(self.data.screen, param["cborder"], rect)
        rect_content = (
        rect[0] + param["border"], rect[1] + param["border"], rect[2] - 2 * param["border"], rect[3] - 2 * param["border"])
        pygame.draw.rect(self.data.screen, color, rect_content)

    def pause(self):
        rect = (160, 150, 400, 200)
        self.add_panel(rect, (255, 255, 255), {"border": 2, "cborder": (0, 0, 0)})
        self.text("Pause", rect[0]+10, rect[1]+10, 100)
        self.text("p - Resume", rect[0]+10, rect[1]+110, 40)
        self.text("Esc - Menu", rect[0]+10, rect[1]+155, 40)
        pygame.display.flip()

    def game(self, rect,  param = {"border":5}):
        self.data.screen.fill((0, 0, 0))
        self.add_panel(rect, (0, 255, 0))
        self.add_panel((455, 50, 210, 610), (194, 178, 128))
        #NEXT BLOCK SPACE
        self.text("Next block:", 467, 58, 45, (0, 255, 0))
        self.text("Result:", 467, 235, 45, (0, 255, 0))
        self.add_panel((467, 275, 180, 50), (0, 0, 0), {"border":2, "cborder":(255, 255, 255)})
        self.text(str(self.data.score), 470, 280, 40, (0, 255, 0))
        self.text("Lines   : " +str(self.data.lines), 467, 335, 45, (0, 255, 0))
        self.text("Level   : " +str(self.data.level), 467, 375, 45, (0, 255, 0))
        self.text("Speed : " +str( round(1.0/self.data.time, 2)), 467, 415, 45, (0, 255, 0))
        self.text("Esc - Menu", 467, 565, 45, (0, 255, 0))
        self.text("p - Pause", 467, 605, 45, (0, 255, 0))
        rect_new_block = (495, 100, 130, 130)
        self.add_panel(rect_new_block, (0, 255, 0))
        heigth = 100+param["border"]
        width = 495+param["border"]
        for i in self.data.table_next_block:
            for j in i:
                if j:
                    self.cell((width, heigth, 30, 30), self.data.colors[self.data.next_block_param["color"]])
                width += 30
            heigth +=30
            width = 495+param["border"]
        #END NEXT BLOCK SPACE
        heigth = rect[1]+param["border"]
        width = rect[0]+param["border"]
        for i in self.data.table:
            for j in i:
                if j:
                    self.cell((width, heigth, 30, 30), self.data.colors[self.data.block_param["color"]])
                width += 30
            heigth +=30
            width = rect[0]+param["border"]
        heigth = rect[1]+param["border"]
        width = rect[0]+param["border"]
        k = 0
        l = 0
        for i in self.data.table_content:
            for j in i:
                if j:
                    self.cell((width, heigth, 30, 30), self.data.colors[self.data.table_colors[k][l]])
                width += 30
                l += 1
            heigth +=30
            k += 1
            width = rect[0]+param["border"]
            l = 0
        pygame.display.flip()
