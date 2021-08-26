from enum import Enum     # for enum34, or the stdlib version
class Piece(Enum):
    BLACK = 0
    RED = 1
    YELLOW = 2

# class Piece:
#     def __init__(self, color):
#         self.color = color
#
#     def get_color(self):
#         return self.color
#
#     def set_color(self, color):
#         self.color = color
