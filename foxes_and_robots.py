import sys
import functools

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QApplication, QGridLayout, QPushButton)

import cells
from communication import Communication


class Controls(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addLayout(self._get_cells_control())
        layout.addStretch()

    def _get_cells_control(self):
        layout = QHBoxLayout()
        for x in dir(cells):
            try:
                item = getattr(cells, x)
                if issubclass(item, (cells.Landscape, cells.Citizen)) and item is not cells.Landscape and item is not cells.Citizen:
                    cell = cells.ControlCell(item)
                    layout.addWidget(cell)
            except TypeError:
                pass

        return layout


class Field(QWidget):

    WIDTH = 20
    HEIGHT = 20

    def replace_cell(self, i, j, cell):
        pass

    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                self.layout.addWidget(cells.Cell(cells.Field()), i, j)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Foxes and Robots')
        self.selected_cell = None

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(Field())
        layout.addWidget(Controls())

        Communication.control_button_clicked.connect(self._select_control_cell)
        Communication.cell_clicked.connect(self._cell_clicked)

        self.show()

    def _cell_clicked(self, cell):
        if self.selected_cell:
            cell.set_citizen(self.selected_cell)

    def _select_control_cell(self, cell):
        self.selected_cell = cell


def init_gui():
    app = QApplication(sys.argv)
    mw = MainWindow()

    with open('styles.qss') as f:
        app.setStyleSheet(f.read())
    sys.exit(app.exec_())


if __name__ == '__main__':
    init_gui()
