from graphics import *
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QPoint
import sys


class BoardGraphic(QWidget):
    def __init__(self):
        super().__init__()

        self.house_a_positions = []
        self.house_b_positions = []
        self.storeroom_a_position = Point(0, 0)
        self.storeroom_b_position = Point(0, 0)

        self.house_a_text_labels = []
        self.house_b_text_labels = []
        self.storeroom_a_text_label = QLabel()
        self.storeroom_b_text_label = QLabel()

        self.house_a_buttons = []
        self.house_b_buttons = []

        self.display_must_update = True

        self.acceptDrops()
        # set the title
        self.setWindowTitle("Congkak")

        # setting the geometry of window
        self.setGeometry(100, 100, 800, 600)

        self.generate_points()

        self.create_hole_text()
        self.create_buttons()



        #
        # label = QLabel(self)
        # label.move(30, 200)
        # label.setText("tefdsfgsf edfshbsgshrgyhgd")

        # show all the widgets
        self.show()

    def generate_points(self):

        storeroom_b_x_pos = 100
        storeroom_y_pos = 250

        house_a_y_pos = 200
        house_b_y_pos = 300

        storeroom_house_offset = 90
        house_x_pos_init = storeroom_b_x_pos + storeroom_house_offset
        house_x_pos_offset = 70

        # storeroom B
        self.storeroom_b_position = QPoint(storeroom_b_x_pos, storeroom_y_pos)

        # house a
        house_x_pos = house_x_pos_init
        for x in range(7):
            self.house_a_positions.append(QPoint(house_x_pos, house_a_y_pos))
            house_x_pos += house_x_pos_offset
        house_x_pos -= house_x_pos_offset
        self.house_a_positions.reverse()

        # storeroom A
        storeroom_a_x_pos = house_x_pos + storeroom_house_offset
        self.storeroom_a_position = QPoint(storeroom_a_x_pos, storeroom_y_pos)

        # house b
        for x in range(7):
            self.house_b_positions.append(QPoint(house_x_pos, house_b_y_pos))
            house_x_pos -= house_x_pos_offset

    def paintEvent(self, QPaintEvent):

        storeroom_diameter = 45

        house_diameter = 25

        painter = QPainter(self)
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setColor(QtGui.QColor('brown'))
        painter.setPen(pen)

        # storeroom B
        painter.drawEllipse(self.storeroom_a_position, storeroom_diameter, storeroom_diameter)

        # house a
        for pos in self.house_a_positions:
            painter.drawEllipse(pos, house_diameter, house_diameter)

        # storeroom A
        painter.drawEllipse(self.storeroom_b_position, storeroom_diameter, storeroom_diameter)

        # house b
        for pos in self.house_b_positions:
            painter.drawEllipse(pos, house_diameter, house_diameter)

        painter.end()

        #self.create_UI()

    def create_hole_text(self):

        offset = QPoint(-4, -7)

        # creating text label for all the holes.
        for pos in self.house_a_positions:
            label = QLabel(self)
            label.move(pos + offset)
            label.setText("7")
            self.house_a_text_labels.append(label)

        for pos in self.house_b_positions:
            label = QLabel(self)
            label.move(pos + offset)
            label.setText("7")
            self.house_b_text_labels.append(label)

        self.storeroom_a_text_label = QLabel(self)
        self.storeroom_a_text_label.move(self.storeroom_a_position + offset)
        self.storeroom_a_text_label.setText("0")

        self.storeroom_b_text_label = QLabel(self)
        self.storeroom_b_text_label.move(self.storeroom_b_position + offset)
        self.storeroom_b_text_label.setText("0")

    def create_buttons(self):

        offset = QPoint(-22, -60)

        count = 7

        for pos in self.house_a_positions:
            button = QPushButton(self)
            button.resize(40, 25)
            button.move(pos + offset)
            button.setText("Pick")
            self.house_a_buttons.append(button)

            count -= 1

        count = 7

        offset = QPoint(-22, 40)

        for pos in self.house_b_positions:
            button = QPushButton(self)
            button.resize(40, 25)
            button.move(pos + offset)
            button.setText("Pick")
            self.house_b_buttons.append(button)

            count -= 1


    def update_values(self, house_a_values, house_b_values, storeroom_a_value, storeroom_b_value):

        for x in range(len(self.house_a_positions)):
            label = Text(self.house_a_positions[x], house_a_values[x])
            label.draw(self.win)

        for x in range(len(self.house_b_positions)):
            label = Text(self.house_b_positions[x], house_b_values[x])
            label.draw(self.win)

        label = Text(self.storeroom_a_position, storeroom_a_value)
        label.draw(self.win)

        label = Text(self.storeroom_b_position, storeroom_b_value)
        label.draw(self.win)


