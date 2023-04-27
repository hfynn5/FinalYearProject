import sys

from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, \
    QDialogButtonBox, QLabel, QVBoxLayout, QGridLayout, QComboBox, QSpinBox, QCheckBox

from PyQt6 import QtGui

class TournamentDialogBox(QDialog):

    def __init__(self):
        super().__init__()

        self.tournament_participants = []
        self.number_of_games = 1
        self.player_simul_agent = 1

        self.setWindowTitle("Run Round Robin Tournament")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QGridLayout()

        self.player_simul_dropdown = QComboBox(self)
        self.player_simul_dropdown.addItems(['Random', 'R Learning', 'Q Learning', 'Preset'])
        self.player_simul_dropdown.activated. \
            connect(lambda index=self.player_simul_dropdown.currentIndex(): self.set_player_simul_agent(index))

        self.is_random_participate_checkbox = QCheckBox()
        self.is_random_participate_checkbox.setChecked(False)
        self.is_random_participate_checkbox.stateChanged.connect(self.add_random_agent)

        self.is_max_participate_checkbox = QCheckBox()
        self.is_max_participate_checkbox.setChecked(False)
        self.is_max_participate_checkbox.stateChanged.connect(self.add_max_agent)

        self.is_minimax_participate_checkbox = QCheckBox()
        self.is_minimax_participate_checkbox.setChecked(False)
        self.is_minimax_participate_checkbox.stateChanged.connect(self.add_minimax_agent)

        self.game_count_spin_box = QSpinBox()
        self.game_count_spin_box.setMinimum(1)
        self.game_count_spin_box.setMaximum(999)
        self.game_count_spin_box.setSuffix(" rounds")
        self.game_count_spin_box.setSingleStep(1)
        self.game_count_spin_box.valueChanged.connect(self.no_games_changed)

        layout.addWidget(QLabel("Round Robin Tournament Participants:"), 0, 0)
        layout.addWidget(QLabel("Random Agent"), 1, 0)
        layout.addWidget(QLabel("Max Agent"), 2, 0)
        layout.addWidget(QLabel("Minimax Agent"), 3, 0)
        layout.addWidget(QLabel("Simul Agent"), 4, 0)
        layout.addWidget(QLabel("Number of Games per Round"), 5, 0)

        layout.addWidget(self.is_random_participate_checkbox, 1, 1)
        layout.addWidget(self.is_max_participate_checkbox, 2, 1)
        layout.addWidget(self.is_minimax_participate_checkbox, 3, 1)
        layout.addWidget(self.player_simul_dropdown, 4, 1)
        layout.addWidget(self.game_count_spin_box, 5, 1)
        layout.addWidget(self.buttonBox, 6, 1)

        self.setLayout(layout)

    def no_games_changed(self, count):
        self.number_of_games = count

    def set_player_simul_agent(self, i):
        self.player_simul_agent = i + 1

    def add_random_agent(self,state):
        if state:
            self.tournament_participants.append(1)
        else:
            self.tournament_participants.remove(1)

    def add_max_agent(self,state):
        if state:
            self.tournament_participants.append(2)
        else:
            self.tournament_participants.remove(2)

    def add_minimax_agent(self,state):
        if state:
            self.tournament_participants.append(3)
        else:
            self.tournament_participants.remove(3)