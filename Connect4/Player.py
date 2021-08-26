import numpy as np
# import pygame
import sys
import math

from Piece import Piece
from UIBoard import UIBoard
from pygame.locals import *

class Player:
	def __init__(self, player, b_control, pygame, ui):
		self.player = player
		if player == 1:
			self.piece = Piece.RED
		elif player == 2:
			self.piece = Piece.YELLOW
		else:
			print('ONLY 2 POSSIBLE PLAYERS!!')

		self.b_controller = b_control
		self.i_rows, self.i_cols = b_control.get_rowcols()
		self.i_rows -= 1
		self.i_cols -= 1
		self.game = pygame
		self.pos_piece = 0
		self.ui = ui

	def move(self):

		for event in self.game.event.get():

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return False
				elif event.key == K_LEFT:
					self.pos_piece = max(0, self.pos_piece-1)
					self.ui.print_player_screen(self.player, self.pos_piece)
				elif event.key == K_RIGHT:
					self.pos_piece = min(self.pos_piece+1, self.i_cols)
					self.ui.print_player_screen(self.player, self.pos_piece)
				elif event.key == K_RETURN :
					self.ui.print_drop_piece(self.player, self.pos_piece)
					self.b_controller.drop_piece(self.pos_piece, self.player)
					self.pos_piece = 0
					return True
			elif event.type == self.game.QUIT:
				return False

		return None


	def wait_to_reestart(self):
		for event in self.game.event.get():

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return False
				elif event.key == K_RETURN :
					return True
			elif event.type == self.game.QUIT:
				return False

		return None
