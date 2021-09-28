import random
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

    def get_sumvalues(self):
        b = self.board.get_board_values()

        sum = 0
        for r in b:
            for c in r:
                sum += c
        return sum

    def new_line(self):
        self.next_level()
        self.board.remove_last_line()
        self.board.add_line(self.level)

    def check_lost(self):
        b = self.get_board()
        for c in range(self.cols):
            # isinstance( < var >, int)
            p = b.get_piece(self.rows-1, c).get_value()
            if p != 0:
                return True
        return False

    def get_level(self):
        return self.level

    def next_level(self):
        self.level += 1






    def appear_piece(self):
        empty_r, empty_c = self.board.get_empty_pos()
        random_ind = random.randint(0, len(empty_r) - 1)

        random_value = random.randint(1, 10)
        if random_value <= 9:  # 90% value 2
            random_value = 2
        else:  # 10% value 4
            random_value = 4

        # print(empty_r, empty_c, random_ind, random_value)

        self.board.put_piece(empty_r[random_ind], empty_c[random_ind], Piece(random_value))
        return empty_r[random_ind], empty_c[random_ind]

    def reestart_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.board.put_piece(r, c, Piece())

    def check_nomoves(self):
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.board.get_piece(r, c).get_value()
                if value == 0:
                    return False

                if r != 0:
                    value_up = self.board.get_piece(r - 1, c).get_value()
                    if value_up == value:
                        return False
                if c != 0:
                    value_left = self.board.get_piece(r, c - 1).get_value()
                    if value_left == value:
                        return False
        return True

    def check_winner(self):
        b = self.get_board_values()
        for r in b:
            for c in r:
                if c == 2048:
                    return True
        return False

    def move_left(self):
        movements = 0
        merged_values = 0
        try:
            for r in range(self.rows):
                merged_row = False
                for c in range(self.cols):
                    if c != 0:  # ignore the pieces on position 0 that will not move
                        if self.board.get_piece(r, c).get_value() != 0:
                            # print('-----')
                            piece_c = c
                            while (self.board.get_piece(r, piece_c - 1).get_value() == 0):
                                self.board.move_piece(r, piece_c, r, piece_c - 1)
                                # print('moving ({}, {}) to ({}, {})'.format(r,piece_c, r,piece_c-1))

                                movements += 1
                                piece_c -= 1
                                if piece_c == 0:
                                    break

                            if merged_row == False and piece_c != 0:

                                # b_values = self.get_board()
                                # print(np.matrix(b_values))

                                if self.can_be_merged(r, piece_c - 1, r, piece_c):
                                    # print('merged')
                                    m_value = self.board.merge_pieces(r, piece_c - 1, r, piece_c)
                                    merged_row = True
                                    movements += 1
                                    merged_values += m_value

            return movements, merged_values

        except ValueError as ve:
            print(str(ve))
            return 0

    def move_right(self):
        movements = 0
        merged_values = 0
        try:
            for r in range(self.rows):
                merged_row = False
                for c in range(self.cols - 1, -1, -1):
                    if c != self.cols - 1:
                        if self.board.get_piece(r, c).get_value() != 0:
                            piece_c = c
                            while (self.board.get_piece(r, piece_c + 1).get_value() == 0):
                                self.board.move_piece(r, piece_c, r, piece_c + 1)

                                movements += 1
                                piece_c += 1
                                if piece_c == self.cols - 1:
                                    break

                            if merged_row == False and piece_c != self.cols - 1:
                                if self.can_be_merged(r, piece_c + 1, r, piece_c):
                                    m_value = self.board.merge_pieces(r, piece_c + 1, r, piece_c)
                                    merged_row = True
                                    movements += 1
                                    merged_values += m_value

            return movements, merged_values

        except ValueError as ve:
            print(str(ve))
            return 0

    def move_up(self):
        movements = 0
        merged_values = 0
        try:
            for c in range(self.cols):
                merged_col = False
                for r in range(self.rows):
                    if r != 0:
                        if self.board.get_piece(r, c).get_value() != 0:
                            piece_r = r
                            while (self.board.get_piece(piece_r - 1, c).get_value() == 0):
                                self.board.move_piece(piece_r, c, piece_r - 1, c)

                                movements += 1
                                piece_r -= 1
                                if piece_r == 0:
                                    break

                            if merged_col == False and piece_r != 0:
                                if self.can_be_merged(piece_r - 1, c, piece_r, c):
                                    m_value = self.board.merge_pieces(piece_r - 1, c, piece_r, c)
                                    merged_col = True
                                    movements += 1
                                    merged_values += m_value

            return movements, merged_values

        except ValueError as ve:
            print(str(ve))
            return 0

    def move_down(self):
        movements = 0
        merged_values = 0
        try:
            for c in range(self.cols):
                merged_col = False
                for r in range(self.rows - 1, -1, -1):
                    if r != self.rows - 1:
                        if self.board.get_piece(r, c).get_value() != 0:
                            piece_r = r
                            while (self.board.get_piece(piece_r + 1, c).get_value() == 0):
                                self.board.move_piece(piece_r, c, piece_r + 1, c)

                                movements += 1
                                piece_r += 1
                                if piece_r == self.cols - 1:
                                    break

                            if merged_col == False and piece_r != self.cols - 1:
                                if self.can_be_merged(piece_r + 1, c, piece_r, c):
                                    m_value = self.board.merge_pieces(piece_r + 1, c, piece_r, c)
                                    merged_col = True
                                    movements += 1
                                    merged_values += m_value

            return movements, merged_values

        except ValueError as ve:
            print(str(ve))
            return 0

    def can_be_merged(self, row1, col1, row2, col2):
        val1 = self.board.get_piece(row1, col1).get_value()
        val2 = self.board.get_piece(row2, col2).get_value()

        if val1 == val2:
            return True
        return False
