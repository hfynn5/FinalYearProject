from PyQt6.QtGui import QPixmap, QPainter, QPen, QAction, QIcon, QPalette
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QPoint, Qt
from Congkak.Hand import Hand
from Congkak.DialogueBoxes.MultiGameDialogBox import MultiGameDialogBox
from Congkak.DialogueBoxes.TournamentDialogBox import TournamentDialogBox
from Congkak.DialogueBoxes.GameEndDialogBox import GameEndDialogBox
from Congkak.DialogueBoxes.MultiGameEndDialogBox import MultiGameEndDialogBox
from Congkak.DialogueBoxes.TournamentEndDialogBox import TournamentEndDialogBox
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie, QRegion
from PyQt6.QtCore import Qt, QPoint
import sys


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

        self.board_img_label = QLabel(self)
        self.player_a_hand_img_label = QLabel(self)
        self.player_b_hand_img_label = QLabel(self)

        self.house_a_text_labels = []
        self.house_b_text_labels = []
        self.storeroom_a_text_label = QLabel(self)
        self.storeroom_b_text_label = QLabel(self)
        self.player_a_hand_text_label = QLabel(self)
        self.player_a_hand_text_label.setStyleSheet("font: bold 15px")
        self.player_b_hand_text_label = QLabel(self)
        self.player_b_hand_text_label.setStyleSheet("font: bold 15px")

        self.house_a_buttons = []
        self.house_b_buttons = []

        self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
        self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)

        self.player_a_hand_point = QPoint(0, 0)
        self.player_b_hand_point = QPoint(0, 0)

        self.player_a_dropdown = QComboBox()
        self.player_b_dropdown = QComboBox()

        self.move_speed_slider = QSlider()
        self.play_button = QPushButton()

        self.new_game_menu_button_action = QAction()
        self.save_game_menu_button_action = QAction()
        self.load_game_menu_button_action = QAction()

        self.run_multiple_games_menu_button_action = QAction()
        self.run_tournament_menu_button_action = QAction()

        self.game_end_dialog_box = GameEndDialogBox()

        self.multiple_games_dialog_box = MultiGameDialogBox()
        self.multi_game_end_dialog_box = MultiGameEndDialogBox()

        self.tournament_dialog_box = TournamentDialogBox()
        self.tournament_end_dialog_box = TournamentEndDialogBox()

        self.acceptDrops()

        self.generate_points()

        self.create_hole_labels()
        self.create_inputs()
        self.create_menus()

        self.set_pictures()

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

    # updates the hand value label
    def update_hand_label(self):

        offset = QPoint(20, -30)

        self.player_a_hand_text_label.move(self.player_a_hand_point + offset)
        self.player_a_hand_text_label.setText(str(self.player_a_hand.counter_count))

        offset = QPoint(20, 50)

        self.player_b_hand_text_label.move(self.player_b_hand_point + offset)
        self.player_b_hand_text_label.setText(str(self.player_b_hand.counter_count))

    # update images
    def update_images(self):

        offset = QPoint(5, -50)
        self.player_a_hand_img_label.move(self.player_a_hand_point + offset)

        offset = QPoint(0, 15)
        self.player_b_hand_img_label.move(self.player_b_hand_point + offset)

    # set pictures
    def set_pictures(self):

        pixmap = QPixmap('Congkak/Assets/Sprites/Hand_sprite.png')
        pixmap_b = pixmap.scaled(45, 89)
        pixmap_a = pixmap_b.transformed(QtGui.QTransform().rotate(180))

        # self.player_a_hand_img_label = QLabel(self)
        self.player_a_hand_img_label.resize(45, 89)
        self.player_a_hand_img_label.setPixmap(pixmap_a)

        # self.player_b_hand_img_label = QLabel(self)
        self.player_b_hand_img_label.resize(45, 89)
        self.player_b_hand_img_label.setPixmap(pixmap_b)

        pixmap = QPixmap('Congkak/Assets/Sprites/Congkak_Board_1.png')
        pixmap = pixmap.scaledToWidth(732)
        self.board_img_label.resize(800, 300)
        self.board_img_label.setPixmap(pixmap)
        self.board_img_label.move(QPoint(29, 103))

        self.update_images()

    # create the label for all the holes
    def create_hole_labels(self):

        offset = QPoint(-4, -15)

        # creating text label for all the holes.
        for pos in self.house_a_points:
            label = QLabel(self)
            label.setStyleSheet("color: #FFEB22; font: bold 15px")
            label.move(pos + offset)
            label.setText("7")
            self.house_a_text_labels.append(label)

        for pos in self.house_b_points:
            label = QLabel(self)
            label.setStyleSheet("color: #FFEB22; font: bold 15px")
            label.move(pos + offset)
            label.setText("7")
            self.house_b_text_labels.append(label)

        # self.storeroom_a_text_label = QLabel(self)
        self.storeroom_a_text_label.move(self.storeroom_a_point + offset)
        self.storeroom_a_text_label.setStyleSheet("color: #FFEB22; font: bold 15px")
        self.storeroom_a_text_label.setText("0")

        # self.storeroom_b_text_label = QLabel(self)
        self.storeroom_b_text_label.move(self.storeroom_b_point + offset)
        self.storeroom_b_text_label.setStyleSheet("color: #FFEB22; font: bold 15px")
        self.storeroom_b_text_label.setText("0")
        #
        # self.player_a_hand_text_label = QLabel(self)
        #
        # self.player_b_hand_text_label = QLabel(self)

    # creates the UI.
    def create_inputs(self):

        offset = QPoint(-22, -55)

        for pos in self.house_a_points:
            button = QPushButton(self)
            button.resize(40, 25)
            button.move(pos + offset)
            button.setText("Pick")
            self.house_a_buttons.append(button)

        offset = QPoint(-22, 31)

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

        # Game Menu
        game_menu = self.menuBar().addMenu("Game")

        self.run_multiple_games_menu_button_action = QAction("Run Multiple Games...", self)
        self.run_multiple_games_menu_button_action.setStatusTip("Run Multiple Games")
        self.run_multiple_games_menu_button_action.triggered.connect(self.multiple_games_dialog_box.exec)
        game_menu.addAction(self.run_multiple_games_menu_button_action)

        self.run_tournament_menu_button_action = QAction("Run Round Robin Tournament...", self)
        self.run_tournament_menu_button_action.setStatusTip("Run Round Robin Tournament")
        self.run_tournament_menu_button_action.triggered.connect(self.tournament_dialog_box.exec)
        game_menu.addAction(self.run_tournament_menu_button_action)

        help_menu = self.menuBar().addMenu("Help")

        about_menu = self.menuBar().addMenu("About")

    def update_values(self, house_a_values, house_b_values,
                      storeroom_a_value, storeroom_b_value,
                      player_a_hand, player_b_hand):

        self.update_hand_positions()

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
            if not 10 < player_a_hand.hole_pos < 18:
                print("the weirdest fucking anomaly")
            y_coord = round(self.house_a_points[player_a_hand.hole_pos - 11].y() - hand_diameter - 10)
        elif 20 < player_a_hand.hole_pos < 28:
            x_coord = round(self.house_b_points[player_a_hand.hole_pos - 21].x() - round(hand_diameter / 2) - 1)
            y_coord = round(self.house_b_points[player_a_hand.hole_pos - 21].y() - hand_diameter - 10)
        elif player_a_hand.hole_pos == 10:
            x_coord = self.storeroom_a_point.x() - round(hand_diameter / 2) - 1
            y_coord = self.storeroom_a_point.y() - 80
        else:
            x_coord = -100
            y_coord = -100

        self.player_a_hand_point = QPoint(x_coord, y_coord)

        if 10 < player_b_hand.hole_pos < 18:
            x_coord = self.house_a_points[player_b_hand.hole_pos - 11].x() - round(hand_diameter / 2) - 1
            y_coord = self.house_a_points[player_b_hand.hole_pos - 11].y() + 10
        elif 20 < player_b_hand.hole_pos < 28:
            x_coord = self.house_b_points[player_b_hand.hole_pos - 21].x() - round(hand_diameter / 2) - 1
            y_coord = self.house_b_points[player_b_hand.hole_pos - 21].y() + 10
        elif player_b_hand.hole_pos == 20:
            x_coord = self.storeroom_b_point.x() - round(hand_diameter / 2) - 1
            y_coord = self.storeroom_b_point.y() + 40
        else:
            x_coord = -100
            y_coord = -100

        self.player_b_hand_point = QPoint(x_coord, y_coord)

    # prompts end game
    def end_game_prompt(self, winner, player_a_score, player_b_score):
        self.game_end_dialog_box.winner_label.setText(str(winner))
        self.game_end_dialog_box.player_a_score_label.setText(str(player_a_score))
        self.game_end_dialog_box.player_b_score_label.setText(str(player_b_score))
        self.game_end_dialog_box.exec()
        pass

    def multi_end_game_prompt(self, score_list):

        player_a_wins = score_list.count(1)
        player_b_wins = score_list.count(-1)
        draws = score_list.count(0)
        games_played = len(score_list)

        self.multi_game_end_dialog_box.no_games_played_label.setText(str(games_played))
        self.multi_game_end_dialog_box.player_a_score_label.setText(str(player_a_wins))
        self.multi_game_end_dialog_box.player_b_score_label.setText(str(player_b_wins))
        self.multi_game_end_dialog_box.draws_label.setText(str(draws))

        self.multi_game_end_dialog_box.game_score_list_label.setText(str(score_list))

        self.multi_game_end_dialog_box.exec()

    def tournament_end_prompt(self, participants, no_of_games, results):

        self.tournament_end_dialog_box.create_table(participants, results)

        self.tournament_end_dialog_box.exec()

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