#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from enum import Enum, unique


@unique
class TetrisShape(Enum):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class TetrisPiece:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pieceShape = None
        self.coords = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
        ]

        self.setShape(TetrisShape.NoShape)

    def setRandomShape(self):
        pass

    def setShape(self, shape):
        coordsTable = [
            [
                [0, 0], [0, 0], [0, 0], [0, 0]
            ],
            [
                [0, -1], [0, 0], [-1, 0], [-1, 1]
            ],
            [
                [0, -1], [0, 0], [1, 0], [1, 1]
            ],
            [
                [0, -1], [0, 0], [0, 1], [0, 2]
            ],
            [
                [-1, 0], [0, 0], [1, 0], [0, 1]
            ],
            [
                [0, 0], [1, 0], [0, 1], [1, 1]
            ],
            [
                [-1, -1], [0, -1], [0, 0], [0, 1]
            ],
            [
                [1, -1], [0, -1], [0, 0], [0, 1]
            ],
        ]

        for i in range(4):
            for j in range(2):
                self.coords[i][j] = coordsTable[shape.value][i][j]

        self.pieceShape = shape

    def shape(self):
        return self.pieceShape

    def x(self, i):
        return self.coords[i][0]

    def y(self, i):
        return self.coords[i][1]

    def minX(self):
        min_c = self.coords[0][0]
        for i in range(1, 4):
            min_c = min(min_c, self.coords[i][0])
        return min_c

    def maxX(self):
        max_c = self.coords[0][0]
        for i in range(1, 4):
            max_c = max(max_c, self.coords[i][0])
        return max_c

    def minY(self):
        min_c = self.coords[0][1]
        for i in range(1, 4):
            min_c = min(min_c, self.coords[i][1])
        return min_c

    def maxY(self):
        max_c = self.coords[0][1]
        for i in range(1, 4):
            max_c = max(max_c, self.coords[i][1])
        return max_c

    def rotatedLeft(self):
        if self.pieceShape == TetrisShape.SquareShape:
            return self

        result = TetrisPiece()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

    def rotatedRight(self):
        if self.pieceShape == TetrisShape.SquareShape:
            return self

        result = TetrisPiece()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result

    def setX(self, i, x):
        self.coords[i][0] = x

    def setY(self, i, y):
        self.coords[i][1] = y
