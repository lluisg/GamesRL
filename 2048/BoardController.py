import numpy as np
# import pygame
import sys
import math
# from random import random
import random

from Board import Board
from Piece import Piece
from Piece import Piece

class BoardController:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.board = Board(self.rows, self.cols)

	def get_rowcols(self):
		return self.rows, self.cols

	def set_board(self, new_board):
		for ind_r, r in enumerate(new_board):
			for ind_c, c in enumerate(r):
				self.board.put_piece(ind_r, ind_c, Piece(c))

	def get_board(self):
		return self.board.get_board_values()

	def get_score(self):
		b = self.board.get_board_values()

		sum = 0
		for r in b:
			for c in r:
				sum += c
		return sum

	def appear_piece(self):
		empty_r, empty_c = self.board.get_empty_pos()
		random_ind = random.randint(0, len(empty_r)-1)

		random_value = random.randint(1,10)
		if random_value <= 9: # 90% value 2
			random_value = 2
		else: # 10% value 4
			random_value = 4

		# print(empty_r, empty_c, random_ind, random_value)

		self.board.put_piece(empty_r[random_ind], empty_c[random_ind], Piece(random_value))
		return empty_r[random_ind], empty_c[random_ind]

	def reestart_board(self):
		for r in range(self.rows):
			for c in range(self.cols):
				self.board.put_piece(r, c, Piece())

	def no_moves(self):
		#FOR NOW ONLY CHECKS IF FULL, LATER CHECK MOVEMENTS
		for r in range(self.rows):
			for c in range(self.cols):
				if self.board.get_piece(r, c).get_value() == 0:
					return False
		return True

	def move_left(self):
		movements = 0
		try:
			for r in range(self.rows):
				merged_row = False
				for c in range(self.cols):
					if c != 0: # ignore the pieces on position 0 that will not move
						if self.board.get_piece(r, c).get_value() != 0:
							# print('-----')
							piece_c = c
							while(self.board.get_piece(r, piece_c-1).get_value() == 0):
								self.board.move_piece(r, piece_c, r, piece_c-1)
								# print('moving ({}, {}) to ({}, {})'.format(r,piece_c, r,piece_c-1))

								movements += 1
								piece_c -= 1
								if piece_c == 0:
									break

							if merged_row == False and piece_c != 0:

								# b_values = self.get_board()
								# print(np.matrix(b_values))

								if self.can_be_merged(r, piece_c-1, r, piece_c):
									# print('merged')
									self.board.merge_pieces(r, piece_c-1, r, piece_c)
									merged_row = True
									movements += 1
			return movements

		except ValueError as ve:
			print(str(ve))
			return 0

	def move_right(self):
		movements = 0
		try:
			for r in range(self.rows):
				merged_row = 0
				for c in range(self.cols-1, -1, -1):
					if c != self.cols-1:
						if self.board.get_piece(r, c).get_value() != 0:
							piece_c = c
							while(self.board.get_piece(r, piece_c+1).get_value() == 0):
								self.board.move_piece(r, piece_c, r, piece_c+1)

								movements += 1
								piece_c += 1
								if piece_c == self.cols-1:
									break

							if merged_row == False and piece_c != self.cols-1:
								if self.can_be_merged(r, piece_c+1, r, piece_c):
									self.board.merge_pieces(r, piece_c+1, r, piece_c)
									merged_row = True
									movements += 1
			return movements

		except ValueError as ve:
			print(str(ve))
			return 0

	def move_up(self):
		movements = 0
		try:
			for c in range(self.cols):
				merged_col = 0
				for r in range(self.rows):
					if r != 0:
						if self.board.get_piece(r, c).get_value() != 0:
							piece_r = r
							while(self.board.get_piece(piece_r-1, c).get_value() == 0):
								self.board.move_piece(piece_r, c, piece_r-1, c)

								movements += 1
								piece_r -= 1
								if piece_r == 0:
									break

							if merged_col == False and piece_r != 0:
								if self.can_be_merged(piece_r-1, c, piece_r, c):
									self.board.merge_pieces(piece_r-1, c, piece_r, c)
									merged_col = True
									movements += 1
			return movements

		except ValueError as ve:
			print(str(ve))
			return 0

	def move_down(self):
		movements = 0
		try:
			for c in range(self.cols):
				merged_col = 0
				for r in range(self.rows-1, -1, -1):
					if r != self.rows-1:
						if self.board.get_piece(r, c).get_value() != 0:
							piece_r = r
							while(self.board.get_piece(piece_r+1, c).get_value() == 0):
								self.board.move_piece(piece_r, c, piece_r+1, c)

								movements += 1
								piece_r += 1
								if piece_r == self.cols-1:
									break

							if merged_col == False and piece_c != self.cols-1:
								if self.can_be_merged(piece_r+1, c, piece_r, c):
									self.board.merge_pieces(piece_r+1, c, piece_r, c)
									merged_col = True
									movements += 1
			return movements

		except ValueError as ve:
			print(str(ve))
			return 0

	def can_be_merged(self, row1, col1, row2, col2):
		val1 = self.board.get_piece(row1, col1).get_value()
		val2 = self.board.get_piece(row2, col2).get_value()

		if val1 == val2:
			return True
		return False

	# def drop_piece(self, col, player):
	# 	if self.valid_position(col):
	# 		row = self.get_available_row(col)
	# 		if player == 1:
	# 			self.board.put_piece(row, col, Piece.RED)
	# 		elif player == 2:
	# 			self.board.put_piece(row, col, Piece.YELLOW)
	#
	#
	# def valid_position(self, col):
	# 	bp = self.board.get_position(0, col)
	# 	if bp.get_piece_color() == Piece.BLACK.value:
	# 		return True
	# 	else:
	# 		return False
	#
	# def get_available_row(self, col):
	# 	for r in range(self.rows-1, -1, -1):
	# 		bp = self.board.get_position(r, col)
	# 		if bp.get_piece_color() == Piece.BLACK.value:
	# 			return r
	#
	# def check_draw(self):
	# 	board_values = self.board.get_board_values()
	# 	for c in range(self.cols):
	# 		col_used = self.valid_position(c)
	# 		if col_used == True:
	# 			return False
	# 	return True
	#
	#
	# def check_winner(self, last_move):
	#
	# 	for ind_r, r in enumerate(self.board.get_board_values()):
	# 		for ind_c, c in enumerate(r):
	# 			if self.board.get_position(ind_r, ind_c).get_piece_color() == last_move:
	#
	# 				if self.check_horizontal(ind_r, ind_c, last_move) or \
	# 					self.check_vertical(ind_r, ind_c, last_move) or \
	# 					self.check_diagonal(ind_r, ind_c, last_move):
	# 						return last_move
	# 	return False
	#
	# def check_horizontal(self, row, col, color):
	# 	last_piece = Piece.BLACK
	# 	inline = 0
	# 	for i in range(-3, 4, 1):
	# 		# print('\ncoord:', row, col, i, col+i)
	# 		# print(i < 0, col + i >= 0, i >= 0, col + i < self.cols)
	# 		if (i < 0 and col + i >= 0) or (i >= 0 and col + i < self.cols):
	# 			p = self.board.get_position(row, col+i).get_piece()
	# 			# print('last piece', last_piece, p, p==last_piece)
	# 			if last_piece != p:
	# 				last_piece = p
	# 				inline = 0
	#
	# 			# print('value color', p.value, color, p.value == color)
	# 			if p.value == color:
	# 				inline += 1
	#
	# 			# print('inline', inline)
	# 			if inline >= 4:
	# 				# print('horiz')
	# 				return True
	#
	# 	return False
	#
	# def check_vertical(self, row, col, color):
	# 	last_piece = Piece.BLACK
	# 	inline = 0
	# 	for i in range(-3, 4, 1):
	# 		if (i < 0 and row + i >= 0) or (i >= 0 and row + i < self.rows):
	# 			p = self.board.get_position(row+i, col).get_piece()
	# 			if last_piece != p:
	# 				last_piece = p
	# 				inline = 0
	#
	# 			if p.value == color:
	# 				inline += 1
	#
	# 			if inline >= 4:
	# 				# print('vert')
	# 				return True
	#
	# 	return False
	#
	# def check_diagonal(self, row, col, color):
	# 	# 1 down right
	# 	last_piece = Piece.BLACK
	# 	inline = 0
	# 	for i in range(-3, 4, 1):
	# 		if ((i < 0 and row + i >= 0) or (i >= 0 and row + i < self.rows)) and \
	# 		((i < 0 and col + i >= 0) or (i >= 0 and col + i < self.cols)):
	#
	# 			p = self.board.get_position(row+i, col+i).get_piece()
	# 			if last_piece != p:
	# 				last_piece = p
	# 				inline = 0
	#
	# 			if p.value == color:
	# 				inline += 1
	#
	# 			if inline >= 4:
	# 				# print('diag dr')
	# 				return True
	#
	# 	# 2 down left
	# 	last_piece = Piece.BLACK
	# 	inline = 0
	# 	for i in range(-3, 4, 1):
	# 		if ((i < 0 and row + i >= 0) or (i >= 0 and row + i < self.rows)) and \
	# 		((i > 0 and col - i >= 0) or (i <= 0 and col - i < self.cols)):
	#
	# 			p = self.board.get_position(row+i, col-i).get_piece()
	# 			if last_piece != p:
	# 				last_piece = p
	# 				inline = 0
	#
	# 			if p.value == color:
	# 				inline += 1
	#
	# 			if inline >= 4:
	# 				# print('diag dl')
	# 				return True
	#
	# 	return False
