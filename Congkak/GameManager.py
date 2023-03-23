import copy
import sys, traceback
import time

from Congkak.CongkakBoardGraphics import BoardGraphic
from Congkak.CongkakBoardModel import BoardModel
from Congkak.Hand import Hand
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QRunnable, QThreadPool

from PyQt6.QtGui import QPixmap

from Congkak.IntelligentAgents.MinimaxAgent import MinimaxAgent
from Congkak.IntelligentAgents.RandomAgent import RandomAgent
from Congkak.IntelligentAgents.MaxAgent import MaxAgent


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
    board_graphic.update_values(house_a_values=board_model.house_a_values,
                                house_b_values=board_model.house_b_values,
                                storeroom_a_value=board_model.storeroom_a_value,
                                storeroom_b_value=board_model.storeroom_b_value,
                                player_a_hand=board_model.player_a_hand,
                                player_b_hand=board_model.player_b_hand)


class GameManager:

    def __init__(self):

        self.player_a_hand_pos = -1
        self.player_b_hand_pos = -1

        # user, random, max, minimax, mcts
        self.agent_list = ['user', 'random', 'max', 'minimax', 'mcts']
        self.player_a_agent = "user"
        self.player_b_agent = "user"

        # create Intelligent Agents
        self.random_agent = RandomAgent()
        self.max_agent = MaxAgent()
        self.minimax_agent = MinimaxAgent(weights=(0, 0, 0, 0, 0, 0), maximum_depth=2, maximum_self_depth=3, maximum_number_node=0)

        self.autoplay_hands = False

        self.loading_game = False
        self.loaded_moves = []
        self.move_counter = 0

        self.show_starting_hands = True

        # declare threadpool
        self.threadpool = QThreadPool()
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

        sys.exit(app.exec())

    def connect_inputs_to_functions(self):
        # connect input with corresponding functions
        for i, button in enumerate(self.board_graphic.house_a_buttons):
            button.clicked.connect(lambda checked, value=i + 11: self.choosing_hole_action('a', value))

        for i, button in enumerate(self.board_graphic.house_b_buttons):
            button.clicked.connect(lambda checked, value=i + 21: self.choosing_hole_action('b', value))

        self.board_graphic.play_button.clicked.connect(lambda checked:
                                                       self.start_worker_simultaneous_sowing(hole_a=self.player_a_hand_pos,
                                                                                             hole_b=self.player_b_hand_pos,
                                                                                            ))

        self.board_graphic.move_speed_slider. \
            valueChanged.connect(lambda value=self.board_graphic.move_speed_slider.value():
                                 self.update_sowing_speed(value))

        self.board_graphic.save_game_button_action.triggered.connect(lambda checked: self.save_moves())
        self.board_graphic.load_game_button_action.triggered.connect(lambda checked: self.load_moves())
        self.board_graphic.new_game_button_action.triggered.connect(lambda checked: self.new_game())

        self.board_graphic.player_a_dropdown. \
            activated.connect(lambda
                                  index=self.board_graphic.player_a_dropdown.
                                      currentIndex(): self.set_player_agent('a', index))

        self.board_graphic.player_b_dropdown. \
            activated.connect(lambda
                                  index=self.board_graphic.player_b_dropdown.
                                      currentIndex(): self.set_player_agent('b', index))

    # makes worker constantly update graphics
    def start_worker_graphic_updater(self):
        worker = Worker(self.update_board_graphics_constantly)
        self.threadpool.start(worker)

    # makes worker to start sowing
    def start_worker_sowing(self, player = None, hole = None, new_hand = None):

        if player == 'a':
            self.board_model.append_move(hole, 0)
        elif player == 'b':
            self.board_model.append_move(0, hole)

        if new_hand is None:
            new_hand = Hand(player=player, hole_pos=hole, counter_count=0)

        worker = Worker(self.sow, new_hand=new_hand)
        worker.signals.finished.connect(self.next_action)
        self.threadpool.start(worker)

    # starts a worker for each hand
    def start_worker_simultaneous_sowing(self, hole_a = None, hole_b = None, hand_a = None, hand_b = None):
        self.autoplay_hands = True
        self.board_graphic.set_enable_play_button(False)

        # print("hand a pos: " + str(hand_a.hole_pos))
        # print("hand b pos: " + str(hand_b.hole_pos))

        if not self.player_a_agent == 'user' and (hole_a is None or hole_a <= 0) and hand_a is None:
            # print()
            hole_a = self.prompt_agent_for_input('a')

        if not self.player_b_agent == 'user' and (hole_b is None or hole_b <= 0) and hand_b is None:
            hole_b = self.prompt_agent_for_input('b')

        if hand_a is None:
            hand_a = Hand(player='a', hole_pos=hole_a, counter_count=0)
        if hand_b is None:
            hand_b = Hand(player='b', hole_pos=hole_b, counter_count=0)

        worker_simul = Worker(self.simul_sow, hand_a=hand_a, hand_b=hand_b)
        worker_simul.signals.finished.connect(self.next_action)
        self.threadpool.start(worker_simul)

    def start_worker_tikam(self, hand):
        worker_tikam = Worker(self.tikam, hand=hand)
        worker_tikam.signals.finished.connect(self.next_action)
        self.threadpool.start(worker_tikam)

    # iterate sowing in board model
    def sow(self, new_hand):
        self.board_graphic.set_enable_player_inputs(new_hand.player, False)
        self.update_sowing_speed(self.board_graphic.move_speed_slider.value())

        self.board_model.iterate_sowing(new_hand)

    def simul_sow(self, hand_a, hand_b):
        self.board_graphic.set_enable_player_inputs('a', False)
        self.board_graphic.set_enable_player_inputs('b', False)
        self.update_sowing_speed(self.board_graphic.move_speed_slider.value())

        self.board_model.iterated_sowing_simultaneous(hand_a, hand_b)

    def tikam(self, hand):
        self.update_sowing_speed(self.board_graphic.move_speed_slider.value())

        self.board_model.tikam(hand=hand)

    def next_action(self):

        update_board_graphics(board_graphic=self.board_graphic, board_model=self.board_model)

        # print("next action")

        action = self.board_model.action_to_take()

        # print("action: " + str(action))
        # print("player a: " + str(self.board_model.player_a_status))
        # print("player b: " + str(self.board_model.player_b_status))

        if self.board_model.player_a_status == BoardModel.TIKAM_A:
            self.start_worker_tikam(hand=self.board_model.player_a_hand)
        if self.board_model.player_b_status == BoardModel.TIKAM_B:
            self.start_worker_tikam(hand=self.board_model.player_b_hand)

        match action:
            case BoardModel.PROMPT_SOWING_A:
                if self.loading_game:
                    self.do_next_move_from_loaded_moves(action)
                else:
                    self.prompt_player('a')
            case BoardModel.PROMPT_SOWING_B:
                if self.loading_game:
                    self.do_next_move_from_loaded_moves(action)
                else:
                    self.prompt_player('b')
            case BoardModel.PROMPT_SOWING_BOTH:
                if self.loading_game:
                    self.do_next_move_from_loaded_moves(action)
                else:
                    self.autoplay_hands = False
                    self.prompt_player('b')
                    self.prompt_player('a')
                    self.board_graphic.set_enable_play_button(True)

            case BoardModel.CONTINUE_SOWING_A:
                self.start_worker_sowing(new_hand=self.board_model.player_a_hand)
                pass
            case BoardModel.CONTINUE_SOWING_B:
                self.start_worker_sowing(new_hand=self.board_model.player_b_hand)
                pass
            case BoardModel.GAME_END:
                print("Game over")
                self.end_game()

    # ends the game
    def end_game(self):

        self.board_graphic.end_game_prompt()

        if self.board_model.storeroom_a_value == self.board_model.storeroom_b_value:
            print("Draw")
        elif self.board_model.storeroom_a_value > self.board_model.storeroom_b_value:
            print("Player A wins")
        elif self.board_model.storeroom_b_value > self.board_model.storeroom_a_value:
            print("Player B wins")

        print("moves made: ")

        for move in self.board_model.moves_made:
            print(move)

    # decides what action to take when the hole input is chosen
    def choosing_hole_action(self, player, hole):
        if self.autoplay_hands:
            if self.board_model.game_phase == BoardModel.SIMULTANEOUS_PHASE:
                # print("simul")
                if player == 'a':
                    self.start_worker_simultaneous_sowing(hole_a=hole, hand_b=self.board_model.player_b_hand)
                elif player == 'b':
                    self.start_worker_simultaneous_sowing(hole_b=hole, hand_a=self.board_model.player_a_hand)

            elif self.board_model.game_phase == BoardModel.SEQUENTIAL_PHASE:
                # print("seq")
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
    def prompt_player(self, player):

        available_moves = self.board_model.available_moves(player)

        if player == 'a':
            if self.player_a_agent == 'user':
                self.board_graphic.set_enable_player_specific_inputs(player=player,
                                                                     enable_list=available_moves)
            else:
                self.choosing_hole_action(player=player, hole=self.prompt_agent_for_input(player))

        elif player == 'b':
            if self.player_b_agent == 'user':
                self.board_graphic.set_enable_player_specific_inputs(player=player,
                                                                     enable_list=available_moves)
            else:
                self.choosing_hole_action(player=player, hole=self.prompt_agent_for_input(player))

    # TODO: add a way to save future moves to save time
    def prompt_agent_for_input(self, player):
        copied_board = copy.deepcopy(self.board_model)
        move = 0
        if player == 'a':
            if self.player_a_agent == 'random':
                move = self.random_agent.choose_move(player, copied_board) + 10
            elif self.player_a_agent == 'max':
                move = self.max_agent.choose_move(player, copied_board) + 10
            elif self.player_a_agent == 'minimax':
                move = self.minimax_agent.choose_move(player, copied_board) + 10
        elif player == 'b':
            if self.player_b_agent == 'random':
                move = self.random_agent.choose_move(player, copied_board) + 20
            elif self.player_b_agent == 'max':
                move = self.max_agent.choose_move(player, copied_board) + 20
            elif self.player_b_agent == 'minimax':
                move = self.minimax_agent.choose_move(player, copied_board) + 20

        return move

    def set_player_agent(self, player, agent_index):

        self.set_hand_pos(player, 0)

        if player == 'a':
            self.player_a_agent = self.agent_list[agent_index]
            print(self.player_a_agent)
        elif player == 'b':
            self.player_b_agent = self.agent_list[agent_index]
            print(self.player_b_agent)

        if agent_index == 0:
            self.board_graphic.set_enable_player_inputs(player, True)
        else:
            self.board_graphic.set_enable_player_inputs(player, False)

    # updates board graphics constantly
    def update_board_graphics_constantly(self):
        while self.board_graphic.active:
            update_board_graphics(board_graphic=self.board_graphic, board_model=self.board_model)
        sys.exit("Window closed")

    # updates the sowing speed
    def update_sowing_speed(self, move_per_second):

        if move_per_second > 10:
            self.board_model.sowing_speed = 0
        else:
            self.board_model.sowing_speed = 1 / move_per_second

    def new_game(self):
        self.board_model.reset_game()
        self.move_counter = 0
        self.autoplay_hands = False
        self.player_a_hand_pos = 0
        self.player_b_hand_pos = 0
        self.threadpool.clear()
        self.board_graphic.set_enable_play_button(True)
        self.prompt_player('a')
        self.prompt_player('b')

    def save_moves(self):
        file = open("moves.txt", 'w')

        for move in self.board_model.moves_made:
            file.write(str(move) + '\n')

        file.write("END")
        file.close()

    def load_moves(self):

        self.board_model.reset_game()
        self.loading_game = True

        file = open("moves.txt", 'r')
        for line in file:
            if not (line == 'END'):
                self.loaded_moves.append(eval(line))
            else:
                break
        file.close()

        self.move_counter = 0
        self.do_next_move_from_loaded_moves(BoardModel.PROMPT_SOWING_BOTH)

    def do_next_move_from_loaded_moves(self, action):

        if self.move_counter < len(self.loaded_moves):
            current_move = self.loaded_moves[self.move_counter]
            if BoardModel.PROMPT_SOWING_A and not current_move[0] == 0 and current_move[1] == 0:
                self.start_worker_sowing('a', current_move[0])
            elif BoardModel.PROMPT_SOWING_B and not current_move[1] == 0 and current_move[0] == 0:
                self.start_worker_sowing('b', current_move[1])
            elif BoardModel.PROMPT_SOWING_BOTH and not current_move[0] == 0 and not current_move[1] == 0:
                self.start_worker_simultaneous_sowing(current_move[0], current_move[1])
            else:
                print("error with loading move. action: " + str(action) + " Move: " + str(current_move))

        self.move_counter += 1
        if self.move_counter >= len(self.loaded_moves):
            print("Game Loaded")
            self.loading_game = False



