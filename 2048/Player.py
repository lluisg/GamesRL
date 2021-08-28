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
					movements = self.b_controller.move_left()
					print('movements:', movements)
					if movements > 0:
						return True
				elif event.key == K_RIGHT:
					movements = self.b_controller.move_right()
					print('movements:', movements)
					if movements > 0:
						return True
				elif event.key == K_UP:
					movements = self.b_controller.move_up()
					print('movements:', movements)
					if movements > 0:
						return True
				elif event.key == K_DOWN:
					movements = self.b_controller.move_down()
					print('movements:', movements)
					if movements > 0:
						return True
			elif event.type == self.game.QUIT:
				return False
		return None
		# for event in self.game.event.get():
		#
		# 	if event.type == KEYDOWN:
		# 		if event.key == K_ESCAPE:
		# 			return False
		# 		elif event.key == K_LEFT:
		# 			self.pos_piece = max(0, self.pos_piece - 1)
		# 			self.ui.print_player_screen(self.player, self.pos_piece)
		# 		elif event.key == K_RIGHT:
		# 			self.pos_piece = min(self.pos_piece + 1, self.i_cols)
		# 			self.ui.print_player_screen(self.player, self.pos_piece)
		# 		elif event.key == K_RETURN:
		# 			if self.b_controller.valid_position(self.pos_piece):
		# 				self.ui.print_drop_piece(self.player, self.pos_piece)
		# 				self.b_controller.drop_piece(self.pos_piece, self.player)
		# 				self.pos_piece = 3
		# 				return True
		# 			else:
		# 				self.ui.print_wrongdrop(self.player, self.pos_piece)
		# 	elif event.type == self.game.QUIT:
		# 		return False
		#
		# return None

	def wait_to_reestart(self):
		for event in self.game.event.get():

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return False
				# elif event.key == K_RETURN:
				# 	return True
			elif event.type == self.game.QUIT:
				return False

		return None
