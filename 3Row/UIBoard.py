import numpy as np
import os

class UIBoard:
    def __init__(self, bcontrol):
        self.b_controller = bcontrol

    def print_board_values(self):
        board = self.b_controller.get_board_values()
        print(np.matrix(board))

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
