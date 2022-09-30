from graphics import *
from Congkak.CongkakBoardGraphics import BoardGraphic

class BoardModel:

    # player A is top with storeroom on right.
    # player B is bottom with storeroom on left.
    storeroom_a_value = 0
    storeroom_b_value = 0

    # player A house 1 starts at right. For the sake of sanity, houses start at 1, not 0
    # player B house 1 starts at left.
    house_a_values = [0, 0, 0, 0, 0, 0, 0]
    house_b_values = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        #self.win = GraphWin("Congkak", 800, 600)

        self.board_graphic = BoardGraphic()

        self.house_a_values = [7, 6, 5, 4, 3, 2, 1]
        self.house_b_values = [1, 2, 3, 4, 5, 6, 7]

        self.storeroom_a_value = 12
        self.storeroom_b_value = 17

        while True:

            self.board_graphic.update_values(self.house_a_values, self.house_b_values, self.storeroom_a_value, self.storeroom_b_value)

            click_point = self.board_graphic.win.getMouse()

            if click_point is None:
                print('none')

        self.board_graphic.win.close()
