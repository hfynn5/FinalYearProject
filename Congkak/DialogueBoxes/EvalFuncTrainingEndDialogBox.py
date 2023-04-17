import sys

from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, \
    QDialogButtonBox, QLabel, QVBoxLayout, QGridLayout, QComboBox, QSpinBox, QCheckBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QAbstractTableModel

from PyQt6 import QtGui, QtCore

class EvalFuncTrainingEndDialogBox(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ended Evaluation Function Training")

        self.no_generations_label = QLabel("")
        self.best_weight_label = QLabel("")

        self.final_weight = []

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.apply_weights_max_agent_a_button = QPushButton("Update max agent A", self)
        self.apply_weights_max_agent_b_button = QPushButton("Update max agent B", self)
        self.apply_weights_minimax_agent_a_button = QPushButton("Update minimax agent A", self)
        self.apply_weights_minimax_agent_b_button = QPushButton("Update minimax agent B", self)

        layout = QGridLayout()

        layout.addWidget(QLabel("Evaluation Function Trained"), 0, 0)
        layout.addWidget(QLabel("Number of generations: "), 1, 0)
        layout.addWidget(QLabel("Best weights: "), 2, 0)

        layout.addWidget(self.no_generations_label, 1, 1)
        layout.addWidget(self.best_weight_label, 2, 1)

        layout.addWidget(self.apply_weights_max_agent_a_button, 3, 0)
        layout.addWidget(self.apply_weights_max_agent_b_button, 3, 1)
        layout.addWidget(self.apply_weights_minimax_agent_a_button, 4, 0)
        layout.addWidget(self.apply_weights_minimax_agent_b_button, 4, 1)

        layout.addWidget(self.buttonBox, 5, 1)

        self.setLayout(layout)
