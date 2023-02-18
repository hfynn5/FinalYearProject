from graphics import *
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QPainter, QPen, QAction, QIcon
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QPoint, Qt
import sys


class BoardGraphic(QMainWindow):
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

        self.player_a_dropdown = QComboBox()
        self.player_b_dropdown = QComboBox()

        self.play_speed_slider = QSlider()
        self.play_button = QPushButton()

        self.acceptDrops()
        # set the title
        self.setWindowTitle("Congkak")

        # setting the geometry of window
        self.setGeometry(100, 100, 800, 600)

        self.generate_points()

        self.create_hole_text()
        self.create_buttons()
        self.create_ui()

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
        self.house_b_positions.reverse()

    # Draws all the circles
    # TODO: add a list of all the circles to edit and show hand position
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

    # create the label for all the holes
    def create_hole_text(self):

        offset = QPoint(-4, -15)

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

    # create all buttons
    def create_buttons(self):

        offset = QPoint(-22, -60)

        # count = 7

        for pos in self.house_a_positions:
            button = QPushButton(self)
            button.resize(40, 25)
            button.move(pos + offset)
            button.setText("Pick")
            self.house_a_buttons.append(button)

            # count -= 1

        # count = 7

        offset = QPoint(-22, 40)

        for pos in self.house_b_positions:
            button = QPushButton(self)
            button.resize(40, 25)
            button.move(pos + offset)
            button.setText("Pick")
            self.house_b_buttons.append(button)

    # creats the UI.
    # TODO split into inputs and menus
    def create_ui(self):

        self.player_a_dropdown = QComboBox(self)
        self.player_a_dropdown.move(650, 100)
        self.player_a_dropdown.addItems(['Random', 'Minimax', 'MCTS', 'Human'])

        self.player_b_dropdown = QComboBox(self)
        self.player_b_dropdown.move(650, 380)
        self.player_b_dropdown.addItems(['Random', 'Minimax', 'MCTS', 'Human'])

        slider_label = QLabel(self)
        slider_label.move(360, 500)
        slider_label.setText("Moves Per Second")

        self.play_speed_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.play_speed_slider.setGeometry(200, 450, 400, 50)
        self.play_speed_slider.setMinimum(1)
        self.play_speed_slider.setMaximum(20)
        self.play_speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.play_speed_slider.setTickInterval(1)

        self.play_button = QPushButton(self)
        self.play_button.setGeometry(150,450,40,25)
        self.play_button.setText("Play")

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
    def update_values(self, house_a_values, house_b_values, storeroom_a_value, storeroom_b_value):

        for i, label in enumerate(self.house_a_text_labels):
            label.setText(str(house_a_values[i]))

        for i, label in enumerate(self.house_b_text_labels):
            label.setText(str(house_b_values[i]))

        self.storeroom_a_text_label.setText(str(storeroom_a_value))
        self.storeroom_b_text_label.setText(str(storeroom_b_value))

    # enable or disable the inputs
    def set_enable_inputs(self, enable):
        for button in self.house_a_buttons:
            button.setEnabled(enable)
        for button in self.house_b_buttons:
            button.setEnabled(enable)


