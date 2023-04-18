import sys

from PyQt6.QtWidgets import QDialog, QPushButton, \
    QDialogButtonBox, QLabel, QGridLayout, QDoubleSpinBox

from PyQt6 import QtGui, QtCore

class UpdateWeightsDialogBox(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edit Weights of Max and Minimax agents")

        self.final_weight = [0, 0, 0, 0, 0, 0]

        QBtn = QDialogButtonBox.StandardButton.Close

        self.buttonBox = QDialogButtonBox(QBtn)
        # self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.apply_weights_max_agent_a_button = QPushButton("Update max agent A", self)
        self.apply_weights_max_agent_b_button = QPushButton("Update max agent B", self)
        self.apply_weights_minimax_agent_a_button = QPushButton("Update minimax agent A", self)
        self.apply_weights_minimax_agent_b_button = QPushButton("Update minimax agent B", self)

        layout = QGridLayout()

        self.h1_spin_box = QDoubleSpinBox()
        self.h1_spin_box.setMinimum(0)
        self.h1_spin_box.setMaximum(1)
        self.h1_spin_box.setSingleStep(0.001)
        self.h1_spin_box.setDecimals(5)
        self.h1_spin_box.valueChanged.connect(lambda value=self.h1_spin_box.value(), index=0:
                                              self.update_weight(index, value))

        self.h2_spin_box = QDoubleSpinBox()
        self.h2_spin_box.setMinimum(0)
        self.h2_spin_box.setMaximum(1)
        self.h2_spin_box.setSingleStep(0.001)
        self.h2_spin_box.setDecimals(5)
        self.h2_spin_box.valueChanged.connect(lambda value=self.h2_spin_box.value(), index=1:
                                              self.update_weight(index, value))

        self.h3_spin_box = QDoubleSpinBox()
        self.h3_spin_box.setMinimum(0)
        self.h3_spin_box.setMaximum(1)
        self.h3_spin_box.setSingleStep(0.001)
        self.h3_spin_box.setDecimals(5)
        self.h3_spin_box.valueChanged.connect(lambda value=self.h3_spin_box.value(), index=2:
                                              self.update_weight(index, value))

        self.h4_spin_box = QDoubleSpinBox()
        self.h4_spin_box.setMinimum(0)
        self.h4_spin_box.setMaximum(1)
        self.h4_spin_box.setSingleStep(0.001)
        self.h4_spin_box.setDecimals(5)
        self.h4_spin_box.valueChanged.connect(lambda value=self.h4_spin_box.value(), index=3:
                                              self.update_weight(index, value))

        self.h5_spin_box = QDoubleSpinBox()
        self.h5_spin_box.setMinimum(0)
        self.h5_spin_box.setMaximum(1)
        self.h5_spin_box.setSingleStep(0.001)
        self.h5_spin_box.setDecimals(5)
        self.h5_spin_box.valueChanged.connect(lambda value=self.h5_spin_box.value(), index=4:
                                              self.update_weight(index, value))

        self.h6_spin_box = QDoubleSpinBox()
        self.h6_spin_box.setMinimum(0)
        self.h6_spin_box.setMaximum(1)
        self.h6_spin_box.setSingleStep(0.001)
        self.h6_spin_box.setDecimals(5)
        self.h6_spin_box.valueChanged.connect(lambda value=self.h6_spin_box.value(), index=5:
                                              self.update_weight(index, value))

        layout.addWidget(QLabel("Update Weights"), 0, 0)
        layout.addWidget(QLabel("H1: Maximise the total number of counters in the player’s houses"), 1, 0)
        layout.addWidget(QLabel("H2: Maximise the number of houses on the player’s side with counters"), 2, 0)
        layout.addWidget(QLabel("H3: Maximise the number of counters in the player’s storeroom"), 3, 0)
        layout.addWidget(QLabel("H4: Minimise the number of counters in the opponent’s storeroom"), 4, 0)
        layout.addWidget(QLabel("H5: Maximise the number of repeated turns the player takes"), 5, 0)
        layout.addWidget(QLabel("H6: Maximise the difference of counters in both players’ storeroom"), 6, 0)

        layout.addWidget(self.h1_spin_box, 1, 1)
        layout.addWidget(self.h2_spin_box, 2, 1)
        layout.addWidget(self.h3_spin_box, 3, 1)
        layout.addWidget(self.h4_spin_box, 4, 1)
        layout.addWidget(self.h5_spin_box, 5, 1)
        layout.addWidget(self.h6_spin_box, 6, 1)

        layout.addWidget(self.apply_weights_max_agent_a_button, 7, 0)
        layout.addWidget(self.apply_weights_max_agent_b_button, 7, 1)
        layout.addWidget(self.apply_weights_minimax_agent_a_button, 8, 0)
        layout.addWidget(self.apply_weights_minimax_agent_b_button, 8, 1)

        layout.addWidget(self.buttonBox, 9, 1)

        self.setLayout(layout)

    def update_weight(self, index, value):
        self.final_weight[index] = value

        print(self.final_weight)

