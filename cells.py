import random
from collections import namedtuple

from PyQt5.QtWidgets import QPushButton

import config
import utils
from communication import Communication


class Cell(QPushButton):

    def __init__(self, field, landscape, pos, citizen=None):
        super().__init__(flat=True)
        self.style = namedtuple('Style', ['background_color'])(background_color='FFFFFF')
        self.landscape = landscape
        self.pos_ = utils.Position(pos)
        self.field = field
        self.citizen = citizen
        self.setFixedSize(20, 20)
        self.set_style()
        self.clicked.connect(self._clicked)

    def _clicked(self):
        Communication.cell_clicked.emit(self)

    def clear(self, full=False):
        if self.citizen:
            self.remove_citizen()
            if not full:
                return
        self.remove_landscape()

    def remove_citizen(self):
        self.citizen = None
        self.set_style()

    def remove_landscape(self):
        self.landscape = None
        self.set_style()

    def set_citizen(self, citizen):
        self.citizen = citizen(self)
        self.set_style()

    def set_landscape(self, landscape):
        self.landscape = landscape()
        self.set_style()

    def set_style(self):
        item = self.citizen or self.landscape or self.style
        self.setStyleSheet('background-color: #{};'.format(item.background_color))

    def tick(self):
        if self.landscape:
            self.landscape.tick()

        if self.citizen:
            self.citizen.tick()

    def apply_tick(self):
        if self.citizen:
            self.citizen.apply_tick()

    def is_occupied(self, future=False):
        occupied = bool(self.citizen) or not isinstance(self.landscape, Field)
        if not occupied and future:
            return any([c.citizen.next_cell is self
                        for c in self.field.get_cells_in_range(*self.pos_, r=1) if c.citizen])
        return occupied

    def enterEvent(self, event):
        item = self.citizen or self.landscape or self.style
        hc = ''.join([hex(int(int(item.background_color[i:i+1], 16) * 0.8))
                      for i in range(len(item.background_color))]).replace('0x', '')
        self.setStyleSheet("background-color: #{};".format(hc))

    def leaveEvent(self, event):
        self.set_style()


class ControlCell(Cell):
    def __init__(self, item):
        super().__init__(None, Landscape, (), item)
        self.item = item
        self.setToolTip(item.__name__)

    def _clicked(self):
        Communication.control_button_clicked.emit(self.item)

    def tick(self):
        pass


class Landscape:

    background_color = '000000'
    obstacle = False

    def interact(self):
        return NotImplemented

    def tick(self):
        return NotImplemented


class Field(Landscape):

    background_color = '7DCA9C'

    def tick(self):
        pass


class Berry(Landscape):

    background_color = 'B23484'

    def tick(self):
        print('Berry!')


class EnergyCell(Landscape):

    background_color = 'F9DE21'

    def tick(self):
        print('EnergyCell!')


class Citizen:

    background_color = '000000'

    def __init__(self, cell):
        self.cell = cell
        self.next_cell = cell

    def tick(self):
        return NotImplemented

    def apply_tick(self):
        return NotImplemented

    def move(self):
        # todo: in hurry
        if self.next_cell == self.cell:
            return

        self.next_cell.citizen = self
        self.next_cell.set_style()
        self.cell.remove_citizen()
        self.cell = self.next_cell


class Fox(Citizen):
    background_color = 'FC6D26'
    MAX_HUNGER = 100

    def __init__(self, cell):
        super().__init__(cell)
        self.hunger = self.MAX_HUNGER - random.randint(0, 5)
        self.known_places = {}

    def _run(self, cell):
        direction = self.cell.pos_ - cell.pos_
        direction.to_vector()
        cell = self.cell.field.get_cell_at(*(self.cell.pos_ + direction))
        if not cell.is_occupied(future=True):
            self.next_cell = cell

    def apply_tick(self):
        self.move()

    def tick(self):
        cells = self.cell.field.get_cells_in_range(*self.cell.pos_, r=2)
        berries = []
        for cell in cells:
            if isinstance(cell.citizen, Robot):
                self._run(cell)
                break
            if isinstance(cell.landscape, Berry):
                berries.append(cell)

        self.hunger -= 1


class Robot(Citizen):
    background_color = '8EB0CC'
    MAX_HUNGER = 200

    def __init__(self, cell):
        super().__init__(cell)
        self.hunger = self.MAX_HUNGER - random.randint(0, 20)
        # Todo
        self.hive_mind = None

    def tick(self):
        self.hunger -= 1

        cells = self.cell.field.get_free_cells_in_range(*self.cell.pos_, r=1)
        self.next_cell = cells[random.randint(0, len(cells) - 1)]
        self.hunger -= 1

    def apply_tick(self):
        self.move()
