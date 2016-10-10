import sys
import functools

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QApplication, QPushButton)

import cells
import field
from communication import Communication


class Controls(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addLayout(self._get_cells_control())
        tick_button = QPushButton('Tick')
        tick_button.clicked.connect(Communication.tick.emit)
        layout.addWidget(tick_button)
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

        b = QPushButton('x')
        b.setFixedSize(20, 20)
        b.clicked.connect(functools.partial(Communication.control_button_clicked.emit, None))
        layout.addWidget(b)

        b = QPushButton('Clear')
        b.clicked.connect(Communication.clear_field.emit)
        layout.addWidget(b)

        return layout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Foxes and Robots')
        self.selected_cell = None

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(field.Field())
        layout.addWidget(Controls())

        Communication.control_button_clicked.connect(self._select_control_cell)
        Communication.cell_clicked.connect(self._cell_clicked)

        self.show()

    def _cell_clicked(self, cell):
        if self.selected_cell is None:
            cell.clear(full=False)
        elif issubclass(self.selected_cell, cells.Landscape):
            cell.set_landscape(self.selected_cell)
        else:
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
