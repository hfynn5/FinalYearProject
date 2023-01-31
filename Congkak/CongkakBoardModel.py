from graphics import *
from Congkak.CongkakBoardGraphics import BoardGraphic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap

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

        App = QApplication(sys.argv)
        self.board_graphic = BoardGraphic()

        self.house_a_values = [7, 7, 7, 7, 7, 7, 7]
        self.house_b_values = [7, 7, 7, 7, 7, 7, 7]

        self.storeroom_a_value = 0
        self.storeroom_b_value = 0

        self.update_board()

        # time.sleep(1)

        self.iterate_sowing(player='a', hole=1)

        self.update_board()


        sys.exit(App.exec())

    def iterate_sowing(self, player, hole):

        CONTINUE_SOWING = 1
        STOP_SOWING = 2
        PROMPT_SOWING = 3

        status = CONTINUE_SOWING

        while status == CONTINUE_SOWING:

            new_hand_pos = self.sow_once(player = player, hole = hole)

            if new_hand_pos == 28 or new_hand_pos == 18:
                new_hand_pos -= 1

            if (new_hand_pos < 20 and self.house_a_values[new_hand_pos-11] == 1) or (new_hand_pos > 20 and self.house_b_values[new_hand_pos - 21] == 1):
                status = STOP_SOWING
                print("sowing stopped")
            elif new_hand_pos == 17 or new_hand_pos == 27:
                status = PROMPT_SOWING
                print("user needs to input hole")
            else:
                status = CONTINUE_SOWING
                hole = new_hand_pos % 10
                print("continuing starting with: " + str(hole))





    def sow_once(self, player, hole):

        hand_value = 0
        hand_pos = hole

        if player == 'a':

            hand_pos = 10 + hole

            hand_value = self.house_a_values[hole-1]
            self.house_a_values[hole-1] = 0

        elif player == 'b':

            hand_pos = 20 + hole

            hand_value = self.house_b_values[hole-1]
            self.house_b_values[hole-1] = 0

        while hand_value > 0:

            # time.sleep(1)
            self.update_board()

            hand_pos -= 1

            if hand_pos == 10:
                if player == 'a':
                    self.storeroom_a_value += 1
                    hand_value -= 1
                hand_pos = 28
            elif hand_pos == 20:
                if player == 'b':
                    self.storeroom_b_value += 1
                    hand_value -= 1
                hand_pos = 18
            elif hand_pos < 20:
                self.house_a_values[hand_pos-11] += 1
                hand_value -= 1
            elif hand_pos > 20:
                self.house_b_values[hand_pos-21] += 1
                hand_value -= 1

        return hand_pos

    def update_board(self):
        self.board_graphic.update_values(house_a_values=self.house_a_values, house_b_values=self.house_b_values,
                                         storeroom_a_value=self.storeroom_a_value,
                                         storeroom_b_value=self.storeroom_b_value)




