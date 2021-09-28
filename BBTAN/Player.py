class Player:
    def __init__(self):
        pass

    def play_turn(self):
        angle = None

        while angle not in [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165]:
            print "Input an angle multiple of 15 between 15 and 165"
            # angle = int(input())
            angle = 15
            print angle

