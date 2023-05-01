import copy
import sys
import time
import traceback

from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool
from PyQt6.QtWidgets import *

from Congkak.CongkakBoardGraphics import BoardGraphic
from Congkak.CongkakBoardModel import BoardModel
from Congkak.EvalFuncTrainer import EvalFuncTrainer
from Congkak.Hand import Hand
from Congkak.IntelligentAgents.MaxAgent import MaxAgent
from Congkak.IntelligentAgents.MinimaxAgent import MinimaxAgent
from Congkak.IntelligentAgents.QLearningSimulAgent import QLearningSimulAgent
from Congkak.IntelligentAgents.ReinforcementLearningSimulAgent import ReinforcementLearningSimulAgent
from Congkak.IntelligentAgents.RandomAgent import RandomAgent
from Congkak.IntelligentAgents.PresetSimulAgent import PresetSimulAgent

from statistics import mean


class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        self.signals = WorkerSignals()

    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        # Retrieve args/kwargs here; and fire processing using them

        try:
            # for x in range(5):
            #
            #     start_time = time.time()
            #
            #     while time.time() - start_time < 1:
            #         pass
            #     print("ping")
            #     result = self.fn()

            result = self.fn(*self.args, **self.kwargs)

        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


# updates board graphic
def update_board_graphics(board_graphic: BoardGraphic, board_model: BoardModel):
    if board_model.waiting:
        board_model.pause = True
        copied_board_model = copy.deepcopy(board_model)
        board_model.pause = False

        board_graphic.update_values(house_a_values=copied_board_model.house_a_values,
                                    house_b_values=copied_board_model.house_b_values,
                                    storeroom_a_value=copied_board_model.storeroom_a_value,
                                    storeroom_b_value=copied_board_model.storeroom_b_value,
                                    player_a_hand=copied_board_model.player_a_hand,
                                    player_b_hand=copied_board_model.player_b_hand)


def error_handler(etype, value, tb):
    error_msg = ''.join(traceback.format_exception(etype, value, tb))
    # do something with the error message, for example print it
    print(error_msg)


