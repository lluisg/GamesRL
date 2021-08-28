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
        self.small_width = self.width * 14/16
        self.small_height = self.height * 14/16

        self.game = pygame
        self.screen = screen
        self.font_numbers = self.game.font.Font(None, 60)
        self.font_info = self.game.font.Font(None, 24)
        self.font_score = self.game.font.Font(None, 24)

        self.GRAY = (185, 173, 160)
        self.GRAY2 = (238, 228, 218)
        self.GRAY3 = (205, 196, 179)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.ORANGE = (242, 177, 121)
        self.ORANGE2 = (245, 149, 99)
        self.RED = (245, 124, 95)
        self.RED2 = (247, 94, 60)
        self.YELLOW = (236, 206, 115)
        self.YELLOW2 = (236, 200, 80)
        self.YELLOW3 = (237, 204, 97)
        self.YELLOW4 = (237, 197, 63)
        self.YELLOW5 = (238, 194, 46)

        self.values2colorsPiece = {	0: self.GRAY3,      2: self.GRAY2,      4: self.GRAY2,
                                    8: self.ORANGE,     16: self.ORANGE2,   32: self.RED,
                                    64: self.RED2,      128: self.YELLOW,   256: self.YELLOW2,
                                    512: self.YELLOW3,  1024: self.YELLOW4, 2048: self.YELLOW5 }
        self.values2colorsNumber = {0: self.WHITE,      2: self.BLACK,      4: self.BLACK,
                                    8: self.WHITE,      16: self.WHITE,     32: self.WHITE,
                                    64: self.WHITE,     128: self.WHITE,    256: self.WHITE,
                                    512: self.WHITE,    1024: self.WHITE,   2048: self.WHITE }

    def print_board_values(self):

        b_values = self.b_controller.get_board()
        print(np.matrix(b_values))

    def print_base_screen(self, time, moves):
        board = self.b_controller.get_board()

        self.screen.fill(self.WHITE)
        white_borderx = self.width*1/16
        white_bordery = self.height*1/16
        self.game.draw.rect(self.screen, self.GRAY, (white_borderx, white_bordery,
                                                    self.small_width, self.small_height))

        miniborderx = 1/32*self.small_width
        minibordery = 1/32*self.small_height
        #there will be 5 miniborders
        rectanglex = self.small_width*(32-5)/32 / self.cols
        rectangley = self.small_height*(32-5)/32 / self.rows
        for ind_r, r in enumerate(board):
            for ind_c, c in enumerate(r):
                x_pos =  white_borderx + (ind_c+1) * miniborderx + ind_c * rectanglex
                y_pos =  white_bordery + (ind_r+1) * minibordery + ind_r * rectangley

                rr = self.game.draw.rect(self.screen, self.values2colorsPiece[c], (x_pos, y_pos, rectanglex, rectangley), border_radius=3)

                if c != 0:
                    text_o = self.font_numbers.render(str(c), 0, self.values2colorsNumber[c])

                    textRect = text_o.get_rect()
                    textRect.center = (x_pos + rectanglex/2, y_pos + rectangley/2)
                    self.screen.blit(text_o, textRect)


        #score
        score = self.b_controller.get_score()
        text_score = self.font_score.render('Score: {}'.format(score), 0, self.BLACK)
        textRect = text_score.get_rect()
        textRect.x = white_borderx
        textRect.centery = white_bordery/2
        self.screen.blit(text_score, textRect)

        #time
        text_score = self.font_score.render(time, 0, self.GRAY)
        textRect = text_score.get_rect()
        textRect.left = self.width - white_borderx*2
        textRect.centery = self.height - white_bordery/2
        self.screen.blit(text_score, textRect)

        #moves
        text_score = self.font_score.render("{} moves".format(moves), 0, self.GRAY)
        textRect = text_score.get_rect()
        textRect.x = white_borderx
        textRect.centery = self.height - white_bordery/2
        self.screen.blit(text_score, textRect)

        self.game.display.update()


    def new_piece(self, row, col):
        PRINT THE NEW PIECES GETTING BIGGER






    #
    # def print_player_screen(self, player, column):
    #     self.print_base_screen()
    #     row = 0
    #
    #     x_pos = self.width / self.cols / 2 + column * self.width / self.cols
    #     y_pos = self.height / (self.rows + 1) / 2 + \
    #         row * self.height / (self.rows + 1)
    #     self.game.draw.circle(self.screen, self.indices_colors[player], (x_pos, y_pos), min(
    #         self.width / self.cols, self.height / (self.rows + 1)) / 2)
    #
    #     self.game.display.update(self.RECT_upperscreen)
    #
    # def print_drop_piece(self, player, column):
    #
    #     row = self.b_controller.get_available_row(column)
    #     x_pos = self.width / self.cols / 2 + column * self.width / self.cols
    #     self.RECT_columnscreen = self.game.Rect(
    #         column * self.width / self.cols, 0, self.width / self.cols, self.height)  # only update the column necesary
    #
    #     for r in range(1, row + 2):
    #         self.game.time.delay(50)  # 1s each
    #         y_pos = self.height / (self.rows + 1) / 2 + \
    #             r * self.height / (self.rows + 1)
    #
    #         self.print_base_screen()
    #         self.game.draw.circle(self.screen, self.indices_colors[player], (x_pos, y_pos), min(
    #             self.width / self.cols, self.height / (self.rows + 1)) / 2)
    #         self.game.display.update(self.RECT_columnscreen)
    #
    # def print_wrongdrop(self, player, column):
    #     self.print_base_screen()
    #     row = 0
    #
    #     x_pos = self.width / self.cols / 2 + column * self.width / self.cols
    #     y_pos = self.height / (self.rows + 1) / 2 + \
    #         row * self.height / (self.rows + 1)
    #     self.game.draw.circle(self.screen, self.BLUE, (x_pos, y_pos), min(
    #         self.width / self.cols, self.height / (self.rows + 1)) / 2)
    #
    #     self.game.display.update(self.RECT_upperscreen)
    #     self.game.time.wait(100)
    #     self.print_player_screen(player, column)
    #
    # def print_ending(self, text, color_text):
    #     self.print_base_screen()
    #     center_screen_x = self.width / 2
    #     center_screen_y = self.height / 2
    #
    #     self.game.draw.rect(self.screen, self.WHITE,
    #                         (self.width / 4 - 1, self.height * 3 / 8 - 1, self.width / 2 + 2, self.height / 4 + 2))
    #     self.game.draw.rect(self.screen, self.BLACK,
    #                         (self.width / 4, self.height * 3 / 8, self.width / 2, self.height / 4))
    #
    #     text_o = self.textOutline(self.font, text, color_text, self.WHITE)
    #
    #     textRect = text_o.get_rect()
    #     textRect.center = (self.width / 2, self.height / 2)
    #     self.screen.blit(text_o, textRect)
    #     self.game.display.update()
    #
    # def print_winner(self, player):
    #     text = 'PLAYER {} WINS!!'.format(player)
    #     self.print_ending(text, self.indices_colors[player])
    #
    # def print_draw(self):
    #     text = 'DRAW ...'
    #     self.print_ending(text, self.BLUE)
    #
    # def textOutline(self, font, message, fontcolor, outlinecolor):
    #     base = font.render(message, 0, fontcolor)
    #     outline = self.textHollow(font, message, outlinecolor)
    #     img = self.game.Surface(outline.get_size(), 16)
    #     img.blit(base, (1, 1))
    #     img.blit(outline, (0, 0))
    #     img.set_colorkey(0)
    #     return img
    #
    # def textHollow(self, font, message, fontcolor):
    #     notcolor = [c ^ 0xFF for c in fontcolor]
    #     base = font.render(message, 0, fontcolor, notcolor)
    #     size = base.get_width() + 2, base.get_height() + 2
    #     img = self.game.Surface(size, 16)
    #     img.fill(notcolor)
    #     base.set_colorkey(0)
    #     img.blit(base, (0, 0))
    #     img.blit(base, (2, 0))
    #     img.blit(base, (0, 2))
    #     img.blit(base, (2, 2))
    #     base.set_colorkey(0)
    #     base.set_palette_at(1, notcolor)
    #     img.blit(base, (1, 1))
    #     img.set_colorkey(notcolor)
    #     return img
