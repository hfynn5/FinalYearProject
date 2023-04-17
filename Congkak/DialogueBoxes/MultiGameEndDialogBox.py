import sys

from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, \
    QDialogButtonBox, QLabel, QVBoxLayout, QGridLayout, QComboBox, QSpinBox, QCheckBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QAbstractTableModel

from PyQt6 import QtGui, QtCore

class MultiGameEndDialogBox(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("End Multiple Game")

        self.no_games_played_label = QLabel("")
        self.player_a_score_label = QLabel("")
        self.player_b_score_label = QLabel("")
        self.draws_label = QLabel("")
        self.game_score_list_label = QLabel("")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QGridLayout()

        layout.addWidget(QLabel("Multiple Games Ran"), 0, 0)
        layout.addWidget(QLabel("Number of games ran: "), 1, 0)
        layout.addWidget(QLabel("Player A score: "), 2, 0)
        layout.addWidget(QLabel("Player B score: "), 3, 0)
        layout.addWidget(QLabel("Draws: "), 4, 0)
        # layout.addWidget(QLabel("Game results: "), 5, 0)

        layout.addWidget(self.no_games_played_label, 1, 1)
        layout.addWidget(self.player_a_score_label, 2, 1)
        layout.addWidget(self.player_b_score_label, 3, 1)
        layout.addWidget(self.draws_label, 4, 1)
        # layout.addWidget(self.game_score_list_label, 6, 0)

        layout.addWidget(self.buttonBox, 7, 1)

        self.setLayout(layout)


