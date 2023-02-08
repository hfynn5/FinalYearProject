import sys

from Congkak.CongkakBoardGraphics import BoardGraphic
from Congkak.CongkakBoardModel import BoardModel, Hand
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap

class GameManager:

    def __init__(self):

        self.board_model = BoardModel()

        App = QApplication(sys.argv)
        self.board_graphic = BoardGraphic()

        self.update_board(board_graphic=self.board_graphic, board_model=self.board_model)

        sys.exit(App.exec())

    pass

    def update_board(self, board_graphic: BoardGraphic, board_model: BoardModel):

        board_graphic.update_values(house_a_values=board_model.house_a_values, house_b_values=board_model.house_b_values,
                                             storeroom_a_value=board_model.storeroom_a_value,
                                             storeroom_b_value=board_model.storeroom_b_value)

        # def update_board(self):
        #     self.board_graphic.update_values(house_a_values=self.house_a_values, house_b_values=self.house_b_values,
        #                                      storeroom_a_value=self.storeroom_a_value,
        #                                      storeroom_b_value=self.storeroom_b_value)

