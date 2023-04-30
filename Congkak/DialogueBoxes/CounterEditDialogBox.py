import sys

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel,  QGridLayout, QComboBox, QSpinBox

from PyQt6 import QtGui


class CounterEditDialogBox(QDialog):

    def __init__(self):

        super().__init__()

        self.player_a_houses = [0, 0, 0, 0, 0, 0, 0]
        self.player_b_houses = [0, 0, 0, 0, 0, 0, 0]
        self.player_a_storeroom = 0
        self.player_b_storeroom = 0

        self.wheel_a = []
        self.wheel_b = []
        self.wheel_store_a = QSpinBox()
        self.wheel_store_b = QSpinBox()

        self.setWindowTitle("Edit Counter Count")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QGridLayout()

        layout.addWidget(QLabel("Set Player A Houses: "), 0, 0)
        layout.addWidget(QLabel("Set Player B Houses: "), 1, 0)
        layout.addWidget(QLabel("Set Player A Storeroom: "), 2, 0)
        layout.addWidget(QLabel("Set Player B Storeroom: "), 3, 0)

        for i in range(7):
            wheel = QSpinBox()
            wheel.setMinimum(0)
            wheel.setMaximum(100)
            wheel.setSingleStep(1)
            wheel.valueChanged.connect(
                lambda checked, hole=i+1, value=wheel.value(): self.update_house('a', hole, value))
            layout.addWidget(wheel, 0, i+1)

            self.wheel_a.append(wheel)

            wheel = QSpinBox()
            wheel.setMinimum(0)
            wheel.setMaximum(100)
            wheel.setSingleStep(1)
            wheel.valueChanged.connect(
                lambda checked, hole=i + 1, value=wheel.value(): self.update_house('b', hole, value))
            layout.addWidget(wheel, 1, i + 1)

            self.wheel_b.append(wheel)
            pass

        wheel = QSpinBox()
        wheel.setMinimum(0)
        wheel.setMaximum(100)
        wheel.setSingleStep(1)
        wheel.valueChanged.connect(
            lambda checked, value=wheel.value(): self.update_storeroom('a', value))
        layout.addWidget(wheel, 3, 1)
        self.wheel_store_a = wheel

        wheel = QSpinBox()
        wheel.setMinimum(0)
        wheel.setMaximum(100)
        wheel.setSingleStep(1)
        wheel.valueChanged.connect(
            lambda checked, value=wheel.value(): self.update_storeroom('b', value))
        layout.addWidget(wheel, 4, 1)
        self.wheel_store_b = wheel

        layout.addWidget(self.buttonBox, 5, 1)

        self.setLayout(layout)

    def update_house(self, player, hole, value):

        if player == 'a':

            value = self.wheel_a[hole - 1].value()
            self.player_a_houses[hole - 1] = value
        elif player == 'b':

            value = self.wheel_b[hole - 1].value()
            self.player_b_houses[hole - 1] = value

        print(self.player_a_houses)
        print(self.player_b_houses)
        print("player: " + player + " hole: " + str(hole) + " vlaue: " + str(value))

    def update_storeroom(self, player, value):

        if player == 'a':
            value = self.wheel_store_a.value()
            self.player_a_storeroom = value
        elif player == 'b':
            value = self.wheel_store_b.value()
            self.player_b_storeroom = value

        print(self.player_a_storeroom)
        print(self.player_b_storeroom)

        print("player: " + player + " vlaue: " + str(value))
