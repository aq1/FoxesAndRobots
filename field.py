from PyQt5.QtWidgets import QWidget, QGridLayout

import utils
import cells
from communication import Communication


class Field(QWidget):

    WIDTH = 20
    HEIGHT = 20
    # _instance = None

    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super().__new__(cls, *args, **kwargs)
    #     return cls._instance

    def replace_cell(self, i, j, cell):
        pass

    def _init(self):
        utils.clear_layout(self.layout)
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                self.layout.addWidget(cells.Cell(self, cells.Field(), (i, j)), i, j)

    def __init__(self):
        super().__init__()

        Communication.clear_field.connect(self._init)
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self._init()
