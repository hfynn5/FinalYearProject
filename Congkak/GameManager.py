import sys, traceback
import time

from Congkak.CongkakBoardGraphics import BoardGraphic
from Congkak.CongkakBoardModel import BoardModel, Hand
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QRunnable, QThreadPool
from Congkak.Hand import Hand
from PyQt6.QtGui import QPixmap


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
    board_graphic.update_labels(house_a_values=board_model.house_a_values,
                                house_b_values=board_model.house_b_values,
                                storeroom_a_value=board_model.storeroom_a_value,
                                storeroom_b_value=board_model.storeroom_b_value,
                                player_a_hand=board_model.player_a_hand,
                                player_b_hand=board_model.player_b_hand)


class GameManager:

    def __init__(self):

        self.player_a_hand_pos = 0
        self.player_b_hand_pos = 0

        self.autoplay_hands = False

        # declare threadpool
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        # declare board model
        self.board_model = BoardModel()

        # declare graphics
        App = QApplication(sys.argv)
        self.board_graphic = BoardGraphic()

        # connect input with corresponding functions
        for i, button in enumerate(self.board_graphic.house_a_buttons):
            button.clicked.connect(lambda checked, value=i + 11: self.hole_button_action('a', value))

        for i, button in enumerate(self.board_graphic.house_b_buttons):
            button.clicked.connect(lambda checked, value=i + 21: self.hole_button_action('b', value))

        self.board_graphic.play_button.clicked.connect(lambda checked:
                                                       self.start_worker_simultaneous_sowing(self.player_a_hand_pos,
                                                                                             self.player_b_hand_pos))

        self.board_graphic.move_speed_slider. \
            valueChanged.connect(lambda value=self.board_graphic.move_speed_slider.value():
                                 self.update_sowing_speed(value))

        self.board_graphic.save_game_button_action.triggered.connect(lambda checked: self.save_moves())

        self.board_graphic.menuBar()

        # start constantly updating graphics
        self.start_worker_graphic_updater()

        sys.exit(App.exec())

    # makes worker constantly update graphics
    def start_worker_graphic_updater(self):
        worker = Worker(self.update_board_graphics_constantly)
        self.threadpool.start(worker)

    # makes worker to start sowing
    def start_worker_sowing(self, player, hole):

        if player == 'a':
            self.board_model.append_move(hole, 0)
        elif player == 'b':
            self.board_model.append_move(0, hole)

        worker = Worker(self.sow, player=player, hole=hole)
        self.threadpool.start(worker)

    # TODO: disable play button if sequential mode or choices are not made.

    # starts a worker for each hand
    def start_worker_simultaneous_sowing(self, hole_a, hole_b):
        self.autoplay_hands = True

        self.board_model.append_move(hole_a, hole_b)

        worker_a = Worker(self.sow, player='a', hole=hole_a)
        self.threadpool.start(worker_a)

        worker_b = Worker(self.sow, player='b', hole=hole_b)
        self.threadpool.start(worker_b)

    # iterate sowing in board model
    def sow(self, player, hole):
        false_list = [False,False,False,False,False,False,False]
        self.board_graphic.set_enable_player_inputs(player, enable_list=false_list)
        self.update_sowing_speed(self.board_graphic.move_speed_slider.value())

        new_hand = Hand(player=player, hole_pos=hole, counter_count=0)

        self.board_model.iterate_sowing(new_hand)

        action = self.board_model.action_to_take()

        # print("player: " + player + " action: " + str(action))
        # print("player a: " + str(self.board_model.player_a_status))
        # print("player b: " + str(self.board_model.player_b_status))

        if action == BoardModel.PROMPT_SOWING_A and not self.board_model.player_a_status == BoardModel.CONTINUE_SOWING:
            self.prompt_player('a')
            self.board_model.player_b_sowing_slowed = True
        elif action == BoardModel.PROMPT_SOWING_B and not self.board_model.player_b_status == BoardModel.CONTINUE_SOWING:
            self.prompt_player('b')
            self.board_model.player_a_sowing_slowed = True
        elif action == BoardModel.PROMPT_SOWING_BOTH:
            self.autoplay_hands = False
            self.prompt_player('a')
            self.prompt_player('b')
        elif action == BoardModel.GAME_END:
            print("Game over")
            self.end_game()

    # ends the game
    def end_game(self):
        if self.board_model.storeroom_a_value == self.board_model.storeroom_b_value:
            print("Draw")
        elif self.board_model.storeroom_a_value > self.board_model.storeroom_b_value:
            print("Player A wins")
        elif self.board_model.storeroom_b_value > self.board_model.storeroom_a_value:
            print("Player B wins")

        print("moves made: ")

        for move in self.board_model.moves_made:
            print(move)

    # decides what action the hole button should take
    def hole_button_action(self, player, hole):
        if self.autoplay_hands:
            self.start_worker_sowing(player, hole)
        else:
            self.set_hand_pos(player, hole)

    # sets the hand position
    def set_hand_pos(self, player, hole):
        self.board_model.update_player_hand_pos(player, hole)
        if player == 'a':
            self.player_a_hand_pos = hole
        elif player == 'b':
            self.player_b_hand_pos = hole

    # prompts the corresponding player
    def prompt_player(self, player):

        self.board_graphic.set_enable_player_inputs(player=player,
                                                    enable_list=self.board_model.does_hole_have_counter(player))

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

    def save_moves(self):
        file = open("moves.txt",'w')
        move_string = str(self.board_model.moves_made)
        file.write(move_string)
        file.close()
