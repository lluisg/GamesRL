import numpy as np
# import pygame
import sys
import math

from Piece import Piece
from UIBoard import UIBoard
from pygame.locals import *


class Player:
    def __init__(self, b_control, pygame, ui):
        self.b_controller = b_control
        self.i_rows, self.i_cols = b_control.get_rowcols()
        self.i_rows -= 1
        self.i_cols -= 1
        self.game = pygame
        self.pos_piece = 3
        self.ui = ui

    def move(self):
        for event in self.game.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_LEFT:
                    movements, merged = self.b_controller.move_left()
                    print('movements: {}, reward: {}'.format(movements, merged))
                    if movements > 0:
                        return True
                elif event.key == K_RIGHT:
                    movements, merged = self.b_controller.move_right()
                    print('movements: {}, reward: {}'.format(movements, merged))
                    if movements > 0:
                        return True
                elif event.key == K_UP:
                    movements, merged = self.b_controller.move_up()
                    print('movements: {}, reward: {}'.format(movements, merged))
                    if movements > 0:
                        return True
                elif event.key == K_DOWN:
                    movements, merged = self.b_controller.move_down()
                    print('movements: {}, reward: {}'.format(movements, merged))
                    if movements > 0:
                        return True

            elif event.type == self.game.QUIT:
                return False

        return None

    def wait_to_reestart(self):
        for event in self.game.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
            elif event.type == self.game.QUIT:
                return False

        return True
