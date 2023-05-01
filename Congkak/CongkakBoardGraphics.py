from PyQt6.QtGui import QPixmap, QPainter, QPen, QAction, QIcon, QPalette
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QPoint, Qt
from Congkak.Hand import Hand
from Congkak.DialogueBoxes.CounterEditDialogBox import CounterEditDialogBox
from Congkak.DialogueBoxes.MultiGameDialogBox import MultiGameDialogBox
from Congkak.DialogueBoxes.TournamentDialogBox import TournamentDialogBox
from Congkak.DialogueBoxes.GameEndDialogBox import GameEndDialogBox
from Congkak.DialogueBoxes.MultiGameEndDialogBox import MultiGameEndDialogBox
from Congkak.DialogueBoxes.TournamentEndDialogBox import TournamentEndDialogBox
from Congkak.DialogueBoxes.EvalFuncTrainingDialogBox import EvalFuncTrainingDialogBox
from Congkak.DialogueBoxes.EvalFuncTrainingEndDialogBox import EvalFuncTrainingEndDialogBox
from Congkak.DialogueBoxes.UpdateWeightsDialogBox import UpdateWeightsDialogBox
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QMessageBox, QFrame
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie, QRegion
from PyQt6.QtCore import Qt, QPoint
import sys

#
# class VLine(QFrame):
#     # a simple VLine, like the one you get from designer
#     def __init__(self):
#         super(VLine, self).__init__()
#         self.setFrameShape(self.VLine|self.Sunken)


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

        self.player_a_agent_dropdown = QComboBox()
        self.player_b_agent_dropdown = QComboBox()
        self.player_a_simul_agent_dropdown = QComboBox()
        self.player_b_simul_agent_dropdown = QComboBox()

        self.move_speed_slider = QSlider()
        self.play_button = QPushButton()

        self.new_game_menu_button_action = QAction()
        self.save_game_menu_button_action = QAction()
        self.load_game_menu_button_action = QAction()

        self.counter_edit_dialog_box = CounterEditDialogBox()

        self.update_graphics_menu_toggle_action = QAction()

        self.train_state_agent_menu_toggle_action = QAction()
        self.run_eval_func_training_menu_button_action = QAction()

        self.run_multiple_games_menu_button_action = QAction()
        self.run_tournament_menu_button_action = QAction()

        self.game_end_dialog_box = GameEndDialogBox()

        self.update_weights_dialog_box = UpdateWeightsDialogBox()

        self.show_rl_state_button_action = QAction()
        self.show_q_state_button_action = QAction()

        self.eval_func_training_dialog_box = EvalFuncTrainingDialogBox()
        self.eval_func_training_end_dialog_box = EvalFuncTrainingEndDialogBox()

        self.run_bfpm_menu_button_action = QAction()

        self.multiple_games_dialog_box = MultiGameDialogBox()
        self.multi_game_end_dialog_box = MultiGameEndDialogBox()

        self.tournament_dialog_box = TournamentDialogBox()
        self.tournament_end_dialog_box = TournamentEndDialogBox()

        self.message_box = QMessageBox()
        self.message_box.setStyleSheet("QLabel{min-width: 1000px;}")

        self.acceptDrops()

        self.generate_points()

        self.create_hole_labels()
        self.create_inputs()
        self.create_menus()

        self.set_pictures()

        self.status_current_status_label = QLabel("Status: ")
        self.status_mode_label = QLabel("Mode: ")
        self.status_games_left_label = QLabel("Games left: ")
        self.status_random_label = QLabel("")

        self.statusBar().reformat()
        self.statusBar().setStyleSheet('border: 0; background-color: #FFF8DC;')
        self.statusBar().setStyleSheet("QStatusBar::item {border: none;}")

        self.statusBar().addPermanentWidget(self.status_current_status_label)
        # self.statusBar().addPermanentWidget(VLine())
        self.statusBar().addPermanentWidget(self.status_mode_label)
        # self.statusBar().addPermanentWidget(VLine())
        self.statusBar().addPermanentWidget(self.status_games_left_label)
        # self.statusBar().addPermanentWidget(VLine())
        self.statusBar().addPermanentWidget(self.status_random_label)
        # self.statusBar().addPermanentWidget(VLine())




        # show all the widgets
        self.show()

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

        label_a = QLabel(self)
        label_a.move(650, 70)
        label_a.setText("Player A agent")

        self.player_a_agent_dropdown = QComboBox(self)
        self.player_a_agent_dropdown.move(650, 100)
        self.player_a_agent_dropdown.addItems(['Human', 'Random', 'Max', 'Minimax'])

        label_a = QLabel(self)
        label_a.move(650, 410)
        label_a.setText("Player B agent")

        self.player_b_agent_dropdown = QComboBox(self)
        self.player_b_agent_dropdown.move(650, 380)
        self.player_b_agent_dropdown.addItems(['Human', 'Random', 'Max', 'Minimax'])

        label_a = QLabel(self)
        label_a.move(500, 70)
        label_a.setText("Player A simul agent")

        self.player_a_simul_agent_dropdown = QComboBox(self)
        self.player_a_simul_agent_dropdown.move(500, 100)
        self.player_a_simul_agent_dropdown.addItems(['Human', 'Random', 'R Learning', 'Q Learning', 'Preset'])

        label_a = QLabel(self)
        label_a.move(500, 410)
        label_a.setText("Player B simul agent")

        self.player_b_simul_agent_dropdown = QComboBox(self)
        self.player_b_simul_agent_dropdown.move(500, 380)
        self.player_b_simul_agent_dropdown.addItems(['Human', 'Random', 'R Learning', 'Q Learning', 'Preset'])

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

        # File Menu
        file_menu = self.menuBar().addMenu("File")

        self.new_game_menu_button_action = QAction("New Game", self)
        self.new_game_menu_button_action.setStatusTip("Create a new game from the start")
        file_menu.addAction(self.new_game_menu_button_action)

        self.save_game_menu_button_action = QAction("Save Game", self)
        self.save_game_menu_button_action.setStatusTip("Save the game to a text file")
        file_menu.addAction(self.save_game_menu_button_action)

        self.load_game_menu_button_action = QAction("Load Game", self)
        self.load_game_menu_button_action.setStatusTip("Load a game from a text file")
        file_menu.addAction(self.load_game_menu_button_action)

        # Edit Menu
        edit_menu = self.menuBar().addMenu("Edit")

        # submenu = edit_menu.addMenu("Edit Player")
        #
        # button_action = QAction("Player A", self)
        # submenu.addAction(button_action)
        #
        # button_action = QAction("Player B", self)
        # submenu.addAction(button_action)

        button_action = QAction("Edit Marble Count", self)
        button_action.triggered.connect(self.counter_edit_dialog_box.exec)
        edit_menu.addAction(button_action)

        # button_action = QAction("Change Speed", self)
        # edit_menu.addAction(button_action)

        # Training Menu
        train_menu = self.menuBar().addMenu("Training")

        self.train_state_agent_menu_toggle_action = QAction("Train State Agents", self)
        self.train_state_agent_menu_toggle_action.setCheckable(True)
        self.train_state_agent_menu_toggle_action.setChecked(False)
        train_menu.addAction(self.train_state_agent_menu_toggle_action)

        train_menu.addSeparator()

        self.show_rl_state_button_action = QAction("Show all RL states", self)
        train_menu.addAction(self.show_rl_state_button_action)

        self.show_q_state_button_action = QAction("Show all Q states", self)
        train_menu.addAction(self.show_q_state_button_action)

        train_menu.addSeparator()

        update_weights_menu_button = QAction("Open Weight Edit Box", self)
        update_weights_menu_button.triggered.connect(self.update_weights_dialog_box.exec)
        train_menu.addAction(update_weights_menu_button)

        self.run_eval_func_training_menu_button_action = QAction("Run Evaluation Function Training", self)
        self.run_eval_func_training_menu_button_action.setStatusTip("Run Evaluation Function Training")
        self.run_eval_func_training_menu_button_action.triggered.connect(self.eval_func_training_dialog_box.exec)
        train_menu.addAction(self.run_eval_func_training_menu_button_action)

        self.run_bfpm_menu_button_action = QAction("Run Brute Force Payof Matrix", self)
        train_menu.addAction(self.run_bfpm_menu_button_action)

        # View Menu
        view_menu = self.menuBar().addMenu("View")

        self.update_graphics_menu_toggle_action = QAction("Update Graphics", self)
        self.update_graphics_menu_toggle_action.setCheckable(True)
        self.update_graphics_menu_toggle_action.setChecked(True)
        view_menu.addAction(self.update_graphics_menu_toggle_action)

        # Game Menu
        game_menu = self.menuBar().addMenu("Game")

        # TODO: make the menus that are used locally to be only used locally
        self.run_multiple_games_menu_button_action = QAction("Run Multiple Games...", self)
        self.run_multiple_games_menu_button_action.setStatusTip("Run Multiple Games")
        self.run_multiple_games_menu_button_action.triggered.connect(self.multiple_games_dialog_box.exec)
        game_menu.addAction(self.run_multiple_games_menu_button_action)

        self.run_tournament_menu_button_action = QAction("Run Round Robin Tournament...", self)
        self.run_tournament_menu_button_action.setStatusTip("Run Round Robin Tournament")
        self.run_tournament_menu_button_action.triggered.connect(self.tournament_dialog_box.exec)
        game_menu.addAction(self.run_tournament_menu_button_action)
        #
        # help_menu = self.menuBar().addMenu("Help")
        #
        # about_menu = self.menuBar().addMenu("About")

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

        # self.multi_game_end_dialog_box.game_score_list_label.setText(str(score_list))

        self.multi_game_end_dialog_box.exec()

    def tournament_end_prompt(self, participants, no_of_games, results):

        self.tournament_end_dialog_box.create_table(participants, results)

        self.tournament_end_dialog_box.exec()

        pass

    def TEF_end_prompt(self, no_generations, best_weight):

        for i, weight in enumerate(best_weight):
            best_weight[i] = round(weight, 3)

        self.eval_func_training_end_dialog_box.no_generations_label.setText(str(no_generations))
        self.eval_func_training_end_dialog_box.final_weight = best_weight
        self.eval_func_training_end_dialog_box.best_weight_label.setText(str(best_weight))

        self.eval_func_training_end_dialog_box.exec()
        pass
    #
    # def update_status_bar_message(self, message):
    #     self.status_bar.showMessage(message)

    def update_status_bar_message(self, status, mode, games_left, random):

        self.status_current_status_label.setText(status)

        match mode:
            case 0:
                self.status_mode_label.setText("Mode: Normal")
            case 1:
                self.status_mode_label.setText("Mode: Multi-Game")
            case 2:
                self.status_mode_label.setText("Mode: Round Robin Tournament")
            case 3:
                self.status_mode_label.setText("Mode: Loading")
            case 4:
                self.status_mode_label.setText("Mode: Evaluation Function Training")
            case 5:
                self.status_mode_label.setText("Mode: Payoff Matrix Brute Force")

        self.status_games_left_label.setText("Games Left: " + str(games_left))

        self.status_random_label.setText(random)


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