import sys, traceback
import time

from Congkak.CongkakBoardGraphics import BoardGraphic
from Congkak.CongkakBoardModel import BoardModel, Hand
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QRunnable, QThreadPool
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

class GameManager:

    def __init__(self):

        self.threadpool = QThreadPool()

        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.board_model = BoardModel()

        App = QApplication(sys.argv)
        self.board_graphic = BoardGraphic()

        for i, button in enumerate(self.board_graphic.house_a_buttons):
            button.clicked.connect(lambda checked, value = i+1: self.start_worker_sowing('a', value))

        for i, button in enumerate(self.board_graphic.house_b_buttons):
            button.clicked.connect(lambda checked, value = i+1: self.start_worker_sowing('b', value))

        self.update_board_graphics(board_graphic=self.board_graphic, board_model=self.board_model)

        self.start_worker_updating()

        sys.exit(App.exec())

    def start_worker_sowing(self, player, hole):
        # print(hole)
        worker = Worker(self.sow, player=player, hole=hole)

        self.threadpool.start(worker)

    def start_worker_updating(self):
        worker = Worker(self.constant_update_board_graphics, True)

        self.threadpool.start(worker)

    def sow(self,player,hole):
        self.board_graphic.set_enable_inputs(False)
        self.board_model.iterate_sowing(player=player, hole=hole, sowing_speed=0.5)
        self.board_graphic.set_enable_inputs(True)

    def constant_update_board_graphics(self):
        while True:
            self.update_board_graphics(board_graphic=self.board_graphic, board_model=self.board_model)

    def update_board_graphics(self, board_graphic: BoardGraphic, board_model: BoardModel):

        board_graphic.update_values(house_a_values=board_model.house_a_values, house_b_values=board_model.house_b_values,
                                             storeroom_a_value=board_model.storeroom_a_value,
                                             storeroom_b_value=board_model.storeroom_b_value)

