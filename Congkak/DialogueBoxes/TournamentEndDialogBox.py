import sys

from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, \
    QDialogButtonBox, QLabel, QVBoxLayout, QGridLayout, QComboBox, QSpinBox, QCheckBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QAbstractTableModel

from PyQt6 import QtGui, QtCore

class TournamentEndDialogBox(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tournament End")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def create_table(self, participants, results):

        layout = QGridLayout()

        y_offset = 1
        x_offset = 0

        layout.addWidget(QLabel("Round Robin Results"), 0, 0)

        for m, participant_a in enumerate(participants):

            layout.addWidget(QLabel(participant_a), m + y_offset + 1, x_offset)
            layout.addWidget(QLabel(participant_a), y_offset, m + x_offset + 1)

            for n, participant_b in enumerate(participants):

                layout.addWidget(QLabel(str(results[m][n])), m + y_offset + 1, n + x_offset + 1)

        layout.addWidget(self.buttonBox, len(participants) + y_offset + 2, 1)

        self.setLayout(layout)


