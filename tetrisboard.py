#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from PySide.QtGui import *
from PySide.QtCore import *

from tetrispiece import TetrisPiece, TetrisShape


# TODO: закончить портирование

class TetrisBoard(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setFocusPolicy(Qt.StrongFocus)

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

        self.clearBoard()
        self.nextPiece.setRandomShape()

        # Сигналы
        self.scoreChanged = Signal(int)
        self.levelChanged = Signal(int)
        self.linesRemovedChanged = Signal(int)

    def setNextPieceLabel(self, label):
        self.nextPieceLabel = label

    def sizeHint(self):
        return QSize(TetrisBoard.BOARD_WIDTH * 15 + self.frameWidth() * 2,
                     TetrisBoard.BOARD_HEIGHT * 15 + self.frameWidth() * 2)

    def minimumSizeHint(self):
        return QSize(TetrisBoard.BOARD_WIDTH * 5 + self.frameWidth() * 2,
                     TetrisBoard.BOARD_HEIGHT * 5 + self.frameWidth() * 2)

    # @Slot
    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.numPiecesDropped = 0
        self.score = 0
        self.level = 1
        self.clearBoard()

        self.linesRemovedChanged.emit(self.numLinesRemoved)
        self.scoreChanged.emit(self.score)
        self.levelChanged.emit(self.level)

        self.newPiece()
        self.timer.start(self.timeoutTime(), self)

    # @Slot
    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        if self.isPaused:
            self.timer.stop()
        else:
            self.timer.start(self.timeoutTime(), self)

        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        rect = self.contentsRect()

        if self.isPaused:
            painter.drawText(rect, Qt.AlignCenter, "Pause")
            return

        boardTop = rect.bottom() - TetrisBoard.BoardHeight * self.squareHeight()

        for i in range(TetrisBoard.BoardHeight):
            for j in range(TetrisBoard.BoardWidth):
                shape = self.shapeAt(j, TetrisBoard.BoardHeight - i - 1)
                if shape != TetrisShape.NoShape:
                    self.drawSquare(painter, rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != TetrisShape.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                                boardTop + (self.BoardHeight - y - 1) * self.squareHeight(),
                                self.curPiece.shape())

    def keyPressEvent(self, event):
        if not self.isStarted or self.isPaused or self.curPiece.shape() == TetrisShape.NoShape:
            super().keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotatedRight(), self.curX, self.curY)

        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotatedLeft(), self.curX, self.curY)

        elif key == Qt.Key_Space:
            self.dropDown()

        elif key == Qt.Key_D:
            self.oneLineDown()

        else:
            super().keyPressEvent(event)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId:
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
                self.timer.start(self.timeoutTime(), self)
            else:
                self.oneLineDown()
        else:
            super().timerEvent(event)

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
