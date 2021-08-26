import numpy as np
# import pygame
import sys
import math

from Board import Board
from Piece import Piece
from BoardPiece import BoardPiece

class BoardController:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.board = Board(self.rows, self.cols)

	def get_rowcols(self):
		return self.rows, self.cols

	def set_board(self, board):
		self.board.set_specific_board(board)

	def get_board(self):
		return self.board.get_board_values()

	def drop_piece(self, col, player):
		if self.valid_position(col):
			row = self.get_available_row(col)
			if player == 1:
				self.board.put_piece(row, col, Piece.RED)
			elif player == 2:
				self.board.put_piece(row, col, Piece.YELLOW)


	def valid_position(self, col):
		bp = self.board.get_position(0, col)
		if bp.get_piece_color() == Piece.BLACK.value:
			return True
		else:
			return False

	def get_available_row(self, col):
		for r in range(self.rows-1, -1, -1):
			bp = self.board.get_position(r, col)
			if bp.get_piece_color() == Piece.BLACK.value:
				return r

	def check_draw(self):
		board_values = self.board.get_board_values()
		for c in range(self.cols):
			col_used = self.valid_position(c)
			if col_used == True:
				return False
		return True


	def check_winner(self, last_move):

		for ind_r, r in enumerate(self.board.get_board_values()):
			for ind_c, c in enumerate(r):
				if self.board.get_position(ind_r, ind_c).get_piece_color() == last_move:

					if self.check_horizontal(ind_r, ind_c, last_move) or \
						self.check_vertical(ind_r, ind_c, last_move) or \
						self.check_diagonal(ind_r, ind_c, last_move):
							return last_move
		return False

	def check_horizontal(self, row, col, color):
		last_piece = Piece.BLACK
		inline = 0
		for i in range(-3, 4, 1):
			# print('\ncoord:', row, col, i, col+i)
			# print(i < 0, col + i >= 0, i >= 0, col + i < self.cols)
			if (i < 0 and col + i >= 0) or (i >= 0 and col + i < self.cols):
				p = self.board.get_position(row, col+i).get_piece()
				# print('last piece', last_piece, p, p==last_piece)
				if last_piece != p:
					last_piece = p
					inline = 0

				# print('value color', p.value, color, p.value == color)
				if p.value == color:
					inline += 1

				# print('inline', inline)
				if inline >= 4:
					# print('horiz')
					return True

		return False

	def check_vertical(self, row, col, color):
		last_piece = Piece.BLACK
		inline = 0
		for i in range(-3, 4, 1):
			if (i < 0 and row + i >= 0) or (i >= 0 and row + i < self.rows):
				p = self.board.get_position(row+i, col).get_piece()
				if last_piece != p:
					last_piece = p
					inline = 0

				if p.value == color:
					inline += 1

				if inline >= 4:
					# print('vert')
					return True

		return False

	def check_diagonal(self, row, col, color):
		# 1 down right
		last_piece = Piece.BLACK
		inline = 0
		for i in range(-3, 4, 1):
			if ((i < 0 and row + i >= 0) or (i >= 0 and row + i < self.rows)) and \
			((i < 0 and col + i >= 0) or (i >= 0 and col + i < self.cols)):

				p = self.board.get_position(row+i, col+i).get_piece()
				if last_piece != p:
					last_piece = p
					inline = 0

				if p.value == color:
					inline += 1

				if inline >= 4:
					# print('diag dr')
					return True

		# 2 down left
		last_piece = Piece.BLACK
		inline = 0
		for i in range(-3, 4, 1):
			if ((i < 0 and row + i >= 0) or (i >= 0 and row + i < self.rows)) and \
			((i > 0 and col - i >= 0) or (i <= 0 and col - i < self.cols)):

				p = self.board.get_position(row+i, col-i).get_piece()
				if last_piece != p:
					last_piece = p
					inline = 0

				if p.value == color:
					inline += 1

				if inline >= 4:
					# print('diag dl')
					return True

		return False
