"""
Solution code. Fairly concise recursive backtracking generator.

Works by mutating one single board. This is much faster than creating a bunch of
new boards because it limits memory usage, so you get better caching or whatnot,
and also it avoids unnecessary allocation overhead.
"""

from sys import stderr
from time import time

progress_wait = 0
PROGRESS_RESET = 1000

def progress_report(fraction):
    """
    Display a progress bar at a certain fraction completion.
    """
    print("\r[{:<60}] ({:6.0%})".format(
            int(60 * fraction) * "-", fraction),
          end="", file=stderr, flush=True)

def solve(board, regs, pos=0, fraction=0, progress=False):
    """
    Solve a calcudoku in `board`, using regions defined in `regs`, going from
    position "pos".

    Calcudokus are represented as flat lists. It may be tempting to use a 2-D
    array, but really there's nothing inherently two-dimensional about a
    calcudoku, and it's much better to just think of it as a set of tiles, where
    some subsets happen to correspond to regions with some associated rules.
    """
    # used to track how often to show progress report
    global progress_wait
    if progress:
        if progress_wait <= 0:
            progress_wait = PROGRESS_RESET
            progress_report(fraction)
        else:
            progress_wait -= 1
    if pos == 64:
        yield board
    else:
        for i in range(1, 9):
            board[pos] = i
            if all(r.isvalid(board) for r in regs[pos]):
                # teensy bit of maths to work out the next fraction
                yield from solve(board, regs, pos + 1,
                                 fraction + 8 ** -(pos + 1) * (i - 1),
                                 progress)
        board[pos] = None
    # just so we finish on 100%.
    if progress and pos == 0:
        progress_report(1)
        print(file=stderr)
