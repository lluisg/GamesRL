from BoardController import BoardController

class Player:
    def __init__(self, number, bc):
        self.player = number
        self.b_controller = bc

    def get_number(self):
        return self.player

    def play_turn(self):

        validmove = False
        while not validmove:
            column = None
            row = None
            while column not in range(1, 4):
                print("Input a valid column (1-3):")
                column = int(input())
                # column = 1
            while row not in range(1, 4):
                print("Input a valid row (1-3):")
                row = int(input())
                # row = 3
            column -= 1
            row -= 1

            validmove = self.b_controller.put_piece(row, column, self.player)
            if not validmove:
                print('-- Please enter a valid move!!')

