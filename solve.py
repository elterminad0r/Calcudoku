"""
Solution code. Fairly concise recursive backtracking generator.

Works by mutating one single board. This is much faster than creating a bunch of
new boards because it limits memory usage, so you get better caching or whatnot,
and also it avoids unnecessary allocation overhead.

In order to prevent confusion when you're trying to generate a list of results,
it yields deep copies of solutions.

The code doing the actual solving is probably about 20 lines. Almost all of this
module is concerned with printing pretty progress reports.
"""

# TODO: visualisation of current state, maybe one day.

from sys import stderr
from time import time
from io import StringIO

PROGRESS_RESET = 1000
BAR_WIDTH = 40

def progress_report(fraction, visited, start, file=stderr):
    """
    Display a progress bar at a certain fraction completion.

    The estimate of number of boards is drawn from the total space of possible
    boards, most of which are pruned with the backtracking. It's not meant to
    suggest that boards are actually being processed at that speed. This is only
    done this way because it's really hard to guess in advance how many actual
    board will be looked at (and it looks impressive).

    It does also directly print the current total number of examined boards,
    just to have a little flex on big O.
    """
    print("\r[{:<{w}}] ({:4.0%}) ~{:7.1e}/{:7.1e} b, {:7.1e} v, {:7.1e} v/s"
            .format(
                int(BAR_WIDTH * fraction) * "-", fraction,
                int(fraction * 8 ** 64), 8 ** 64,
                visited,
                visited / (time() - start),
                w=BAR_WIDTH),
          end="", file=file, flush=True)

def solve(regs, progress=False):
    """
    Solve a calcudoku in `board`, using regions defined in `regs`, going from
    position "pos".

    Calcudokus are represented as flat lists. It may be tempting to use a 2-D
    array, but really there's nothing inherently two-dimensional about a
    calcudoku, and it's much better to just think of it as a set of tiles, where
    some subsets happen to correspond to regions with some associated rules.
    """
    if progress:
        # used to track how often to show progress report
        progress_wait = 0
        # used to track how many board have been visited
        visited = 0
        # start time, used to calculate average rate of processing boards
        start = time()
    def _solve(board, regs, pos, fraction, progress):
        """
        Function that actually does the recursive solving. This is within a
        closure so that the wrapping function can set up some of the variables,
        and furthermore we can use "global"-like variables without them actually
        being global.
        """
        if progress:
            nonlocal progress_wait, visited
            visited += 1
            if progress_wait <= 0:
                progress_wait = PROGRESS_RESET
                progress_report(fraction, visited, start)
            else:
                progress_wait -= 1
        if pos == len(board):
            # erase current progress report
            if progress:
                # write a progress report to a mock output to determine the
                # length, because I'm lazy and only want to keep track of a
                # single thing.
                dummy_progress = StringIO()
                progress_report(fraction, visited, start, file=dummy_progress)
                print("\r{}\r".format(" " * len(dummy_progress.getvalue())),
                        end="", file=stderr, flush=True)
            yield board.copy()
        else:
            for i in range(1, 9):
                board[pos] = i
                if all(r.isvalid(board) for r in regs[pos]):
                    # teensy bit of maths to work out the next fraction
                    yield from _solve(board, regs, pos + 1,
                                      fraction + 8 ** -(pos + 1) * (i - 1),
                                      progress)
            board[pos] = None
        # just so we finish on 100%.
        if progress and pos == 0:
            progress_report(1, visited, start)
            print(file=stderr)
    # TODO: no hardcode
    yield from _solve([None] * 64, regs, 0, 0, progress)
