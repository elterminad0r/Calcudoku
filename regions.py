"""
Object-oriented definitions of board regions, for both regions like rows or
columns, or regions of arithmetically related numbers.
"""

import abc
import sys

from functools import reduce
from operator import mul

def product(l):
    """
    Product of an iterable of numbers.
    """
    return reduce(mul, l, 1)

def skip_one(l, item):
    """
    Yield everything from a list except for `item`, the first time it occurs.
    """
    it = iter(l)
    for i in it:
        if i == item:
            break
        yield i
    yield from it

def partition_max(l):
    """
    Partition an *list* into its maximum and all the rest. This frequently
    comes up in calcudoku calculations, so it's useful to have defined.
    O(n) time, which is obviously the best anyone could do, asymptotically, as
    we must scan for the maximum. Needs to scan twice.
    """
    m = max(l)
    return m, skip_one(l, m)

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

    def isvalid(self, board):
        """
        Determine if a state is valid as far as this region is concerned.
        Children should implement fullvalid to determine if a fully filled in
        region, respectively, is valid or not.

        Optionally, children can override partialvalid to determine if a
        partially filled in region can be immediately discarded as invalid. This
        is highly encouraged, as this enables backtracking, pruning huge swathes
        of boards. partialvalid will only be called if there is at least one
        filled in square in the region.

        It may that the caller has entered number in the appropriate range.
        """
        squares = self.getsquares(board)
        if len(squares) == self.size:
            return self.fullvalid(squares)
        return self.partialvalid(squares)

    @abc.abstractmethod
    def fullvalid(self, squares):
        raise NotImplementedError

    def partialvalid(self, squares):
        return True

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
        m, rest = partition_max(squares)
        return m == sum(rest) + self.target

    # TODO: clever partialvalid. May not even be possible

class DivideRegion(Region):
    """
    Region for division
    """
    def fullvalid(self, squares):
        m, rest = partition_max(squares)
        return m * self.target == product(rest)

    # TODO: clever partialvalid. May not even be possible

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
# TODO: really this shouldn't be hardcoded to 8
COLUMNS = [ColumnRegion(i) for i in range(8)]
ROWS = [RowRegion(i) for i in range(8)]

# a defense mechanism to protect me from myself
if __name__ == "__main__":
    sys.exit("Not a runnable module: see calcudoku.py")
