import sys

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel,  QGridLayout, QComboBox, QSpinBox

from PyQt6 import QtGui


class MultipleGamesDialogBox(QDialog):

    def __init__(self):

        super().__init__()

        self.player_a_agent = 1
        self.player_b_agent = 1
        self.number_of_games = 1

        self.setWindowTitle("Run Multiple Games")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QGridLayout()

        self.player_a_dropdown = QComboBox(self)
        self.player_a_dropdown.addItems(['Random', 'Max', 'Minimax', 'MCTS'])

        self.player_a_dropdown.activated.\
            connect(lambda index=self.player_a_dropdown.currentIndex(): self.set_player_a_agent(index))

        self.player_b_dropdown = QComboBox(self)
        self.player_b_dropdown.addItems(['Random', 'Max', 'Minimax', 'MCTS'])

        self.player_b_dropdown.activated.\
            connect(lambda index=self.player_b_dropdown.currentIndex(): self.set_player_b_agent(index))

        self.game_count_spin_box = QSpinBox()
        self.game_count_spin_box.setMinimum(1)
        self.game_count_spin_box.setMaximum(999)
        self.game_count_spin_box.setSuffix(" rounds")
        self.game_count_spin_box.setSingleStep(1)
        self.game_count_spin_box.valueChanged.connect(self.no_games_changed)

        layout.addWidget(QLabel("Set player A agent: "), 0, 0)
        layout.addWidget(QLabel("Set player B agent: "), 1, 0)
        layout.addWidget(QLabel("Number of Rounds: "), 2, 0)
        layout.addWidget(self.player_a_dropdown, 0, 1)
        layout.addWidget(self.player_b_dropdown, 1, 1)
        layout.addWidget(self.game_count_spin_box, 2, 1)
        layout.addWidget(self.buttonBox, 3, 1)

        self.setLayout(layout)

    def exec(self) -> int:
        self.number_of_games = 1
        self.player_a_agent = 1
        self.player_b_agent = 1

        self.player_a_dropdown.setCurrentIndex(0)
        self.player_b_dropdown.setCurrentIndex(0)
        self.game_count_spin_box.setValue(1)

        super().exec()

    def no_games_changed(self, count):
        self.number_of_games = count

    def set_player_a_agent(self, i):
        self.player_a_agent = i + 1

    def set_player_b_agent(self, i):
        self.player_b_agent = i + 1

    def get_no_games(self):
        return self.number_of_games
