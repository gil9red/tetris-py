#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

import sys

from PySide.QtGui import *

from tetriswindow import TetrisWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    tetriswindow = TetrisWindow()
    tetriswindow.show()

    app.exec_()