class GameManager:
    AGENT_USER = 'user'
    AGENT_RANDOM = 'random'
    AGENT_MAX = 'max'
    AGENT_MINIMAX = 'minimax'
    AGENT_MCTS = 'mcts'

    AGENT_Q_SIMUL = 'q simul'
    AGENT_R_SIMUL = 'r simul'
    AGENT_PRESET_SIMUL = 'preset simul'

    LIST_OF_AGENTS_NAME = [AGENT_USER, AGENT_RANDOM, AGENT_MAX, AGENT_MINIMAX]
    LIST_OF_SIMUL_AGENTS_NAME = [AGENT_USER, AGENT_RANDOM, AGENT_R_SIMUL, AGENT_Q_SIMUL, AGENT_PRESET_SIMUL]
    # if update, make sure to update the list below.

    PLAYER_A_WIN = 1
    PLAYER_B_WIN = -1
    DRAW = 0

    NORMAL_MODE = 0
    MULTI_GAME_MODE = 1
    ROUND_ROBIN_MODE = 2
    LOADING_MODE = 3
    EVAL_TRAINING_MODE = 4
    BFPM_MODE = 5

    def __init__(self):

        sys.excepthook = error_handler

        self.player_a_hand_pos = -1
        self.player_b_hand_pos = -1

        # user, random, max, minimax, mcts
        # self.agent_list = [self.AGENT_USER, self.AGENT_RANDOM, self.AGENT_MAX, self.AGENT_MINIMAX, self.AGENT_MCTS]
        self.player_a_agent_name = self.AGENT_USER
        self.player_b_agent_name = self.AGENT_USER
        self.player_a_simul_agent_index = self.AGENT_USER
        self.player_b_simul_agent_index = self.AGENT_USER

        self.player_a_agent = RandomAgent()
        self.player_b_agent = RandomAgent()
        self.player_a_agent_simul = RandomAgent()
        self.player_b_agent_simul = RandomAgent()

        # create Intelligent Agents
        self.max_depth = 5
        self.minmax_depth = 5
        self.default_weights = [0.15, 0.363, 0.806, 0.335, 0.014, 0.828]
        self.is_training_state_agents = False

        self.random_agent = RandomAgent()
        # self.max_agent = MaxAgent(max_depth=self.max_depth, weights=[0, 0, 0, 0, 0, 1])
        # self.minimax_agent = MinimaxAgent(weights=[0, 0, 0, 0, 0, 1], maximum_depth=self.minmax_depth, maximum_self_depth=0,
        #                                   maximum_number_node=0)
        self.max_agent_a = MaxAgent(max_depth=self.max_depth, weights=self.default_weights)
        self.max_agent_b = MaxAgent(max_depth=self.max_depth, weights=self.default_weights)
        self.minimax_agent_a = MinimaxAgent(weights=self.default_weights, maximum_depth=self.minmax_depth,
                                            maximum_self_depth=0,
                                            maximum_number_node=0)
        self.minimax_agent_b = MinimaxAgent(weights=self.default_weights, maximum_depth=self.minmax_depth,
                                            maximum_self_depth=0,
                                            maximum_number_node=0)

        self.q_simul_agent = QLearningSimulAgent()
        self.rl_simul_agent = ReinforcementLearningSimulAgent()
        self.preset_simul_agent = PresetSimulAgent()

        self.list_of_art_agents_a = [None, self.random_agent, self.max_agent_a, self.minimax_agent_a]
        self.list_of_art_agents_b = [None, self.random_agent, self.max_agent_a, self.minimax_agent_a]
        self.list_of_simul_art_agents = [None, self.random_agent, self.rl_simul_agent, self.q_simul_agent, self.preset_simul_agent]
        # if update, make sure to update the list above.

        # training evaluation function
        self.trainer_pop_size = 40
        self.trainer_chromosome_size = 6
        self.trainer_std_dev = 0.1
        self.eval_func_trainer = EvalFuncTrainer(10, 20,
                                                 self.trainer_chromosome_size,
                                                 self.trainer_std_dev)
        self.TEF_individual_a = MaxAgent(max_depth=5, weights=[0, 0, 0, 0, 0, 0])
        self.TEF_individual_b = MaxAgent(max_depth=5, weights=[0, 0, 0, 0, 0, 0])
        self.TEF_population = None
        self.TEF_individual_a_index = 0
        self.TEF_individual_b_index = 0
        self.TEF_generation_count = 0

        self.game_has_ended = False
        self.show_starting_hands = True
        self.autoplay_hands = False

        # For graphics
        self.graphic_refresh_rate = 0.01
        self.update_graphic = True

        self.current_mode = self.NORMAL_MODE

        # for loading
        self.loaded_moves = []
        self.move_counter = 0

        # for multi games
        self.no_of_games_to_run = 0
        self.no_of_games_left = 0
        self.game_results = []

        # for round robin
        self.round_robin_results = [[0 for x in range(len(self.LIST_OF_AGENTS_NAME) - 1)]
                                    for x in range(len(self.LIST_OF_AGENTS_NAME) - 1)]
        self.tournament_participants = []
        self.round_robin_simul_agent = RandomAgent()

        # for brute force
        self.bfpm_player_a_choice = -1
        self.bfpm_player_b_choice = -1
        self.payoff_matrix = [[0 for x in range(7)]
                                    for x in range(7)]

        # declare threadpool
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(3)
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        # declare board model
        self.board_model = BoardModel()
        self.board_model.ping = False

        # declare graphics
        app = QApplication(sys.argv)
        self.board_graphic = BoardGraphic()
        self.board_graphic.show()
        self.connect_inputs_to_functions()

        # start constantly updating graphics
        self.start_worker_graphic_updater()

        self.next_action(BoardModel.PROMPT_SOWING_BOTH)

        sys.exit(app.exec())

    # connect the available input to its functions
    def connect_inputs_to_functions(self):
        for i, button in enumerate(self.board_graphic.house_a_buttons):
            button.clicked.connect(lambda checked, value=i + 11: self.choosing_hole_action('a', value))

        for i, button in enumerate(self.board_graphic.house_b_buttons):
            button.clicked.connect(lambda checked, value=i + 21: self.choosing_hole_action('b', value))

        self.board_graphic.play_button.clicked.connect(lambda checked:
                                                       self.start_worker_simultaneous_sowing(
                                                           hole_a=self.player_a_hand_pos,
                                                           hole_b=self.player_b_hand_pos,
                                                           simul_prompt=True
                                                       ))

        self.board_graphic.move_speed_slider. \
            valueChanged.connect(lambda value=self.board_graphic.move_speed_slider.value():
                                 self.update_sowing_speed(value))

        self.board_graphic.save_game_menu_button_action.triggered.connect(lambda checked: self.save_moves())
        self.board_graphic.load_game_menu_button_action.triggered.connect(lambda checked: self.load_moves())
        self.board_graphic.new_game_menu_button_action.triggered.connect(lambda checked: self.new_game(False))

        self.board_graphic.update_graphics_menu_toggle_action.triggered.connect(self.toggle_update_graphics)
        self.board_graphic.train_state_agent_menu_toggle_action.triggered.connect(self.toggle_learning_state_agents)

        self.board_graphic.show_rl_state_button_action.triggered.connect(self.print_rl_states)
        self.board_graphic.show_q_state_button_action.triggered.connect(self.print_q_states)

        self.board_graphic.player_a_agent_dropdown. \
            activated.connect(lambda
                                  index=self.board_graphic.player_a_agent_dropdown.
                                      currentIndex(): self.set_player_agent_index('a', index))

        self.board_graphic.player_b_agent_dropdown. \
            activated.connect(lambda
                                  index=self.board_graphic.player_b_agent_dropdown.
                                      currentIndex(): self.set_player_agent_index('b', index))

        self.board_graphic.player_a_simul_agent_dropdown. \
            activated.connect(lambda
                                  index=self.board_graphic.player_a_agent_dropdown.
                                      currentIndex(): self.set_player_simul_agent_index('a', index))

        self.board_graphic.player_b_simul_agent_dropdown. \
            activated.connect(lambda
                                  index=self.board_graphic.player_b_agent_dropdown.
                                      currentIndex(): self.set_player_simul_agent_index('b', index))

        self.board_graphic.run_bfpm_menu_button_action.triggered.connect(self.brute_force_payoff_matrix)

        self.board_graphic.eval_func_training_dialog_box.buttonBox.accepted.connect(self.start_training_eval_function)

        self.board_graphic.eval_func_training_end_dialog_box. \
            apply_weights_max_agent_a_button.clicked.connect(lambda
                                                                 checked, max=True, minimax=False, player='a',
                                                                 weights=self.board_graphic.eval_func_training_end_dialog_box.final_weight:
                                                             self.set_max_and_minimax_agent_weights(player=player,
                                                                                                    is_max=max,
                                                                                                    is_minimax=minimax,
                                                                                                    weights=weights)
                                                             )

        self.board_graphic.eval_func_training_end_dialog_box. \
            apply_weights_max_agent_b_button.clicked.connect(lambda
                                                                 checked, max=True, minimax=False, player='b',
                                                                 weights=self.board_graphic.eval_func_training_end_dialog_box.final_weight:
                                                             self.set_max_and_minimax_agent_weights(player=player,
                                                                                                    is_max=max,
                                                                                                    is_minimax=minimax,
                                                                                                    weights=weights)
                                                             )

        self.board_graphic.eval_func_training_end_dialog_box. \
            apply_weights_minimax_agent_a_button.clicked.connect(lambda
                                                                     checked, max=False, minimax=True, player='a',
                                                                     weights=self.board_graphic.eval_func_training_end_dialog_box.final_weight:
                                                                 self.set_max_and_minimax_agent_weights(player=player,
                                                                                                        is_max=max,
                                                                                                        is_minimax=minimax,
                                                                                                        weights=weights)
                                                                 )

        self.board_graphic.eval_func_training_end_dialog_box. \
            apply_weights_minimax_agent_b_button.clicked.connect(lambda
                                                                     checked, max=False, minimax=True, player='b',
                                                                     weights=self.board_graphic.eval_func_training_end_dialog_box.final_weight:
                                                                 self.set_max_and_minimax_agent_weights(player=player,
                                                                                                        is_max=max,
                                                                                                        is_minimax=minimax,
                                                                                                        weights=weights)
                                                                 )

        self.board_graphic.update_weights_dialog_box. \
            apply_weights_max_agent_a_button.clicked.connect(lambda
                                                                 checked, max=True, minimax=False, player='a',
                                                                 weights=self.board_graphic.update_weights_dialog_box.final_weight:
                                                             self.set_max_and_minimax_agent_weights(player=player,
                                                                                                    is_max=max,
                                                                                                    is_minimax=minimax,
                                                                                                    weights=weights)
                                                             )

        self.board_graphic.update_weights_dialog_box. \
            apply_weights_max_agent_b_button.clicked.connect(lambda
                                                                 checked, max=True, minimax=False, player='b',
                                                                 weights=self.board_graphic.update_weights_dialog_box.final_weight:
                                                             self.set_max_and_minimax_agent_weights(player=player,
                                                                                                    is_max=max,
                                                                                                    is_minimax=minimax,
                                                                                                    weights=weights)
                                                             )

        self.board_graphic.update_weights_dialog_box. \
            apply_weights_minimax_agent_a_button.clicked.connect(lambda
                                                                     checked, max=False, minimax=True, player='a',
                                                                     weights=self.board_graphic.update_weights_dialog_box.final_weight:
                                                                 self.set_max_and_minimax_agent_weights(player=player,
                                                                                                        is_max=max,
                                                                                                        is_minimax=minimax,
                                                                                                        weights=weights)
                                                                 )

        self.board_graphic.update_weights_dialog_box. \
            apply_weights_minimax_agent_b_button.clicked.connect(lambda
                                                                     checked, max=False, minimax=True, player='b',
                                                                     weights=self.board_graphic.update_weights_dialog_box.final_weight:
                                                                 self.set_max_and_minimax_agent_weights(player=player,
                                                                                                        is_max=max,
                                                                                                        is_minimax=minimax,
                                                                                                        weights=weights)
                                                                 )


        self.board_graphic.multiple_games_dialog_box.buttonBox.accepted.connect(self.run_multiple_games)

        self.board_graphic.tournament_dialog_box.buttonBox.accepted.connect(self.run_round_robin_tournament)

        self.board_graphic.counter_edit_dialog_box.buttonBox.accepted.connect(self.edit_marble_count)

    # makes worker constantly update graphics
    def start_worker_graphic_updater(self):
        worker = Worker(self.update_board_graphics_constantly)
        self.threadpool.start(worker)

    # makes worker to start sowing
    def start_worker_sowing(self, player=None, hole=None, new_hand=None):

        if player == 'a':
            self.board_model.append_move(hole, 0)
        elif player == 'b':
            self.board_model.append_move(0, hole)

        if new_hand is None:
            new_hand = Hand(player=player, hole_pos=hole, counter_count=0)

        new_hand.current_state = Hand.PICKUP_STATE

        worker = Worker(self.sow, new_hand=new_hand)
        worker.signals.finished.connect(self.next_action)
        self.threadpool.start(worker)

    # starts a worker for each hand
    def start_worker_simultaneous_sowing(self, hole_a=None, hole_b=None, hand_a=None, hand_b=None, simul_prompt=False):

        self.autoplay_hands = True
        self.board_graphic.set_enable_play_button(False)

        prompt_agent_a = False
        prompt_agent_b = False

        if hand_a is None:
            prompt_agent_a = (hole_a is None or hole_a <= 0)
        else:
            prompt_agent_a = hand_a.current_state == Hand.PROMPTING_STATE

        if hand_b is None:
            prompt_agent_b = (hole_b is None or hole_b <= 0)
        else:
            prompt_agent_b = hand_b.current_state == Hand.PROMPTING_STATE

        if prompt_agent_a and not self.player_a_agent_name == self.AGENT_USER:
            hole_a = self.prompt_agent_for_input('a', simul_prompt)

        if prompt_agent_b and not self.player_b_agent_name == self.AGENT_USER:
            hole_b = self.prompt_agent_for_input('b', simul_prompt)

        self.board_model.append_move(hole_a, hole_b)

        if hand_a is None:
            hand_a = Hand(player='a', hole_pos=hole_a, counter_count=0)

        if hand_b is None:
            hand_b = Hand(player='b', hole_pos=hole_b, counter_count=0)

        hand_a.current_state = Hand.PICKUP_STATE
        hand_b.current_state = Hand.PICKUP_STATE

        worker_simul = Worker(self.simul_sow, hand_a=hand_a, hand_b=hand_b)
        worker_simul.signals.finished.connect(self.next_action)
        self.threadpool.start(worker_simul)

    # iterate sowing in board model
    def sow(self, new_hand):

        self.update_graphics_status(message="Sowing player " + new_hand.player.upper() + "...")

        self.board_graphic.set_enable_player_inputs(new_hand.player, False)
        self.update_sowing_speed(self.board_graphic.move_speed_slider.value())

        self.board_model.iterate_progress_player(hand=new_hand)

    # iterate simul sowing in board model
    def simul_sow(self, hand_a, hand_b):

        self.update_graphics_status(message="Sowing both players...")

        self.board_graphic.set_enable_player_inputs('a', False)
        self.board_graphic.set_enable_player_inputs('b', False)
        self.update_sowing_speed(self.board_graphic.move_speed_slider.value())

        self.board_model.iterate_progress_both_players(hand_a=hand_a, hand_b=hand_b)

    # performs the next action based on given or the board model
    def next_action(self, action=None):

        # update_board_graphics(board_graphic=self.board_graphic, board_model=self.board_model)

        # update_board_graphics(board_graphic=self.board_graphic, board_model=self.board_model)

        if action is None:
            action = self.board_model.get_next_action()

        match action:
            case BoardModel.PROMPT_SOWING_A:
                if self.current_mode == self.LOADING_MODE:
                    self.do_next_move_from_loaded_moves(action)
                else:
                    self.prompt_player('a', False)
            case BoardModel.PROMPT_SOWING_B:
                if self.current_mode == self.LOADING_MODE:
                    self.do_next_move_from_loaded_moves(action)
                else:
                    self.prompt_player('b', False)
            case BoardModel.PROMPT_SOWING_BOTH:
                if self.current_mode == self.LOADING_MODE:
                    self.do_next_move_from_loaded_moves(action)
                else:
                    if self.player_a_agent_name == self.AGENT_USER or self.player_b_agent_name == self.AGENT_USER:

                        if (not self.player_a_agent_name == self.AGENT_USER) ^ (
                                self.player_b_agent_name == self.AGENT_USER):
                            print("enable")
                            self.board_graphic.set_enable_play_button(True)
                            self.autoplay_hands = False
                        else:
                            print("disable")
                            self.board_graphic.set_enable_play_button(False)
                            self.autoplay_hands = True

                        if self.player_a_agent_name == self.AGENT_USER:
                            self.prompt_player('a', True)

                        if self.player_b_agent_name == self.AGENT_USER:
                            self.prompt_player('b', True)

                    else:
                        self.start_worker_simultaneous_sowing(simul_prompt=True)

            case BoardModel.GAME_END:
                print("Game over")
                self.end_game()
            case BoardModel.ERROR:
                print("game has errored. restarting game")

                if self.current_mode == self.MULTI_GAME_MODE or self.current_mode == self.ROUND_ROBIN_MODE:
                    self.new_game(True)
                else:
                    self.new_game(False)

    # ends the game or performs next task
    def end_game(self):

        if self.game_has_ended:
            return
        else:
            self.game_has_ended = True

        self.board_model.active_players.clear()

        update_board_graphics(board_graphic=self.board_graphic, board_model=self.board_model)

        result = self.DRAW
        winner = "None"

        if self.board_model.storeroom_a_value == self.board_model.storeroom_b_value:
            print("Draw")
            result = self.DRAW
            winner = "Draw"
        elif self.board_model.storeroom_a_value > self.board_model.storeroom_b_value:
            print("Player A wins")
            result = self.PLAYER_A_WIN
            winner = "a"
        elif self.board_model.storeroom_b_value > self.board_model.storeroom_a_value:
            print("Player B wins")
            result = self.PLAYER_B_WIN
            winner = "b"

        if self.is_training_state_agents:

            if self.player_a_agent_simul == self.rl_simul_agent or self.player_b_agent_simul == self.rl_simul_agent:
                self.rl_simul_agent.update_all_values(winner)
                self.rl_simul_agent.clear_used_states()

            if self.player_a_agent_simul == self.q_simul_agent or self.player_b_agent_simul == self.q_simul_agent:
                self.q_simul_agent.update_all_q_values(winner)
                self.q_simul_agent.clear_used_states()

        # TODO: refactor the hell out of this section
        #  (do it only if you have time and sanity (you have neither))

        match self.current_mode:
            case self.NORMAL_MODE:

                self.update_graphics_status(message="Game has ended")

                self.board_graphic.end_game_prompt(winner, self.board_model.storeroom_a_value,
                                                   self.board_model.storeroom_b_value)
                print("Game has ended. Moves made: ")

                try:
                    print("max a: average leaf count: " + str(mean(self.max_agent_a.all_leaves)))
                    print("max a: average depths: " + str(mean(self.max_agent_a.all_depths)))
                except:
                    pass

                try:
                    print("max b: average leaf count: " + str(mean(self.max_agent_b.all_leaves)))
                    print("max b: average depths: " + str(mean(self.max_agent_b.all_depths)))
                except:
                    pass

                try:
                    print("minimax a: average leaf count: " + str(mean(self.minimax_agent_a.all_leaves)))
                except:
                    pass

                try:
                    print("minimax b: average leaf count: " + str(mean(self.minimax_agent_b.all_leaves)))
                except:
                    pass

                for move in self.board_model.moves_made:
                    print(move)

            case self.MULTI_GAME_MODE:

                self.game_results.append(result)
                if self.no_of_games_left > 0:
                    print("Multi: " + str(self.no_of_games_left) + " games left...")
                    self.no_of_games_left -= 1
                    self.new_game(True)
                else:

                    self.update_graphics_status(message="Multi game has ended")

                    self.board_graphic.multi_end_game_prompt(self.game_results)

                    self.current_mode = self.NORMAL_MODE

                pass
            case self.ROUND_ROBIN_MODE:

                agent_a_index = self.tournament_participants.index(self.player_a_agent_name)
                agent_b_index = self.tournament_participants.index(self.player_b_agent_name)

                if result == self.PLAYER_A_WIN:
                    self.round_robin_results[agent_a_index][agent_b_index] += 1
                elif result == self.PLAYER_B_WIN:
                    self.round_robin_results[agent_b_index][agent_a_index] += 1

                if self.no_of_games_left > 0:
                    print("RR: " + str(self.no_of_games_left) + " games left...")
                    self.no_of_games_left -= 1
                    self.new_game(True)
                else:

                    agent_a_index = self.tournament_participants.index(self.player_a_agent_name)
                    agent_b_index = self.tournament_participants.index(self.player_b_agent_name)

                    agent_b_index += 1

                    if agent_b_index >= len(self.tournament_participants):
                        agent_a_index += 1
                        agent_b_index = agent_a_index

                    if agent_a_index >= len(self.tournament_participants):
                        self.update_graphics_status(message="Round Robin has ended")
                        self.board_graphic.tournament_end_prompt(self.tournament_participants,
                                                                 self.no_of_games_to_run, self.round_robin_results)
                        self.current_mode = self.NORMAL_MODE
                    else:
                        self.run_multiple_games(no_of_games=self.no_of_games_to_run,
                                                agent_a_name=self.tournament_participants[agent_a_index],
                                                agent_b_name=self.tournament_participants[agent_b_index],
                                                simul_agent_a=self.round_robin_simul_agent,
                                                simul_agent_b=self.round_robin_simul_agent)
                pass

            case self.EVAL_TRAINING_MODE:

                if result == self.PLAYER_A_WIN:
                    self.eval_func_trainer.population[self.TEF_individual_a_index].score += 1
                elif result == self.PLAYER_B_WIN:
                    self.eval_func_trainer.population[self.TEF_individual_b_index].score += 1

                if self.no_of_games_left > 0:
                    print("TEF: " + str(self.no_of_games_left) + " games left...")
                    self.no_of_games_left -= 1
                    self.new_game(True)
                else:

                    self.TEF_individual_b_index += 1

                    if self.TEF_individual_b_index >= len(self.TEF_population):
                        self.TEF_individual_a_index += 1
                        self.TEF_individual_b_index = self.TEF_individual_a_index + 1

                    if self.TEF_individual_a_index >= len(self.TEF_population) or \
                            self.TEF_individual_b_index >= len(self.TEF_population):

                        if self.eval_func_trainer.generation_count >= self.eval_func_trainer.max_generation_count or \
                                self.eval_func_trainer.check_if_converge():
                            # end training.

                            self.update_graphics_status(message="Round Robin has ended")

                            best_individual = self.eval_func_trainer.get_best_individual()
                            weight = best_individual.weight_chromosome

                            # TODO: make this part optional/togglable

                            # self.max_agent = MaxAgent(max_depth=self.max_depth,
                            #                           weights=weight)
                            # self.minimax_agent = MinimaxAgent(weights=weight,
                            #                                   maximum_depth=self.minmax_depth, maximum_self_depth=0,
                            #                                   maximum_number_node=0)

                            self.board_graphic.TEF_end_prompt(self.eval_func_trainer.generation_count, weight)
                            self.current_mode = self.NORMAL_MODE
                        else:
                            self.eval_func_trainer.generate_next_population()

                            self.TEF_population = self.eval_func_trainer.population

                            self.TEF_individual_a_index = 0
                            self.TEF_individual_b_index = 1

                            self.TEF_individual_a = MaxAgent(max_depth=self.max_depth,
                                                             weights=self.TEF_population[0].weight_chromosome)
                            self.TEF_individual_b = MaxAgent(max_depth=self.max_depth,
                                                             weights=self.TEF_population[1].weight_chromosome)

                            self.run_multiple_games(no_of_games=self.no_of_games_to_run,
                                                    agent_a=self.TEF_individual_a,
                                                    agent_b=self.TEF_individual_b)

                    else:

                        print("running round robin with agent no " + str(self.TEF_individual_a_index) +
                              " and agent no " + str(self.TEF_individual_b_index))

                        self.TEF_individual_a = MaxAgent(max_depth=self.max_depth,
                                                         weights=self.TEF_population[
                                                             self.TEF_individual_a_index].weight_chromosome)
                        self.TEF_individual_b = MaxAgent(max_depth=self.max_depth,
                                                         weights=self.TEF_population[
                                                             self.TEF_individual_b_index].weight_chromosome)

                        self.run_multiple_games(no_of_games=self.no_of_games_to_run,
                                                agent_a=self.TEF_individual_a,
                                                agent_b=self.TEF_individual_b,
                                                simul_agent_a=self.round_robin_simul_agent,
                                                simul_agent_b=self.round_robin_simul_agent)
                pass

            case self.BFPM_MODE:

                if result == self.PLAYER_A_WIN:
                    self.payoff_matrix[self.bfpm_player_a_choice-1][self.bfpm_player_b_choice-1] += 1
                elif result == self.PLAYER_B_WIN:
                    self.payoff_matrix[self.bfpm_player_a_choice-1][self.bfpm_player_b_choice-1] -= 1

                if self.no_of_games_left > 0:
                    print("BFPM: " + str(self.no_of_games_left) + " games left...")
                    self.no_of_games_left -= 1
                    self.new_game(True)
                else:

                    self.bfpm_player_b_choice += 1

                    if self.bfpm_player_b_choice > 7:
                        self.bfpm_player_a_choice += 1
                        self.bfpm_player_b_choice = 1

                    if self.bfpm_player_a_choice > 7:
                        self.update_graphics_status(message="BFPM has ended")

                        print(self.payoff_matrix)

                        self.current_mode = self.NORMAL_MODE
                    else:
                        print("BFPM: current a choice: " + str(self.bfpm_player_a_choice) + " current b choice" + str(
                            self.bfpm_player_b_choice))
                        self.run_multiple_games(no_of_games=self.no_of_games_to_run,
                                                agent_a_name=self.AGENT_MINIMAX,
                                                agent_b_name=self.AGENT_MINIMAX,
                                                simul_agent_a=self.random_agent,
                                                simul_agent_b=self.random_agent)
                pass


            case self.LOADING_MODE:
                print("Game has loaded.")
                self.current_mode = self.NORMAL_MODE
                pass

    # decides what action to take when the hole input is chosen
    def choosing_hole_action(self, player, hole):
        if self.autoplay_hands:
            if self.board_model.game_phase == BoardModel.SIMULTANEOUS_PHASE:
                if player == 'a':
                    self.start_worker_simultaneous_sowing(hole_a=hole, hand_b=self.board_model.player_b_hand,
                                                          simul_prompt=True)
                elif player == 'b':
                    self.start_worker_simultaneous_sowing(hole_b=hole, hand_a=self.board_model.player_a_hand,
                                                          simul_prompt=True)

            elif self.board_model.game_phase == BoardModel.SEQUENTIAL_PHASE:
                self.start_worker_sowing(player=player, hole=hole)
        else:
            self.set_hand_pos(player, hole)

    # sets the hand position
    def set_hand_pos(self, player, hole):
        if self.show_starting_hands:
            self.board_model.update_player_hand_pos(player, hole)
        if player == 'a':
            self.player_a_hand_pos = hole
        elif player == 'b':
            self.player_b_hand_pos = hole

    # prompts the corresponding player
    def prompt_player(self, player, simul):

        self.update_graphics_status(message="Prompting agent " + player + " for a move...")

        available_moves = self.board_model.available_moves(player)

        if player == 'a':
            if self.player_a_agent_name == self.AGENT_USER:
                self.board_graphic.set_enable_player_specific_inputs(player=player,
                                                                     enable_list=available_moves)
            else:
                self.choosing_hole_action(player=player, hole=self.prompt_agent_for_input(player, simul))

        elif player == 'b':
            if self.player_b_agent_name == self.AGENT_USER:
                self.board_graphic.set_enable_player_specific_inputs(player=player,
                                                                     enable_list=available_moves)
            else:
                self.choosing_hole_action(player=player, hole=self.prompt_agent_for_input(player, simul))

    # TODO: add a way to save future moves to save time
    # TODO: make this a worker so that it doesnt freeze the GUI
    # prompt agent for move. returns  move
    def prompt_agent_for_input(self, player, simul):

        self.update_graphics_status(message="Prompting agent " + player + " for a move...")

        move = -1
        while move not in self.board_model.available_moves(player):
            copied_board = copy.deepcopy(self.board_model)

            if simul:

                if player == 'a':

                    if self.current_mode == self.BFPM_MODE and self.board_model.house_a_values == [7,7,7,7,7,7,7]:
                        move = self.bfpm_player_a_choice
                    # if self.board_model.house_a_values == [7,7,7,7,7,7,7]:
                    #     move = 5
                    else:
                        # print("random")
                        move = self.player_a_agent_simul.choose_move(player, copied_board)

                elif player == 'b':

                    if self.current_mode == self.BFPM_MODE and self.board_model.house_b_values == [7,7,7,7,7,7,7]:
                        move = self.bfpm_player_b_choice
                    # if self.board_model.house_b_values == [7,7,7,7,7,7,7]:
                    #     move = 7
                    else:
                        # print("random")
                        move = self.player_b_agent_simul.choose_move(player, copied_board)
                        print("random choice: " + str(move))

            else:
                if player == 'a':
                    move = self.player_a_agent.choose_move(player, copied_board)

                elif player == 'b':
                    move = self.player_b_agent.choose_move(player, copied_board)

            if move not in self.board_model.available_moves(player):
                print("didnt find a valid move.")
                print("simul: " + str(simul) + " player: " + player +
                      " agent a: " + str(self.player_a_agent_name) +
                      " agent b: " + str(self.player_b_agent_name) +
                      " simul agent a: " + str(self.player_a_simul_agent_index) +
                      " simul agent b: " + str(self.player_b_simul_agent_index))
                print("move: " + str(move))
                copied_board.print_all_data()
                raise "no valid move"

        if player == 'a':
            move += 10
        elif player == 'b':
            move += 20

        return move

    # sets the player agent
    def set_player_agent_index(self, player, agent_index):

        self.set_hand_pos(player, 0)

        if player == 'a':
            self.player_a_agent_name = self.LIST_OF_AGENTS_NAME[agent_index]
            self.player_a_agent = self.list_of_art_agents_a[agent_index]
            self.board_graphic.player_a_agent_dropdown.setCurrentIndex(agent_index)

            if agent_index == 0 and not self.player_a_simul_agent_index == self.AGENT_USER:
                self.set_player_simul_agent_index(player, 0)
            elif not agent_index == 0 and self.player_a_simul_agent_index == self.AGENT_USER:
                self.set_player_simul_agent_index(player, 1)

        elif player == 'b':
            self.player_b_agent_name = self.LIST_OF_AGENTS_NAME[agent_index]
            self.player_b_agent = self.list_of_art_agents_b[agent_index]
            self.board_graphic.player_b_agent_dropdown.setCurrentIndex(agent_index)

            if agent_index == 0 and not self.player_b_simul_agent_index == self.AGENT_USER:
                self.set_player_simul_agent_index(player, 0)
            elif not agent_index == 0 and self.player_b_simul_agent_index == self.AGENT_USER:
                self.set_player_simul_agent_index(player, 1)

        if agent_index == 0:
            self.board_graphic.set_enable_player_inputs(player, True)
        else:
            self.board_graphic.set_enable_player_inputs(player, False)

    # sets the player simul agent
    def set_player_simul_agent_index(self, player, agent_index):

        self.set_hand_pos(player, 0)

        if player == 'a':
            self.player_a_simul_agent_index = self.LIST_OF_SIMUL_AGENTS_NAME[agent_index]
            self.board_graphic.player_a_simul_agent_dropdown.setCurrentIndex(agent_index)
            self.player_a_agent_simul = self.list_of_simul_art_agents[agent_index]

            if agent_index == 0 and not self.player_a_agent_name == self.AGENT_USER:
                self.set_player_agent_index(player, 0)
            elif not agent_index == 0 and self.player_a_agent_name == self.AGENT_USER:
                self.set_player_agent_index(player, 1)

        elif player == 'b':
            self.player_b_simul_agent_index = self.LIST_OF_SIMUL_AGENTS_NAME[agent_index]
            self.board_graphic.player_b_simul_agent_dropdown.setCurrentIndex(agent_index)
            self.player_b_agent_simul = self.list_of_simul_art_agents[agent_index]

            if agent_index == 0 and not self.player_b_agent_name == self.AGENT_USER:
                self.set_player_agent_index(player, 0)
            elif not agent_index == 0 and self.player_b_agent_name == self.AGENT_USER:
                self.set_player_agent_index(player, 1)

    def set_max_and_minimax_agent_weights(self, player, is_max, is_minimax, weights):

        print("updating...." + str(weights))

        if weights is None:
            weights = self.board_graphic.eval_func_training_end_dialog_box.final_weight

        if is_max:
            if player == 'a':
                self.max_agent_a = MaxAgent(max_depth=self.max_depth, weights=weights)
                self.list_of_art_agents_a[2] = self.max_agent_a
            elif player == 'b':
                self.max_agent_b = MaxAgent(max_depth=self.max_depth, weights=weights)
                self.list_of_art_agents_b[2] = self.max_agent_b

        if is_minimax:
            if player == 'a':
                self.minimax_agent_a = MinimaxAgent(weights=weights, maximum_depth=self.minmax_depth,
                                                    maximum_self_depth=0,
                                                    maximum_number_node=0)
                self.list_of_art_agents_a[3] = self.minimax_agent_a
            elif player == 'b':
                self.minimax_agent_b = MinimaxAgent(weights=weights, maximum_depth=self.minmax_depth,
                                                    maximum_self_depth=0,
                                                    maximum_number_node=0)
                self.list_of_art_agents_b[3] = self.minimax_agent_b

    # updates board graphics constantly
    def update_board_graphics_constantly(self):
        pass
        while self.board_graphic.active:
            time.sleep(self.graphic_refresh_rate)
            if self.update_graphic:
                update_board_graphics(board_graphic=self.board_graphic, board_model=self.board_model)
        self.close_program()

    # updates the sowing speed
    def update_sowing_speed(self, move_per_second):

        if move_per_second > 10:
            self.board_model.sowing_speed = 0
        else:
            self.board_model.sowing_speed = 1 / move_per_second

    # runs multiple games
    def run_multiple_games(self, no_of_games=None, agent_a_name=None, agent_b_name=None,
                           agent_a=None, agent_b=None,
                           simul_agent_a_name=None, simul_agent_b_name=None,
                           simul_agent_a=None, simul_agent_b=None):

        if no_of_games is None:
            no_of_games = self.board_graphic.multiple_games_dialog_box.number_of_games

        if agent_a_name is None and agent_a is None:
            self.set_player_agent_index('a', self.board_graphic.multiple_games_dialog_box.player_a_agent)
        elif agent_a_name is not None and agent_a is None:
            self.player_a_agent_name = agent_a_name
            self.set_player_agent_index('a', self.LIST_OF_AGENTS_NAME.index(agent_a_name))
        elif agent_a_name is None and agent_a is not None:
            self.player_a_agent = agent_a

        if agent_b_name is None and agent_b is None:
            self.set_player_agent_index('b', self.board_graphic.multiple_games_dialog_box.player_b_agent)
        elif agent_b_name is not None and agent_b is None:
            self.player_b_agent_name = agent_b_name
            self.set_player_agent_index('b', self.LIST_OF_AGENTS_NAME.index(agent_b_name))
        elif agent_b_name is None and agent_b is not None:
            self.player_b_agent = agent_b

        if simul_agent_a_name is None and simul_agent_a is None:
            self.set_player_simul_agent_index('a', self.board_graphic.multiple_games_dialog_box.player_a_simul_agent)
        elif simul_agent_a_name is not None and simul_agent_a is None:
            self.player_a_agent_name = simul_agent_a_name
            self.set_player_simul_agent_index('a', self.LIST_OF_SIMUL_AGENTS_NAME.index(simul_agent_a_name))
        elif simul_agent_a_name is None and simul_agent_a is not None:
            self.player_a_agent_simul = simul_agent_a

        if simul_agent_b_name is None and simul_agent_b is None:
            self.set_player_simul_agent_index('b', self.board_graphic.multiple_games_dialog_box.player_b_simul_agent)
        elif simul_agent_b_name is not None and simul_agent_b is None:
            self.player_b_agent_name = simul_agent_b_name
            self.set_player_simul_agent_index('b', self.LIST_OF_SIMUL_AGENTS_NAME.index(simul_agent_b_name))
        elif simul_agent_b_name is None and simul_agent_b is not None:
            self.player_b_agent_simul = simul_agent_b

        if agent_a_name == self.AGENT_USER or agent_b_name == self.AGENT_USER:
            print("choose two artificial gents")
            return

        if self.current_mode == self.MULTI_GAME_MODE or self.current_mode == self.ROUND_ROBIN_MODE:
            print("running " + str(no_of_games) + " games. player a: " + str(
                self.player_a_agent_name) + ". player b: " + str(self.player_b_agent_name))
        elif self.current_mode == self.EVAL_TRAINING_MODE:
            print("running " + str(no_of_games) + " games. player a: " + str(
                self.player_a_agent.heuristics_weights) +
                  ". player b: " + str(self.player_b_agent.heuristics_weights))
        elif self.current_mode == self.BFPM_MODE:
            print("BFPM: current a choice: " + str(self.bfpm_player_a_choice) + " current b choice: " + str(
                self.bfpm_player_b_choice))


        if self.current_mode not in [self.ROUND_ROBIN_MODE, self.EVAL_TRAINING_MODE, self.BFPM_MODE]:
            self.current_mode = self.MULTI_GAME_MODE

        # if not self.current_mode == self.ROUND_ROBIN_MODE and not self.current_mode == self.EVAL_TRAINING_MODE and not self.BFPM_MODE:
        #     self.current_mode = self.MULTI_GAME_MODE

        self.new_game(False)

        self.no_of_games_to_run = no_of_games
        self.no_of_games_left = no_of_games - 1
        self.game_results = []

        self.next_action(BoardModel.PROMPT_SOWING_BOTH)

        pass

    # runs a round robin tournament
    def run_round_robin_tournament(self):

        no_of_games = self.board_graphic.tournament_dialog_box.number_of_games
        participants = self.board_graphic.tournament_dialog_box.tournament_participants

        self.round_robin_simul_agent = self.list_of_simul_art_agents[
            self.board_graphic.tournament_dialog_box.player_simul_agent]

        participants.sort()

        self.tournament_participants = []

        for index in participants:
            self.tournament_participants.append(self.LIST_OF_AGENTS_NAME[index])

        self.current_mode = self.ROUND_ROBIN_MODE

        self.player_a_agent_name = self.tournament_participants[0]
        self.player_b_agent_name = self.tournament_participants[0]

        self.no_of_games_to_run = no_of_games

        self.round_robin_results = [[0 for x in range(len(self.tournament_participants))]
                                    for x in range(len(self.tournament_participants))]

        self.run_multiple_games(no_of_games=self.no_of_games_to_run, agent_a_name=self.player_a_agent_name,
                                agent_b_name=self.player_b_agent_name,
                                simul_agent_a=self.round_robin_simul_agent, simul_agent_b=self.round_robin_simul_agent)

        pass

    # start training the evaluation function
    def start_training_eval_function(self, max_no_generations=None, no_of_games=None, pop_size=None):

        if max_no_generations is None:
            max_no_generations = self.board_graphic.eval_func_training_dialog_box.max_generation_count

        if no_of_games is None:
            no_of_games = self.board_graphic.eval_func_training_dialog_box.no_of_games

        if pop_size is None:
            pop_size = self.board_graphic.eval_func_training_dialog_box.pop_size

        self.current_mode = self.EVAL_TRAINING_MODE

        self.eval_func_trainer = EvalFuncTrainer(max_generation_count=max_no_generations,
                                                 pop_size=pop_size,
                                                 size_of_chromosome=self.trainer_chromosome_size,
                                                 initial_std_dev=self.trainer_std_dev)

        self.TEF_population = self.eval_func_trainer.population

        self.no_of_games_to_run = no_of_games

        self.TEF_individual_a_index = 0
        self.TEF_individual_b_index = 1

        self.TEF_individual_a = MaxAgent(max_depth=self.max_depth, weights=self.TEF_population[0].weight_chromosome)
        self.TEF_individual_b = MaxAgent(max_depth=self.max_depth, weights=self.TEF_population[1].weight_chromosome)

        self.round_robin_simul_agent = self.random_agent

        self.set_player_simul_agent_index('a', 1)
        self.set_player_simul_agent_index('b', 1)

        self.run_multiple_games(no_of_games=self.no_of_games_to_run,
                                agent_a=self.TEF_individual_a,
                                agent_b=self.TEF_individual_b,
                                simul_agent_a=self.round_robin_simul_agent,
                                simul_agent_b=self.round_robin_simul_agent)

    def brute_force_payoff_matrix(self, no_of_games=10):

        no_of_games = 1

        print(self.payoff_matrix)

        self.bfpm_player_a_choice = 1
        self.bfpm_player_b_choice = 1

        self.current_mode = self.BFPM_MODE

        print("BFPM: current a choice: " + str(self.bfpm_player_a_choice) + " current b choice: " + str(self.bfpm_player_b_choice))

        self.no_of_games_to_run = no_of_games

        self.run_multiple_games(no_of_games=self.no_of_games_to_run,
                                agent_a_name=self.AGENT_MINIMAX,
                                agent_b_name=self.AGENT_MINIMAX,
                                simul_agent_a=self.player_a_agent_simul,
                                simul_agent_b=self.player_a_agent_simul)

    # Restarts a new game
    def new_game(self, autorun):

        self.game_has_ended = False

        self.kill_all_workers()

        self.board_model.reset_game()
        self.move_counter = 0
        self.autoplay_hands = autorun
        self.player_a_hand_pos = 0
        self.player_b_hand_pos = 0

        self.board_graphic.set_enable_play_button(not autorun)

        if autorun:
            self.next_action(BoardModel.PROMPT_SOWING_BOTH)
        else:
            if self.player_a_agent_name == self.AGENT_USER:
                available_moves = self.board_model.available_moves('a')
                if self.player_a_agent_name == self.AGENT_USER:
                    self.board_graphic.set_enable_player_specific_inputs(player='a',
                                                                         enable_list=available_moves)

            if self.player_b_agent_name == self.AGENT_USER:
                available_moves = self.board_model.available_moves('b')
                if self.player_b_agent_name == self.AGENT_USER:
                    self.board_graphic.set_enable_player_specific_inputs(player='b',
                                                                         enable_list=available_moves)

    # stops all workers
    def kill_all_workers(self):
        self.board_model.running = False
        self.threadpool.clear()

        time.sleep(0.00001)

        self.board_model.running = True

    # save moves BROKEN
    def save_moves(self):
        file = open("moves.txt", 'w')

        for move in self.board_model.moves_made:
            file.write(str(move) + '\n')

        file.write("END")
        file.close()

    # load moves BROKEN
    def load_moves(self):

        self.board_model.reset_game()
        self.current_mode = self.LOADING_MODE

        self.loaded_moves.clear()

        file = open("moves.txt", 'r')
        for line in file:
            if not (line == 'END'):
                self.loaded_moves.append(eval(line))
            else:
                break
        file.close()

        print(self.loaded_moves)

        self.move_counter = 0
        self.do_next_move_from_loaded_moves(BoardModel.PROMPT_SOWING_BOTH)

    # plays the next move loaded BROKEN??
    def do_next_move_from_loaded_moves(self, action):

        if self.move_counter < len(self.loaded_moves):
            current_move = self.loaded_moves[self.move_counter]

            if self.board_model.game_phase == BoardModel.SEQUENTIAL_PHASE:
                if BoardModel.PROMPT_SOWING_A and not current_move[0] == 0 and current_move[1] == 0:
                    self.start_worker_sowing('a', current_move[0])
                elif BoardModel.PROMPT_SOWING_B and not current_move[1] == 0 and current_move[0] == 0:
                    self.start_worker_sowing('b', current_move[1])
                elif BoardModel.PROMPT_SOWING_BOTH and not current_move[0] == 0 and not current_move[1] == 0:
                    self.start_worker_simultaneous_sowing(current_move[0], current_move[1], simul_prompt=True)
                else:
                    print("error with seq loading move. action: " + str(action) + " Move: " + str(current_move))

            elif self.board_model.game_phase == BoardModel.SIMULTANEOUS_PHASE:
                if BoardModel.PROMPT_SOWING_A and not current_move[0] == 0 and current_move[1] == 0:
                    self.start_worker_simultaneous_sowing(hole_a=current_move[0], hand_b=self.board_model.player_b_hand)
                elif BoardModel.PROMPT_SOWING_B and not current_move[1] == 0 and current_move[0] == 0:
                    self.start_worker_simultaneous_sowing(hole_b=current_move[1], hand_a=self.board_model.player_a_hand)
                elif BoardModel.PROMPT_SOWING_BOTH and not current_move[0] == 0 and not current_move[1] == 0:
                    self.start_worker_simultaneous_sowing(hole_a=current_move[0], hole_b=current_move[1],
                                                          simul_prompt=True)
                else:
                    print("error with simul loading move. action: " + str(action) + " Move: " + str(current_move))

        self.move_counter += 1
        if self.move_counter >= len(self.loaded_moves):
            print("Game Loaded")
            self.current_mode = self.NORMAL_MODE

    def print_rl_states(self):
        self.rl_simul_agent.print_all_states()
        self.board_graphic.message_box.setText(self.rl_simul_agent.state_to_string())
        self.board_graphic.message_box.setWindowTitle("RL states")
        self.board_graphic.message_box.exec()

    def print_q_states(self):
        self.q_simul_agent.print_all_states()
        self.board_graphic.message_box.setText(self.q_simul_agent.state_to_string())
        self.board_graphic.message_box.setWindowTitle("Q states")
        self.board_graphic.message_box.exec()

    # toggles whether the graphics should update
    def toggle_update_graphics(self, state):
        self.update_graphic = state

    # toggles whether the simul state agents should learn
    def toggle_learning_state_agents(self, state):
        self.is_training_state_agents = state

    def edit_marble_count(self):

        house_a_value = self.board_graphic.counter_edit_dialog_box.player_a_houses
        house_b_value = self.board_graphic.counter_edit_dialog_box.player_b_houses

        storeroom_a_value = self.board_graphic.counter_edit_dialog_box.player_a_storeroom
        storeroom_b_value = self.board_graphic.counter_edit_dialog_box.player_b_storeroom

        self.board_model.house_a_values = house_a_value
        self.board_model.house_b_values = house_b_value
        self.board_model.storeroom_a_value = storeroom_a_value
        self.board_model.storeroom_b_value = storeroom_b_value

    def update_graphics_status(self, message="", random=""):
        self.board_graphic.update_status_bar_message(message, self.current_mode, self.no_of_games_left+1, random)

    # closes the program
    def close_program(self):
        self.kill_all_workers()
        sys.exit("Window closed")
