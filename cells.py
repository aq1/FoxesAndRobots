from PyQt5.QtWidgets import QPushButton

from communication import Communication


class Cell(QPushButton):

    def __init__(self, landscape, citizen=None):
        super().__init__(flat=True)
        self.landscape = landscape
        self.citizen = citizen
        self.setFixedSize(20, 20)
        self.set_style()
        self.clicked.connect(self._clicked)

    def _clicked(self):
        Communication.cell_clicked.emit(self)

    def set_citizen(self, citizen):
        self.citizen = citizen()
        self.set_style()

    def set_style(self):
        item = self.citizen or self.landscape
        self.setStyleSheet('background-color: #{};'.format(item.background_color))

    def tick(self):
        try:
            self.citizen.tick()
        except AttributeError:
            pass

    def enterEvent(self, event):
        item = self.citizen or self.landscape
        hc = ''.join([hex(int(int(item.background_color[i:i+1], 16) * 0.8))
                      for i in range(len(item.background_color))]).replace('0x', '')
        self.setStyleSheet("background-color: #{};".format(hc))

    def leaveEvent(self, event):
        self.set_style()


class ControlCell(Cell):
    def __init__(self, item):
        super().__init__(Landscape, item)
        self.item = item
        self.setToolTip(item.__name__)

    def _clicked(self):
        Communication.control_button_clicked.emit(self.item)


class Landscape:

    background_color = '000000'
    obstacle = False

    def interact(self):
        return NotImplemented()


class Field(Landscape):

    background_color = '7DCA9C'


class Berry(Landscape):

    background_color = 'B23484'


class Citizen:

    background_color = '000000'

    def __init__(self):
        super().__init__()

    def tick(self):
        return NotImplemented()


class Fox(Citizen):
    background_color = 'FC6D26'


class Robot(Citizen):
    background_color = '8EB0CC'
