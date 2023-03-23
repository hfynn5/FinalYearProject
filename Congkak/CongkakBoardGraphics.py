from graphics import *
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QPainter, QPen, QAction, QIcon, QPalette
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QPoint, Qt
from Congkak.Hand import Hand
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie, QRegion
from PyQt6.QtCore import Qt, QPoint
import sys


# TODO: Better Graphics
class BoardGraphic(QMainWindow):

    def __init__(self):
        super().__init__()

        self.active = True

        # set the title
        self.setWindowTitle("Congkak")

        # setting the geometry of window
        self.setGeometry(100, 100, 800, 600)
        self.setAutoFillBackground(True)

        self.house_a_points = []
        self.house_b_points = []
        self.storeroom_a_point = QPoint(0, 0)
        self.storeroom_b_point = QPoint(0, 0)

        self.house_a_text_labels = []
        self.house_b_text_labels = []
        self.storeroom_a_text_label = QLabel()
        self.storeroom_b_text_label = QLabel()
        self.player_a_hand_text_label = QLabel()
        self.player_b_hand_text_label = QLabel()

        self.house_a_buttons = []
        self.house_b_buttons = []

        self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
        self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)

        self.player_a_hand_point = QPoint(0, 0)
        self.player_b_hand_point = QPoint(0, 0)

        self.player_a_hand_img_label = QLabel()
        self.player_b_hand_img_label = QLabel()

        self.player_a_dropdown = QComboBox()
        self.player_b_dropdown = QComboBox()

        self.move_speed_slider = QSlider()
        self.play_button = QPushButton()

        self.new_game_button_action = QAction()
        self.save_game_button_action = QAction()
        self.load_game_button_action = QAction()

        self.acceptDrops()

        self.generate_points()

        self.create_hole_labels()
        self.create_inputs()
        self.create_menus()

        self.set_pictures()

        # label = QLabel(self)
        # label.resize(136, 267)
        # pixmap = QPixmap('Assets/Sprites/Hand_sprite.png')
        # label.move(QPoint(100, 120))
        # label.setPixmap(pixmap)

        # self.player_a_hand_img_label = QLabel(self)
        # self.player_a_hand_img_label.resize(136, 267)
        # pixmap = QPixmap('Assets/Sprites/Hand_sprite.png')
        # self.player_a_hand_img_label.move(QPoint(300, 200))
        # self.player_a_hand_img_label.setPixmap(pixmap)
        # self.player_b_hand_img_label.show()

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

    # what to do if close window
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.active = False
        a0.accept()

    # Generate points once for the circles
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

    # Draws all the circles and hands and shapes
    def paintEvent(self, QPaintEvent):

        storeroom_diameter = 45

        house_diameter = 25

        hand_diameter = 50

        painter = QPainter(self)
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setColor(QtGui.QColor('white'))
        painter.setPen(pen)

        # painter.fillRect(0, 0, 800, 600, QtGui.QBrush((QtGui.QColor(255, 255, 255, 255))))

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

        # # player hand a
        # pen.setColor(QtGui.QColor('blue'))
        # painter.setPen(pen)
        # painter.drawArc(round(self.player_a_hand_point.x()), round(self.player_a_hand_point.y()), hand_diameter,
        #                 hand_diameter, 0 * 16, 180 * 16)
        # # player hand b
        # pen.setColor(QtGui.QColor('red'))
        # painter.setPen(pen)
        # painter.drawArc(round(self.player_b_hand_point.x()), round(self.player_b_hand_point.y()), hand_diameter,
        #                 hand_diameter, 180 * 16, 180 * 16)

        painter.end()

    # updates the hand value label
    def update_hand_label(self):

        offset = QPoint(22, 5)

        self.player_a_hand_text_label.move(self.player_a_hand_point + offset)
        self.player_a_hand_text_label.setText(str(self.player_a_hand.counter_count))

        offset = QPoint(22, 15)

        self.player_b_hand_text_label.move(self.player_b_hand_point + offset)
        self.player_b_hand_text_label.setText(str(self.player_b_hand.counter_count))

    # update images
    def update_images(self):

        offset = QPoint(5, -10)

        print(self.player_a_hand_point + offset)

        self.player_a_hand_img_label.move(self.player_a_hand_point + offset)

        offset = QPoint(-5, 10)
        self.player_b_hand_img_label.move(self.player_b_hand_point + offset)

    # set pictures
    def set_pictures(self):

        pixmap = QPixmap('Congkak/Assets/Sprites/Hand_sprite.png')
        pixmap_b = pixmap.scaled(45, 89)
        pixmap_a = pixmap_b.transformed(QtGui.QTransform().rotate(180))

        self.player_a_hand_img_label = QLabel(self)
        self.player_a_hand_img_label.resize(45, 89)
        self.player_a_hand_img_label.setPixmap(pixmap_a)

        self.player_b_hand_img_label = QLabel(self)
        self.player_b_hand_img_label.resize(45, 89)
        self.player_b_hand_img_label.setPixmap(pixmap_b)

        self.update_images()

    # create the label for all the holes
    def create_hole_labels(self):

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

        self.player_a_hand_text_label = QLabel(self)

        self.player_b_hand_text_label = QLabel(self)

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
        self.player_a_dropdown.addItems(['Human', 'Random', 'Max', 'Minimax', 'MCTS'])

        self.player_b_dropdown = QComboBox(self)
        self.player_b_dropdown.move(650, 380)
        self.player_b_dropdown.addItems(['Human', 'Random', 'Max', 'Minimax', 'MCTS'])

        slider_label = QLabel(self)
        slider_label.move(360, 500)
        slider_label.setText("Moves Per Second")

        self.move_speed_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.move_speed_slider.setGeometry(200, 450, 400, 50)
        self.move_speed_slider.setMinimum(1)
        self.move_speed_slider.setMaximum(11)
        self.move_speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.move_speed_slider.setTickInterval(1)

        self.play_button = QPushButton(self)
        self.play_button.setGeometry(150,450,40,25)
        self.play_button.setText("Play")

    # creates the menus
    def create_menus(self):

        # save games?
        file_menu = self.menuBar().addMenu("File")

        self.new_game_button_action = QAction("New Game", self)
        self.new_game_button_action.setStatusTip("Create a new game from the start")
        file_menu.addAction(self.new_game_button_action)

        self.save_game_button_action = QAction("Save Game", self)
        self.save_game_button_action.setStatusTip("Save the game to a text file")
        file_menu.addAction(self.save_game_button_action)

        self.load_game_button_action = QAction("Load Game", self)
        self.load_game_button_action.setStatusTip("Load a game from a text file")
        file_menu.addAction(self.load_game_button_action)

        # edit games?
        edit_menu = self.menuBar().addMenu("Edit")

        submenu = edit_menu.addMenu("Edit Player")

        button_action = QAction("Player A", self)
        submenu.addAction(button_action)

        button_action = QAction("Player B", self)
        submenu.addAction(button_action)

        button_action = QAction("Edit Marble Count", self)
        edit_menu.addAction(button_action)

        button_action = QAction("Change Speed", self)
        edit_menu.addAction(button_action)

        train_menu = self.menuBar().addMenu("Training")

        # views
        view_menu = self.menuBar().addMenu("View")

        button_action = QAction("idk", self)
        view_menu.addAction(button_action)
        #
        game_menu = self.menuBar().addMenu("Game")

        button_action = QAction("Run Multiple Games...", self)
        game_menu.addAction(button_action)

        button_action = QAction("Run Round Robin Tournament...", self)
        game_menu.addAction(button_action)

        help_menu = self.menuBar().addMenu("Help")

        about_menu = self.menuBar().addMenu("About")

    def update_values(self, house_a_values, house_b_values,
                      storeroom_a_value, storeroom_b_value,
                      player_a_hand, player_b_hand):

        self.update_labels(house_a_values, house_b_values, storeroom_a_value, storeroom_b_value)

        self.player_a_hand = player_a_hand
        self.player_b_hand = player_b_hand

        self.update_hand_label()
        self.update_images()
        self.update()

    # updates the labels
    def update_labels(self, house_a_values, house_b_values,
                      storeroom_a_value, storeroom_b_value):

        for i, label in enumerate(self.house_a_text_labels):
            label.setText(str(house_a_values[i]))

        for i, label in enumerate(self.house_b_text_labels):
            label.setText(str(house_b_values[i]))

        self.storeroom_a_text_label.setText(str(storeroom_a_value))
        self.storeroom_b_text_label.setText(str(storeroom_b_value))

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
            y_coord = self.storeroom_a_point.y() - 80
        else:
            x_coord = -100
            y_coord = -100

        self.player_a_hand_point = QPoint(x_coord, y_coord)
        # self.player_a_hand_point.x = x_coord
        # self.player_a_hand_point.y = y_coord

        if 10 < player_b_hand.hole_pos < 18:
            x_coord = self.house_a_points[player_b_hand.hole_pos - 11].x() - round(hand_diameter / 2) - 1
            y_coord = self.house_a_points[player_b_hand.hole_pos - 11].y() + 10
        elif 20 < player_b_hand.hole_pos < 28:
            x_coord = self.house_b_points[player_b_hand.hole_pos - 21].x() - round(hand_diameter / 2) - 1
            y_coord = self.house_b_points[player_b_hand.hole_pos - 21].y() + 10
        elif player_b_hand.hole_pos == 18:
            x_coord = self.storeroom_b_point.x() - round(hand_diameter / 2) - 1
            y_coord = self.storeroom_b_point.y() + 40
        else:
            x_coord = -100
            y_coord = -100

        self.player_b_hand_point = QPoint(x_coord, y_coord)
        # self.player_b_hand_point.x = x_coord
        # self.player_b_hand_point.y = y_coord

    # end game prompt
    # TODO: add end game prompt
    def end_game_prompt(self):
        print("game ended.")
        pass

    # enable or disable the inputs
    def set_enable_inputs(self, enable):
        self.set_enable_player_inputs('a',enable)
        self.set_enable_player_inputs('b',enable)

    # enable or disable player inputs
    def set_enable_player_inputs(self, player, enable):
        if enable:
            enable_list = [1,2,3,4,5,6,7]
        else:
            enable_list = []
        self.set_enable_player_specific_inputs(player, enable_list)

    # enable or disable specific inputs of a player
    def set_enable_player_specific_inputs(self, player, enable_list):
        if player == 'a':
            for i, button in enumerate(self.house_a_buttons):
                if i+1 in enable_list:
                    button.setEnabled(True)
                    button.show()
                else:
                    button.setEnabled(False)
                    button.hide()

        elif player == 'b':
            for i, button in enumerate(self.house_b_buttons):
                if i+1 in enable_list:
                    button.setEnabled(True)
                    button.show()
                else:
                    button.setEnabled(False)
                    button.hide()

    # enable or disable play button
    def set_enable_play_button(self, enable):

        self.play_button.setEnabled(enable)

        if enable:
            self.play_button.show()
        else:
            self.play_button.hide()