"""
Object-oriented definitions of board regions, for both regions like rows or
columns, or regions of arithmetically related numbers.
"""

import abc

from functools import reduce
from operator import mul, floordiv

def product(l):
    """
    Product of an iterable of numbers.
    """
    return reduce(mul, l, 1)

class Region(abc.ABC):
    """
    Base class for a region. Provides output formatting and some boilerplate
    methods
    """
    def __init__(self, target, positions):
        """
        Target: the number we are aiming to make
        """
        self.target = target
        self.positions = positions
        self.size = len(positions)

    def __str__(self):
        return "{}({}, {})".format(self.__class__.__name__, self.target,
                                   self.positions)

    def __repr__(self):
        return str(self)

    @abc.abstractmethod
    def fullvalid(self, squares):
        raise NotImplementedError

    @abc.abstractmethod
    def partialvalid(self, squares):
        raise NotImplementedError

    def isvalid(self, board):
        """
        Determine if a state is valid as far as this region is concerned.
        Children should implement partialvalid and fullvalid to determine if a
        partially or fully filled in region, respecitvely,  is valid or not.

        It may that the caller has entered number in the appropriate range.
        """
        squares = self.getsquares(board)
        if len(squares) == self.size:
            return self.fullvalid(squares)
        return self.partialvalid(squares)

    def getsquares(self, board):
        """
        Get the squares in the region that are filled in.
        """
        return [j for j in (board[i] for i in self.positions) if j]

class PlusRegion(Region):
    """
    Region for addition
    """
    def fullvalid(self, squares):
        return sum(squares) == self.target

    def partialvalid(self, squares):
        return sum(squares) < self.target

class TimesRegion(Region):
    """
    Region for multiplication
    """
    def fullvalid(self, squares):
        return product(squares) == self.target

    def partialvalid(self, squares):
        return self.target % product(squares) == 0

class MinusRegion(Region):
    """
    Region for subtraction
    """
    def fullvalid(self, squares):
        s = sorted(squares, reverse=True)
        return s[0] == sum(s[1:]) + self.target

    def partialvalid(self, squares):
        s = sorted(squares, reverse=True)
        # TODO: not yet cleverly implemented. May not even be possible
        return True

class DivideRegion(Region):
    """
    Region for division
    """
    def fullvalid(self, squares):
        s = sorted(squares, reverse=True)
        return s[0] * self.target == product(s[1:])

    def partialvalid(self, squares):
        s = sorted(squares, reverse=True)
        # TODO: not yet cleverly implemented. May not even be possible
        return True

class SudokuRegion(Region):
    """
    Sub-baseclass region for sudoku-like regions (rows and columns that require
    each entry to be unique.
    """
    def __init__(self, positions):
        super().__init__(None, positions)

    def fullvalid(self, squares):
        return len(set(squares)) == len(squares)

    def partialvalid(self, squares):
        return self.fullvalid(squares)

class RowRegion(SudokuRegion):
    """
    Region for a row.
    """
    def __init__(self, start_pos):
        super().__init__([start_pos * 8 + i for i in range(8)])

class ColumnRegion(SudokuRegion):
    """
    Region for a column.
    """
    def __init__(self, start_pos):
        super().__init__([i * 8 + start_pos for i in range(8)])

# Some overall registries of all the classes here, used in parsing calcudoku
# files.
REG_MAP = dict(zip("+-*/",
                   [PlusRegion, MinusRegion, TimesRegion, DivideRegion]))
COLUMNS = [ColumnRegion(i) for i in range(8)]
ROWS = [RowRegion(i) for i in range(8)]
