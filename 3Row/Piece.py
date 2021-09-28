class Piece:
    def __init__(self, player = 0):
        self.player = player

    def set_player(self, player):
        self.player = player

    def get_player(self):
        return self.player
