import numpy as np
from Board import Board
from Piece import Piece

class BoardController:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.level = 1
        self.board = Board(self.rows, self.cols)

    def get_rowcols(self):
        return self.rows, self.cols

    def set_board(self, new_board):
        for ind_r, r in enumerate(new_board):
            for ind_c, c in enumerate(r):
                self.board.put_piece(ind_r, ind_c, Piece(c))

    def get_board_values(self):
        return self.board.get_board_values()

    def get_board(self):
        return self.board

    def put_piece(self, row,  col, player):
        if self.board.get_piece(row, col).get_player() != 0:
            return False

        self.board.put_piece(row, col, Piece(player))
        return True

    def check_winner(self, player):
        if self.check_horizontal(self.board, player) or self.check_vertical(self.board, player) or self.check_diagonal(self.board, player):
            return True
        return False

    def reestart_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.board.put_piece(r, c, Piece())

    def check_horizontal(self, board, player):
        for r in range(self.rows):
            if board.get_piece(r, 0).get_player() == player:
                if board.get_piece(r, 1).get_player() == player:
                    if board.get_piece(r, 2).get_player() == player:
                        return True
        return False

    def check_vertical(self, board, player):
        for c in range(self.cols):
            if board.get_piece(0, c).get_player() == player:
                if board.get_piece(1, c).get_player() == player:
                    if board.get_piece(2, c).get_player() == player:
                        return True
        return False

    def check_diagonal(self, board, player):
        for c in [0, 2]:
            # print c, '-', board.get_piece(0, c).get_player(), board.get_piece(1, 1).get_player(), board.get_piece(2, 2-c).get_player()
            if board.get_piece(0, c).get_player() == player:
                if board.get_piece(1, 1).get_player() == player:
                    if board.get_piece(2, 2-c).get_player() == player:
                        return True
        return False

    def check_nomoves(self):
        for c in range(self.cols):
            for r in range(self.rows):
                if self.board.get_piece(r, c).get_player() == 0:
                    return False
        return True

