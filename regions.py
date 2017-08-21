from functools import reduce
from operator import mul, floordiv

def product(l):
    return reduce(mul, l, 1)

class Region:
    def __init__(self, target, positions):
        self.target = target
        self.positions = positions
        self.size = len(positions)

    def __str__(self):
        return "{}({}, {})".format(self.__class__.__name__, self.target, self.positions)

    def __repr__(self):
        return str(self)

    def isvalid(self, board):
        squares = self.getsquares(board)
        if len(squares) == self.size:
            #print(self, squares, self.fullvalid(squares))
            return self.fullvalid(squares)
        #print(self, squares, self.partialvalid(squares))
        return self.partialvalid(squares)

    def getsquares(self, board):
        return [j for j in (board[i] for i in self.positions) if j]

class PlusRegion(Region):
    def fullvalid(self, squares):
        return sum(squares) == self.target

    def partialvalid(self, squares):
        return sum(squares) < self.target

class TimesRegion(Region):
    def fullvalid(self, squares):
        return product(squares) == self.target

    def partialvalid(self, squares):
        return self.target % product(squares) == 0

class MinusRegion(Region):
    def fullvalid(self, squares):
        s = sorted(squares, reverse=True)
        return s[0] == sum(s[1:]) + self.target

    def partialvalid(self, squares):
        s = sorted(squares, reverse=True)
        return True#s[0] < sum(s[1:]) + self.target# or self.target  sum(s)

class DivideRegion(Region):
    def fullvalid(self, squares):
        s = sorted(squares, reverse=True)
        return s[0] * self.target == product(s[1:])

    def partialvalid(self, squares):
        s = sorted(squares, reverse=True)
        return s[0] * self.target % product(s[1:]) == 0 or self.target > product(s)

class StraightRegion(Region):
    def __init__(self, positions):
        super().__init__(None, positions)

    def fullvalid(self, squares):
        return len(set(squares)) == len(squares)

    def partialvalid(self, squares):
        return self.fullvalid(squares)

class RowRegion(StraightRegion):
    def __init__(self, start_pos):
        super().__init__([start_pos * 8 + i for i in range(8)])

class ColumnRegion(StraightRegion):
    def __init__(self, start_pos):
        super().__init__([i * 8 + start_pos for i in range(8)])
