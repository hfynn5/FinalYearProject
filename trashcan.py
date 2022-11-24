import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle("drawing")

        self.label = QtWidgets.QLabel()

        # canvas = QtGui.QPixmap(400, 300)
        # self.label.setPixmap(canvas)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawRect(50, 15, 300, 100)



    def draw_something(self):
        painter = QtGui.QPainter()
        #painter.begin(self.label.pixmap())
        painter.drawLine(10, 10, 300, 200)
        painter.end()


App = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(App.exec())
