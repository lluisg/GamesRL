class Piece:
    def __init__(self, value = 0):
        self.value = value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def value_decrease(self):
        self.value -= 1

    def value_remove(self):
        self.value = 0
