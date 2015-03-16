#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from PySide.QtGui import *
from PySide.QtCore import *

from tetrisboard import TetrisBoard


class TetrisWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.nextPieceLabel = QLabel()
        self.nextPieceLabel.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.nextPieceLabel.setAlignment(Qt.AlignCenter)

        self.board = TetrisBoard()
        self.board.setNextPieceLabel(self.nextPieceLabel)

        self.scoreLcd = QLCDNumber()
        self.scoreLcd.setSegmentStyle(QLCDNumber.Filled)

        self.levelLcd = QLCDNumber()
        self.levelLcd.setSegmentStyle(QLCDNumber.Filled)

        self.linesLcd = QLCDNumber()
        self.linesLcd.setSegmentStyle(QLCDNumber.Filled)

        self.startButton = QPushButton("Start")
        self.startButton.setFocusPolicy(Qt.NoFocus)

        self.quitButton = QPushButton("Quit")
        self.quitButton.setFocusPolicy(Qt.NoFocus)

        self.pauseButton = QPushButton("Pause")
        self.pauseButton.setFocusPolicy(Qt.NoFocus)

        layout = QGridLayout()
        layout.addWidget(self.createLabel("NEXT"), 0, 0)
        layout.addWidget(self.nextPieceLabel, 1, 0)
        layout.addWidget(self.createLabel("LEVEL"), 2, 0)
        layout.addWidget(self.levelLcd, 3, 0)
        layout.addWidget(self.startButton, 4, 0)
        layout.addWidget(self.board, 0, 1, 6, 1)
        layout.addWidget(self.createLabel("SCORE"), 0, 2)
        layout.addWidget(self.scoreLcd, 1, 2)
        layout.addWidget(self.createLabel("LINES REMOVED"), 2, 2)
        layout.addWidget(self.linesLcd, 3, 2)
        layout.addWidget(self.quitButton, 4, 2)
        layout.addWidget(self.pauseButton, 5, 2)
        self.setLayout(layout)

        self.setWindowTitle("Tetris")
        self.resize(550, 370)

    def createLabel(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        return label
