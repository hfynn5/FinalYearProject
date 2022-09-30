from graphics import *

class Board:

    # player A is top with storeroom on right.
    # player B is bottom with storeroom on left.
    storeroom_a = 0
    storeroom_b = 0

    # player A house 1 starts at right. For the sake of sanity, houses start at 1, not 0
    # player B house 1 starts at left.
    house_a = [0, 0, 0, 0, 0, 0, 0]
    house_b = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        self.win = GraphWin("Congkak", 800, 600)
