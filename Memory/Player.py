# -*- coding: utf-8 -*-

import numpy as np
# import pygame
import sys
import math

from Piece import Piece
# from UIBoard import UIBoard
# from pygame.locals import *

class Player(object):
    def __init__(self, player, b_control, pygame, ui, points = 0):
        self.setNumPlayer(player)
        self.setPoints(points)

        self.b_controller = b_control

        self.i_rows, self.i_cols = b_control.GetRowCols()
        self.i_rows -= 1
        self.i_cols -= 1

        # self.game = pygame
        # self.pos_piece = 3
        # self.ui = ui

    def setNumPlayer(self, num_player):
        self.num_player = num_player

    def getNumPlayer(self):
        return self.num_player

    def setPoints(self, points):
        self.points = points

    def getPoints(self):
        return self.points

    def move(self):

        # for event in self.game.event.get():
        #
        #     if event.type == KEYDOWN:
        #         if event.key == K_ESCAPE:
        #             return False
        #         elif event.key == K_LEFT:
        #             self.pos_piece = max(0, self.pos_piece - 1)
        #             self.ui.print_player_screen(self.player, self.pos_piece)
        #         elif event.key == K_RIGHT:
        #             self.pos_piece = min(self.pos_piece + 1, self.i_cols)
        #             self.ui.print_player_screen(self.player, self.pos_piece)
        #         elif event.key == K_RETURN:
        #             if self.b_controller.valid_position(self.pos_piece):
        #                 self.ui.print_drop_piece(self.player, self.pos_piece)
        #                 self.b_controller.drop_piece(self.pos_piece, self.player)
        #                 self.pos_piece = 3
        #                 return True
        #             else:
        #                 self.ui.print_wrongdrop(self.player, self.pos_piece)
        #     elif event.type == self.game.QUIT:
        #         return False
        while True:
            row, col = self.AskPosition(1)
            fliped = self.b_controller.FlipPosition(row, col)
            valid_fliped = self.ValidFliped(fliped)
            if valid_fliped:
                break

        print self.b_controller.ReturnValuesPlay()
        while True:
            row, col = self.AskPosition(2)
            fliped2 = self.b_controller.FlipPosition(row, col)
            valid_fliped = self.ValidFliped(fliped2)
            if valid_fliped:
                break

        print self.b_controller.ReturnValuesPlay()
        return True

    def ValidFliped(self, flip):
        if flip == 'found':
            print 'Invalid: that piece was already found'
            return False
        elif flip == 'visible':
            print 'Invalid: that piece was already visible'
            return False
        elif flip == 'pos':
            print 'Invalid: that position is outside the board'
            return False
        elif flip is None:
            print 'Invalid'
            return False
        return True

    def AskPosition(self, move=1):
        # if move == 1: return 2,1
        # else:   return 2,0

        while True:
            print 'Input position to flip ('+str(move)+') rowcol:'
            pos = str(input())
            if len(pos) == 1: pos = '0'+pos
            try:
                row = int(pos[0])
                col = int(pos[1])
                break
            except:
                print 'Invalid position format'
                pass

        return row, col
