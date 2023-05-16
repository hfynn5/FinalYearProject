from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel,  QGridLayout, QComboBox, QSpinBox


class EvalFuncTrainingDialogBox(QDialog):

    def __init__(self):

        super().__init__()

        self.max_generation_count = 0
        self.no_of_games = 1
        self.pop_size = 4
        self.player_agent = 2

        self.setWindowTitle("Train Evaluation Function")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QGridLayout()

        pop_size_spin_box = QSpinBox()
        pop_size_spin_box.setMinimum(0)
        pop_size_spin_box.setMaximum(40)
        pop_size_spin_box.setValue(4)
        pop_size_spin_box.setSuffix(" individuals")
        pop_size_spin_box.setSingleStep(4)
        pop_size_spin_box.valueChanged.connect(self.pop_size_changed)

        max_gen_spin_box = QSpinBox()
        max_gen_spin_box.setMinimum(0)
        max_gen_spin_box.setMaximum(999)
        max_gen_spin_box.setValue(1)
        max_gen_spin_box.setSuffix(" generations")
        max_gen_spin_box.setSingleStep(1)
        max_gen_spin_box.valueChanged.connect(self.max_gen_changed)

        game_count_spin_box = QSpinBox()
        game_count_spin_box.setMinimum(1)
        game_count_spin_box.setMaximum(10)
        game_count_spin_box.setValue(1)
        game_count_spin_box.setSuffix(" games")
        game_count_spin_box.setSingleStep(1)
        game_count_spin_box.valueChanged.connect(self.no_games_changed)

        agent_dropdown = QComboBox(self)
        agent_dropdown.addItems(['Max', 'Minimax'])
        agent_dropdown.activated. \
            connect(lambda index=agent_dropdown.currentIndex(): self.set_player_agent(index))

        layout.addWidget(QLabel("Set population size: "), 0, 0)
        layout.addWidget(QLabel("Set max number of generations: "), 1, 0)
        layout.addWidget(QLabel("Set number of games per round: "), 2, 0)
        layout.addWidget(QLabel("Set agent used: "), 3, 0)

        layout.addWidget(pop_size_spin_box, 0, 1)
        layout.addWidget(max_gen_spin_box, 1, 1)
        layout.addWidget(game_count_spin_box, 2, 1)
        layout.addWidget(agent_dropdown, 3, 1)
        layout.addWidget(self.buttonBox, 4, 1)

        self.setLayout(layout)

        pass

    def no_games_changed(self, count):
        self.no_of_games = count

    def max_gen_changed(self, count):
        self.max_generation_count = count

    def pop_size_changed(self, count):
        self.pop_size = count

    def set_player_agent(self, i):
        self.player_agent = i + 2


