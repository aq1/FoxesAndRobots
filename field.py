import random

from PyQt5.QtWidgets import QWidget, QGridLayout

import utils
from config import Foxes, Robots, Berries, EnergyCells
import cells
from communication import Communication


class Field(QWidget):

    WIDTH = 30
    HEIGHT = 30

    def replace_cell(self, i, j, cell):
        pass

    def _clear(self):
        for cell in self.findChildren(cells.Cell):
            cell.set_landscape(cells.Field)
            cell.remove_citizen()

    def _populate(self):
        self._clear()
        for cls, range_ in zip((Foxes, Robots), (((0, self.HEIGHT - 1), (0, self.WIDTH // 2)), ((0, self.HEIGHT - 1), (self.WIDTH // 2, self.WIDTH - 1)))):
            if cls.home:
                self.get_cell_at(*cls.home).setText('')
            cls.home = random.randint(*range_[0]), random.randint(*range_[1])
            coords = self.get_coords_in_range(cls.home[0], cls.home[1], 1)
            random.shuffle(coords)
            self.get_cell_at(*cls.home).setText(cls.citizen[0])
            for pos in coords[:cls.init_population]:
                citizen = getattr(cells, cls.citizen)
                if not citizen:
                    raise AttributeError('No citizen found')
                self.get_cell_at(*pos).set_citizen(citizen)

        for cls in Berries, EnergyCells:
            q = cls.initial_quantity
            while q > 0:
                pos = random.randint(0, self.HEIGHT - 1), random.randint(0, self.WIDTH - 1)
                cell = self.get_cell_at(*pos)
                if not cell.is_occupied():
                    cell.set_landscape(getattr(cells, cls.cell))
                    q -= 1

    def get_coords_in_range(self, x, y, r):
        return [(xx % self.HEIGHT, yy % self.WIDTH) for xx in range(x - r, x + r + 1) for yy in range(y - r, y + r + 1)]

    def get_cell_at(self, x, y):
        return self.layout.itemAt(x * self.WIDTH + y).widget()

    def get_cells_in_range(self, x, y, r):
        return list(map(lambda c: self.get_cell_at(*c), self.get_coords_in_range(x, y, r)))

    def get_free_cells_in_range(self, x, y, r):
        cells = self.get_cells_in_range(x, y, r)
        occupied_cells = [cell.citizen.next_cell for cell in cells if cell.citizen]
        return [c for c in cells if c not in occupied_cells]

    def tick(self):
        cells_ = self.findChildren(cells.Cell)

        for cell in cells_:
            cell.tick()

        for cell in cells_:
            cell.apply_tick()

    def __init__(self):
        super().__init__()

        Communication.clear_field.connect(self._clear)
        Communication.populate.connect(self._populate)
        Communication.tick.connect(self.tick)
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                self.layout.addWidget(cells.Cell(self, cells.Field(), (i, j)), i, j)
        self._clear()
