# https://doc.qt.io/qtforpython-6/gettingstarted.html#create-your-first-qt-application-with-qt-widgets

from typing import Self
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


class Widget(QtWidgets.QWidget):
    def __init__(self: Self):
        super().__init__()

        self.hello = ["hey", "there"]
        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hi world", alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self: Self) -> None:
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Widget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
