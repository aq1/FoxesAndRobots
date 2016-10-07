import random
from collections import namedtuple

from PyQt5.QtWidgets import QPushButton

import field
from communication import Communication


class Cell(QPushButton):

    def __init__(self, field, landscape, pos, citizen=None):
        super().__init__(flat=True)
        self.style = namedtuple('Style', ['background_color'])(background_color='FFFFFF')
        self.landscape = landscape
        self._pos = pos
        self.citizen = citizen
        self.setFixedSize(20, 20)
        self.set_style()
        self.clicked.connect(self._clicked)
        Communication.tick.connect(self.tick)

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


    def enterEvent(self, event):
        item = self.citizen or self.landscape or self.style
        hc = ''.join([hex(int(int(item.background_color[i:i+1], 16) * 0.8))
                      for i in range(len(item.background_color))]).replace('0x', '')
        self.setStyleSheet("background-color: #{};".format(hc))

    def leaveEvent(self, event):
        self.set_style()


class ControlCell(Cell):
    def __init__(self, item):
        super().__init__(None, Landscape, None, item)
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
        return NotImplemented()

    def tick(self):
        return NotImplemented()


class Field(Landscape):

    background_color = '7DCA9C'

    def tick(self):
        pass


class Berry(Landscape):

    background_color = 'B23484'

    def tick(self):
        print('Berry!')


class Citizen:

    background_color = '000000'

    def __init__(self, cell):
        self.cell = cell

    def tick(self):
        return NotImplemented()


class Fox(Citizen):
    background_color = 'FC6D26'
    MAX_HUNGER = 10

    def __init__(self, cell):
        super().__init__(cell)
        self.hunger = self.MAX_HUNGER - random.randint(0, 2)
        self.known_places = {}

    def tick(self):
        self.hunger -= 0.1


class Robot(Citizen):
    background_color = '8EB0CC'

    def tick(self):
        print('Robot!')
