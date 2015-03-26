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
        Signal
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

        boardTop = rect.bottom() - TetrisBoard.BOARD_HEIGHT * self.squareHeight()

        for i in range(TetrisBoard.BOARD_HEIGHT):
            for j in range(TetrisBoard.BOARD_WIDTH):
                shape = self.getShapeAt(j, TetrisBoard.BOARD_HEIGHT - i - 1)
                if shape != TetrisShape.NoShape:
                    self.drawSquare(painter, rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != TetrisShape.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                                boardTop + (self.BOARD_HEIGHT - y - 1) * self.squareHeight(),
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

    def setShapeAt(self, x, y, value):
        self.board[(y * TetrisBoard.BOARD_WIDTH) + x] = value

    def getShapeAt(self, x, y):
        return self.board[(y * TetrisBoard.BOARD_WIDTH) + x]

    def timeoutTime(self):
        return 1000 / (1 + self.level)

    def squareWidth(self):
        return self.contentsRect().width() / TetrisBoard.BOARD_WIDTH

    def squareHeight(self):
        return self.contentsRect().height() / TetrisBoard.BOARD_HEIGHT

    def clearBoard(self):
        for i in range(TetrisBoard.BOARD_WIDTH * TetrisBoard.BOARD_HEIGHT):
            self.board[i] = TetrisShape.NoShape

    def dropDown(self):
        dropHeight = 0
        newY = self.curY

        while newY > 0:
            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break
            newY -= 1
            dropHeight += 1

        self.pieceDropped(dropHeight)

    def oneLineDown(self):
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped(0)

    def pieceDropped(self, dropHeight):
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.numPiecesDropped += 1
        if self.numPiecesDropped % 25 == 0:
            self.level += 1
            self.timer.start(self.timeoutTime(), self)
            self.levelChanged(self.level)

        self.score += dropHeight + 7
        self.scoreChanged(self.score)
        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()

    def removeFullLines(self):
        numFullLines = 0

        # TODO: возможно тут ошибка
        for i in reversed(range(TetrisBoard.BOARD_HEIGHT - 1)):
            lineIsFull = True

            for j in TetrisBoard.BOARD_WIDTH:
                if self.shapeAt(j, i) == TetrisShape.NoShape:
                    lineIsFull = False
                    break

            if lineIsFull:
                numFullLines += 1
                # TODO: возможно тут ошибка
                for k in range(i, TetrisBoard.BOARD_HEIGHT - 1):
                    for j in range(TetrisBoard.BOARD_WIDTH):
                        self.setShapeAt(j, k, self.getShapeAt(j, k + 1))

                for j in range(TetrisBoard.BOARD_WIDTH):
                    self.setShapeAt(j, TetrisBoard.BOARD_HEIGHT - 1, TetrisShape.NoShape)

        if numFullLines > 0:
            self.numLinesRemoved += numFullLines
            self.score += 10 * numFullLines
            self.linesRemovedChanged(self.numLinesRemoved)
            self.scoreChanged(self.score)

            self.timer.start(500, self)
            self.isWaitingAfterLine = True
            self.curPiece.setShape(TetrisShape.NoShape)
            self.update()

    def newPiece(self):
        curPiece = self.nextPiece
        self.nextPiece.setRandomShape()
        self.showNextPiece()
        curX = TetrisBoard.BOARD_WIDTH / 2 + 1
        curY = TetrisBoard.BOARD_HEIGHT - 1 + curPiece.minY()

        if not self.tryMove(curPiece, curX, curY):
            curPiece.setShape(TetrisShape.NoShape)
            self.timer.stop()
            self.isStarted = False

    def showNextPiece(self):
        if not self.nextPieceLabel:
            return

        dx = self.nextPiece.maxX() - self.nextPiece.minX() + 1
        dy = self.nextPiece.maxY() - self.nextPiece.minY() + 1

        pixmap = QPixmap(dx * self.squareWidth(), dy * self.squareHeight())
        painter = QPainter(pixmap)
        painter.fillRect(pixmap.rect(), self.nextPieceLabel.palette().background())

        for i in range(4):
            x = self.nextPiece.x(i) - self.nextPiece.minX()
            y = self.nextPiece.y(i) - self.nextPiece.minY()
            self.drawSquare(painter, x * self.squareWidth(), y * self.squareHeight(),
                            self.nextPiece.shape())

        self.nextPieceLabel.setPixmap(pixmap)

    def tryMove(self, newPiece, newX, newY):
        for i in range(4):
            x = newX + newPiece.x(i);
            y = newY - newPiece.y(i);
            if x < 0 or x >= TetrisBoard.BOARD_WIDTH or y < 0 or y >= TetrisBoard.BOARD_HEIGHT:
                return False
            
            if self.getShapeAt(x, y) != TetrisShape.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()
        return True

    def drawSquare(self, painter, x, y, shape):
        COLORTABLE = [
            0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
            0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00
        ]

        color = COLORTABLE[shape.value]
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, self.squareHeight() - 2, color)

        painter.setPen(color.light())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.dark())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + 1)
