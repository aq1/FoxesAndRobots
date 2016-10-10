from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal


class Communication(QObject):
    """
    Object defines signals for application.
    """

    control_button_clicked = pyqtSignal(object)
    cell_clicked = pyqtSignal(object)
    tick = pyqtSignal()
    clear_field = pyqtSignal()


Communication = Communication()
