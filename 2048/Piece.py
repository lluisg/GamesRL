
class Piece:
    def __init__(self):
        self.value = 0

    def set_piece(self, value):
        self.value = value

    def get_piece(self):
        return self.value

    def piece_upgrade(self):
        self.value = self.value^2

    def piece_remove(self):
        self.value = 0
