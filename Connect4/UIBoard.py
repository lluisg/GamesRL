import numpy as np
from BoardController import BoardController

import pygame
import math


class UIBoard:
    def __init__(self, bcontrol, area, pygame, screen):
        self.b_controller = bcontrol
        self.rows, self.cols = bcontrol.get_rowcols()
        self.area = area
        self.width, self.height = area

        self.game = pygame
        self.screen = screen
        self.font = self.game.font.Font(None, 60)
        # self.font = self.game.font.SysFont('Arial', 25)
        self.RECT_upperscreen = pygame.Rect(0, 0, self.width, self.height / 3)

        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)

        self.indices_colors = {	0: self.BLACK, 1: self.RED, 2: self.YELLOW	}

        self.time = 0
        self.moves = 0

    def set_time_moves(self, t, m):
        self.time = t
        self.moves = m

    def print_board_values(self, indexs):

        b_values = self.b_controller.get_board()
        if indexs:
            a = [1, 2, 3, 4, 5, 6, 7]
            print(np.matrix(a))
        print(np.matrix(b_values))

    def print_base_screen(self):
        board = self.b_controller.get_board()

        self.screen.fill(self.BLACK)
        # the +1 to add a line above to see the intention of the player
        self.game.draw.rect(self.screen, self.BLUE, (0, self.height * 1 / (self.rows + 1),
                                                     self.width, self.height * self.rows / (self.rows + 1)))

        for ind_r, r in enumerate(board):
            for ind_c, c in enumerate(r):
                x_pos = self.width / self.cols / 2 + ind_c * self.width / self.cols
                y_pos = self.height / (self.rows + 1) / 2 + \
                    (ind_r + 1) * self.height / (self.rows + 1)
                # print(ind_r, ind_c, x_pos, y_pos)

                self.game.draw.circle(self.screen, self.indices_colors[c], (x_pos, y_pos), min(
                    self.width / self.cols, self.height / (self.rows + 1)) / 2)

        #time
        text_score = self.font_score.render(self.time, 0, self.GRAY)
        textRect = text_score.get_rect()
        textRect.left = self.width - white_borderx*2
        textRect.centery = self.height - white_bordery/2
        self.screen.blit(text_score, textRect)

        #moves
        text_score = self.font_score.render("{} moves".format(self.moves), 0, self.GRAY)
        textRect = text_score.get_rect()
        textRect.x = white_borderx
        textRect.centery = self.height - white_bordery/2
        self.screen.blit(text_score, textRect)

        self.game.display.update()

    def print_player_screen(self, player, column):
        self.print_base_screen()
        row = 0

        x_pos = self.width / self.cols / 2 + column * self.width / self.cols
        y_pos = self.height / (self.rows + 1) / 2 + \
            row * self.height / (self.rows + 1)
        self.game.draw.circle(self.screen, self.indices_colors[player], (x_pos, y_pos), min(
            self.width / self.cols, self.height / (self.rows + 1)) / 2)

        self.game.display.update(self.RECT_upperscreen)

    def print_drop_piece(self, player, column):

        row = self.b_controller.get_available_row(column)
        x_pos = self.width / self.cols / 2 + column * self.width / self.cols
        self.RECT_columnscreen = self.game.Rect(
            column * self.width / self.cols, 0, self.width / self.cols, self.height)  # only update the column necesary

        for r in range(1, row + 2):
            self.game.time.delay(50)  # 1s each
            y_pos = self.height / (self.rows + 1) / 2 + \
                r * self.height / (self.rows + 1)

            self.print_base_screen()
            self.game.draw.circle(self.screen, self.indices_colors[player], (x_pos, y_pos), min(
                self.width / self.cols, self.height / (self.rows + 1)) / 2)
            self.game.display.update(self.RECT_columnscreen)

    def print_wrongdrop(self, player, column):
        self.print_base_screen()
        row = 0

        x_pos = self.width / self.cols / 2 + column * self.width / self.cols
        y_pos = self.height / (self.rows + 1) / 2 + \
            row * self.height / (self.rows + 1)
        self.game.draw.circle(self.screen, self.BLUE, (x_pos, y_pos), min(
            self.width / self.cols, self.height / (self.rows + 1)) / 2)

        self.game.display.update(self.RECT_upperscreen)
        self.game.time.wait(100)
        self.print_player_screen(player, column)

    def print_ending(self, text, color_text):
        self.print_base_screen()
        center_screen_x = self.width / 2
        center_screen_y = self.height / 2

        self.game.draw.rect(self.screen, self.WHITE,
                            (self.width / 4 - 1, self.height * 3 / 8 - 1, self.width / 2 + 2, self.height / 4 + 2))
        self.game.draw.rect(self.screen, self.BLACK,
                            (self.width / 4, self.height * 3 / 8, self.width / 2, self.height / 4))

        text_o = self.textOutline(self.font, text, color_text, self.WHITE)

        textRect = text_o.get_rect()
        textRect.center = (self.width / 2, self.height / 2)
        self.screen.blit(text_o, textRect)
        self.game.display.update()

    def print_winner(self, player):
        text = 'PLAYER {} WINS!!'.format(player)
        self.print_ending(text, self.indices_colors[player])

    def print_draw(self):
        text = 'DRAW ...'
        self.print_ending(text, self.BLUE)

    def textOutline(self, font, message, fontcolor, outlinecolor):
        base = font.render(message, 0, fontcolor)
        outline = self.textHollow(font, message, outlinecolor)
        img = self.game.Surface(outline.get_size(), 16)
        img.blit(base, (1, 1))
        img.blit(outline, (0, 0))
        img.set_colorkey(0)
        return img

    def textHollow(self, font, message, fontcolor):
        notcolor = [c ^ 0xFF for c in fontcolor]
        base = font.render(message, 0, fontcolor, notcolor)
        size = base.get_width() + 2, base.get_height() + 2
        img = self.game.Surface(size, 16)
        img.fill(notcolor)
        base.set_colorkey(0)
        img.blit(base, (0, 0))
        img.blit(base, (2, 0))
        img.blit(base, (0, 2))
        img.blit(base, (2, 2))
        base.set_colorkey(0)
        base.set_palette_at(1, notcolor)
        img.blit(base, (1, 1))
        img.set_colorkey(notcolor)
        return img
