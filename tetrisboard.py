#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from PySide.QtGui import *
from PySide.QtCore import *

from tetrispiece import TetrisPiece, TetrisShape


# TODO: закончить портирование

class TetrisBoard(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.timer = QBasicTimer()
        self.nextPieceLabel = None
        self.isStarted = False
        self.isPaused = False
        self.isWaitingAfterLine = False
        self.curPiece = TetrisPiece()
        self.nextPiece = TetrisPiece()
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.numPiecesDropped = 0
        self.score = 0
        self.level = 0
        self.board = [TetrisShape.NoShape
                      for i in range(TetrisBoard.BOARD_WIDTH * TetrisBoard.BOARD_HEIGHT)]

        # Сигналы
        self.scoreChanged = Signal(int)
        self.levelChanged = Signal(int)
        self.linesRemovedChanged = Signal(int)

    def setNextPieceLabel(self, label):
        pass

    def sizeHint(self):
        pass

    def minimumSizeHint(self):
        pass

    # @Slot
    def start(self):
        pass

    # @Slot
    def pause(self):
        pass

    def paintEvent(self, event):
        pass

    def keyPressEvent(self, event):
        pass

    def timerEvent(self, event):
        pass

    BOARD_WIDTH = 10
    BOARD_HEIGHT = 22

    def shapeAt(self, x, y):
        return self.board[(y * TetrisBoard.BOARD_WIDTH) + x]

    def timeoutTime(self):
        return 1000 / (1 + self.level)

    def squareWidth(self):
        return self.contentsRect().width() / TetrisBoard.BOARD_WIDTH

    def squareHeight(self):
        return self.contentsRect().height() / TetrisBoard.BOARD_HEIGHT

    def clearBoard(self):
        pass

    def dropDown(self):
        pass

    def oneLineDown(self):
        pass

    def pieceDropped(self, dropHeight):
        pass

    def removeFullLines(self):
        pass

    def newPiece(self):
        pass

    def showNextPiece(self):
        pass

    def tryMove(self, newPiece, newX, newY):
        pass

    def drawSquare(self, painter, x, y, shape):
        pass
