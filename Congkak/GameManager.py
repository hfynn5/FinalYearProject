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
        # self.args = args
        # self.kwargs = kwargs

        self.signals = WorkerSignals()

    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        # Retrieve args/kwargs here; and fire processing using them

        try:
            for x in range(5):

                start_time = time.time()

                while time.time() - start_time < 1:
                    pass
                print("ping")
                result = self.fn()


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

        self.curr_value = 7

        self.update_board(board_graphic=self.board_graphic, board_model=self.board_model)

        self.temp()

        self.update_board(board_graphic=self.board_graphic, board_model=self.board_model)

        sys.exit(App.exec())

    def temp(self):
        worker = Worker(self.sow, board=self.board_model)
        self.threadpool.start(worker)

    def sow(self):
        self.board_model.iterate_sowing(player='a', hole=self.curr_value)
        self.curr_value -= 1
        self.update_board(board_graphic=self.board_graphic, board_model=self.board_model)



    def update_board(self, board_graphic: BoardGraphic, board_model: BoardModel):

        board_graphic.update_values(house_a_values=board_model.house_a_values, house_b_values=board_model.house_b_values,
                                             storeroom_a_value=board_model.storeroom_a_value,
                                             storeroom_b_value=board_model.storeroom_b_value)

        # def update_board(self):
        #     self.board_graphic.update_values(house_a_values=self.house_a_values, house_b_values=self.house_b_values,
        #                                      storeroom_a_value=self.storeroom_a_value,
        #                                      storeroom_b_value=self.storeroom_b_value)

