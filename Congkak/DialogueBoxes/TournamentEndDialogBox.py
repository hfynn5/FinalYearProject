import sys

from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, \
    QDialogButtonBox, QLabel, QVBoxLayout, QGridLayout, QComboBox, QSpinBox, QCheckBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QAbstractTableModel

from PyQt6 import QtGui, QtCore


# class TableView(QTableWidget):
#     def __init__(self, data, labels, *args):
#         QTableWidget.__init__(self, *args)
#         self.data = data
#         self.labels = labels
#         self.setData()
#         self.resizeColumnsToContents()
#         self.resizeRowsToContents()
#
#     def setData(self):
#         # horHeaders = []
#         for n, key in enumerate(sorted(self.data.keys())):
#             # horHeaders.append(key)
#             for m, item in enumerate(self.data[key]):
#                 newitem = QTableWidgetItem(item)
#                 self.setItem(m, n, newitem)
#         # self.setHorizontalHeaderLabels(horHeaders)

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

            layout.addWidget(QLabel(participant_a), m + y_offset, x_offset)
            layout.addWidget(QLabel(participant_a), y_offset, m + x_offset)

            for n, participant_b in enumerate(participants):

                layout.addWidget(QLabel(str(results[m][n])), m + y_offset, n + x_offset)

        layout.addWidget(self.buttonBox, len(participants + y_offset + 1), 1)


