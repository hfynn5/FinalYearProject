import sys

from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, \
    QDialogButtonBox, QLabel, QVBoxLayout, QGridLayout, QComboBox, QSpinBox, QCheckBox

from PyQt6 import QtGui

class GameEndDialogBox(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("End Game")

        self.winner_label = QLabel("")
        self.player_a_score_label = QLabel("")
        self.player_b_score_label = QLabel("")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QGridLayout()

        layout.addWidget(QLabel("Game has ended"), 0, 0)
        layout.addWidget(QLabel("Winner: "), 1, 0)
        layout.addWidget(self.winner_label, 1, 1)

        layout.addWidget(QLabel("Player A score"), 2, 0)
        layout.addWidget(QLabel("Player B score"), 3, 0)
        layout.addWidget(self.player_a_score_label, 2, 1)
        layout.addWidget(self.player_b_score_label, 3, 1)

        layout.addWidget(self.buttonBox, 4, 1)

        self.setLayout(layout)
