from graphics import *
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QPainter, QPen, QAction, QIcon
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QPoint, Qt
from Congkak.Hand import Hand
import sys


class BoardGraphic(QMainWindow):
    def __init__(self):
        super().__init__()

        self.active = True

        self.house_a_points = []
        self.house_b_points = []
        self.storeroom_a_point = Point(0, 0)
        self.storeroom_b_point = Point(0, 0)

        self.house_a_text_labels = []
        self.house_b_text_labels = []
        self.storeroom_a_text_label = QLabel()
        self.storeroom_b_text_label = QLabel()

        self.house_a_buttons = []
        self.house_b_buttons = []

        self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
        self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)

        self.player_a_hand_point = Point(0, 0)
        self.player_b_hand_point = Point(0, 0)

        # self.player_b_hand_point.x()

        self.player_a_dropdown = QComboBox()
        self.player_b_dropdown = QComboBox()

        self.move_speed_slider = QSlider()
        self.play_button = QPushButton()

        self.acceptDrops()
        # set the title
        self.setWindowTitle("Congkak")

        # setting the geometry of window
        self.setGeometry(100, 100, 800, 600)

        self.generate_points()

        self.create_hole_text()
        self.create_inputs()
        self.create_menus

        # show all the widgets
        self.show()

        # comment out afterwards

        # msg = QMessageBox()
        # msg.setWindowTitle("Round Robin Result")
        # msg.setText("Results\n\n"
        #             "Rounds: 100\n"
        #             "Random: 2 wins"
        #             "Minimax: 60 wins\n"
        #             "MCTS: 40 wins\n"
        #             "Q-Learning: 40 wins"
        #             )
        #
        # x = msg.exec()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.active = False
        a0.accept()

    # Generate points for the circles
    def generate_points(self):

        storeroom_b_x_pos = 100
        storeroom_y_pos = 250

        house_a_y_pos = 200
        house_b_y_pos = 300

        storeroom_house_offset = 90
        house_x_pos_init = storeroom_b_x_pos + storeroom_house_offset
        house_x_pos_offset = 70

        # storeroom B
        self.storeroom_b_point = QPoint(storeroom_b_x_pos, storeroom_y_pos)

        # house a
        house_x_pos = house_x_pos_init
        for x in range(7):
            self.house_a_points.append(QPoint(house_x_pos, house_a_y_pos))
            house_x_pos += house_x_pos_offset
        house_x_pos -= house_x_pos_offset
        self.house_a_points.reverse()

        # storeroom A
        storeroom_a_x_pos = house_x_pos + storeroom_house_offset
        self.storeroom_a_point = QPoint(storeroom_a_x_pos, storeroom_y_pos)

        # house b
        for x in range(7):
            self.house_b_points.append(QPoint(house_x_pos, house_b_y_pos))
            house_x_pos -= house_x_pos_offset
        self.house_b_points.reverse()

    # Draws all the circles
    def paintEvent(self, QPaintEvent):

        storeroom_diameter = 45

        house_diameter = 25

        hand_diameter = 50

        painter = QPainter(self)
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setColor(QtGui.QColor('brown'))
        painter.setPen(pen)

        # storeroom A
        painter.drawEllipse(self.storeroom_a_point, storeroom_diameter, storeroom_diameter)

        # house A
        for i, pos in enumerate(self.house_a_points):
            painter.drawEllipse(pos, house_diameter, house_diameter)

        # storeroom B
        painter.drawEllipse(self.storeroom_b_point, storeroom_diameter, storeroom_diameter)

        # house B
        for i, pos in enumerate(self.house_b_points):
            painter.drawEllipse(pos, house_diameter, house_diameter)

        self.update_hand_positions()

        pen.setColor(QtGui.QColor('blue'))
        painter.setPen(pen)
        painter.drawArc(round(self.player_a_hand_point.x), round(self.player_a_hand_point.y), hand_diameter,
                        hand_diameter, 0 * 16, 180 * 16)

        pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen)
        painter.drawArc(round(self.player_b_hand_point.x), round(self.player_b_hand_point.y), hand_diameter,
                        hand_diameter, 180 * 16, 180 * 16)

        painter.end()

    # def paint

    # create the label for all the holes
    def create_hole_text(self):

        offset = QPoint(-4, -15)

        # creating text label for all the holes.
        for pos in self.house_a_points:
            label = QLabel(self)
            label.move(pos + offset)
            label.setText("7")
            self.house_a_text_labels.append(label)

        for pos in self.house_b_points:
            label = QLabel(self)
            label.move(pos + offset)
            label.setText("7")
            self.house_b_text_labels.append(label)

        self.storeroom_a_text_label = QLabel(self)
        self.storeroom_a_text_label.move(self.storeroom_a_point + offset)
        self.storeroom_a_text_label.setText("0")

        self.storeroom_b_text_label = QLabel(self)
        self.storeroom_b_text_label.move(self.storeroom_b_point + offset)
        self.storeroom_b_text_label.setText("0")

    # TODO: create labels for hand
    def create_hand_text(self):
        pass

    # creates the UI.
    def create_inputs(self):

        offset = QPoint(-22, -60)

        for pos in self.house_a_points:
            button = QPushButton(self)
            button.resize(40, 25)
            button.move(pos + offset)
            button.setText("Pick")
            self.house_a_buttons.append(button)

        offset = QPoint(-22, 40)

        for pos in self.house_b_points:
            button = QPushButton(self)
            button.resize(40, 25)
            button.move(pos + offset)
            button.setText("Pick")
            self.house_b_buttons.append(button)

        self.player_a_dropdown = QComboBox(self)
        self.player_a_dropdown.move(650, 100)
        self.player_a_dropdown.addItems(['Random', 'Minimax', 'MCTS', 'Human'])

        self.player_b_dropdown = QComboBox(self)
        self.player_b_dropdown.move(650, 380)
        self.player_b_dropdown.addItems(['Random', 'Minimax', 'MCTS', 'Human'])

        slider_label = QLabel(self)
        slider_label.move(360, 500)
        slider_label.setText("Moves Per Second")

        self.move_speed_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.move_speed_slider.setGeometry(200, 450, 400, 50)
        self.move_speed_slider.setMinimum(1)
        self.move_speed_slider.setMaximum(10)
        self.move_speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.move_speed_slider.setTickInterval(1)

        self.play_button = QPushButton(self)
        self.play_button.setGeometry(150,450,40,25)
        self.play_button.setText("Play")

    # creates the menus
    def create_menus(self):

        menu_bar = self.menuBar()

        # save games?
        file_menu = menu_bar.addMenu("File")

        button_action = QAction("New Game", self)
        # button_action.setStatusTip("This is your button")
        # button_action.triggered.connect(self.onMyToolBarButtonClick)
        # button_action.setCheckable(True)
        file_menu.addAction(button_action)

        button_action = QAction("", self)
        file_menu.addAction(button_action)

        button_action = QAction("Save Game", self)
        file_menu.addAction(button_action)

        button_action = QAction("Load Game", self)
        file_menu.addAction(button_action)

        # edit games?
        edit_menu = menu_bar.addMenu("Edit")

        submenu = edit_menu.addMenu("Edit Player")

        button_action = QAction("Player A", self)
        submenu.addAction(button_action)

        button_action = QAction("Player B", self)
        submenu.addAction(button_action)

        button_action = QAction("Edit Marble Count", self)
        edit_menu.addAction(button_action)

        button_action = QAction("Change Speed", self)
        edit_menu.addAction(button_action)

        train_menu = menu_bar.addMenu("Training")

        # views
        view_menu = menu_bar.addMenu("View")

        button_action = QAction("idk", self)
        view_menu.addAction(button_action)
        #
        game_menu = menu_bar.addMenu("Game")

        button_action = QAction("Run Multiple Games...", self)
        game_menu.addAction(button_action)

        button_action = QAction("Run Round Robin Tournament...", self)
        game_menu.addAction(button_action)

        help_menu = menu_bar.addMenu("Help")

        about_menu = menu_bar.addMenu("About")

    # updates the labels
    def update_values(self, house_a_values, house_b_values,
                      storeroom_a_value, storeroom_b_value,
                      player_a_hand, player_b_hand):

        for i, label in enumerate(self.house_a_text_labels):
            label.setText(str(house_a_values[i]))

        for i, label in enumerate(self.house_b_text_labels):
            label.setText(str(house_b_values[i]))

        self.storeroom_a_text_label.setText(str(storeroom_a_value))
        self.storeroom_b_text_label.setText(str(storeroom_b_value))

        self.player_a_hand = player_a_hand
        self.player_b_hand = player_b_hand

        self.update()

    # update the hand positions
    def update_hand_positions(self):
        hand_diameter = 50

        player_a_hand = self.player_a_hand
        player_b_hand = self.player_b_hand

        if 10 < player_a_hand.hole_pos < 18:
            x_coord = round(self.house_a_points[player_a_hand.hole_pos - 11].x() - round(hand_diameter / 2) - 1)
            y_coord = round(self.house_a_points[player_a_hand.hole_pos - 11].y() - hand_diameter - 10)
        elif 20 < player_a_hand.hole_pos < 28:
            x_coord = round(self.house_b_points[player_a_hand.hole_pos - 21].x() - round(hand_diameter / 2) - 1)
            y_coord = round(self.house_b_points[player_a_hand.hole_pos - 21].y() - hand_diameter - 10)
        elif player_a_hand.hole_pos == 28:
            x_coord = self.storeroom_a_point.x() - round(hand_diameter / 2) - 1
            y_coord = self.storeroom_a_point.y() - 70
        else:
            x_coord = -100
            y_coord = -100

        self.player_a_hand_point = Point(x_coord, y_coord)

        if 10 < player_b_hand.hole_pos < 18:
            x_coord = self.house_a_points[player_b_hand.hole_pos - 11].x() - round(hand_diameter / 2) - 1
            y_coord = self.house_a_points[player_b_hand.hole_pos - 11].y() + 10
        elif 20 < player_b_hand.hole_pos < 28:
            x_coord = self.house_b_points[player_b_hand.hole_pos - 21].x() - round(hand_diameter / 2) - 1
            y_coord = self.house_b_points[player_b_hand.hole_pos - 21].y() + 10
        elif player_b_hand.hole_pos == 18:
            x_coord = self.storeroom_b_point.x() - round(hand_diameter / 2) - 1
            y_coord = self.storeroom_b_point.y() + 30
        else:
            x_coord = -100
            y_coord = -100

        self.player_b_hand_point = Point(x_coord, y_coord)

    # enable or disable the inputs
    def set_enable_inputs(self, enable):
        for button in self.house_a_buttons:
            button.setEnabled(enable)
            if enable:
                button.show()
            else:
                button.hide()
        for button in self.house_b_buttons:
            button.setEnabled(enable)
            if enable:
                button.show()
            else:
                button.hide()