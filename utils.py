"""
Module for common gui operations.
"""

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGroupBox, QScrollArea, QGraphicsDropShadowEffect


def get_scrollable(layout):
    """
    Convert layout to a scrollable widget.
    """

    widget = QWidget()

    groupbox = QGroupBox()
    groupbox.setLayout(layout)
    scroll = QScrollArea()
    scroll.setWidget(groupbox)
    scroll.setWidgetResizable(True)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    this_vbox = QVBoxLayout(widget)
    this_vbox.addWidget(scroll)
    this_vbox.setContentsMargins(0, 0, 0, 0)
    this_vbox.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    return widget


def get_shadow():
    """
    Returns shadow effect.
    """

    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)
    shadow.setXOffset(0)
    shadow.setYOffset(0)
    return shadow


def clear_layout(layout):
    """
    Delete everything from the given layout.
    """

    for i in reversed(range(layout.count())):
        item = layout.takeAt(i)
        try:
            item.widget().setParent(None)
        except AttributeError:
            pass


class Position(tuple):

    def __add__(self, other):
        assert len(other) == 2
        return Position((self[0] - other[0], self[1] - other[1]))

    def __sub__(self, other):
        assert len(other) == 2
        return Position((self[0] - other[0], self[1] - other[1]))

    def __dir__(self, other):
        assert len(other) == 2
        x = other[0] or 1
        y = other[1] or 1
        return Position((self[0] / x, self[1] / y))
