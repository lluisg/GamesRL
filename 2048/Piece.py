
class Piece:
    def __init__(self, *args):
        if len(args) == 0:
            self.value = 0
        elif len(args) == 1:
            self.value = args[0]

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def value_upgrade(self):
        self.value *= 2

    def value_remove(self):
        self.value = 0
