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

# TODO: visualisation of current state, maybe one day (ncurses??)

import sys

from time import time
from io import StringIO

ASCII_PROG_CHARS = ">="
UNICODE_PROG_CHARS = " ▏▎▍▌▋▊▉██"

def format_bar(width, fraction, unicode=None, prog_chars=None):
    """
    Format just the actual progress bar given the characters, width, and
    percentage completion.

    The characters should be a list-like object, where the last character is to
    be used for the solid bar, and the first (length - 1) characters are a
    linear progression to go through.
    """
    if prog_chars is None:
        if unicode is not None:
            prog_chars = UNICODE_PROG_CHARS if unicode else ASCII_PROG_CHARS
        else:
            raise ValueError("Need either to pass unicode, or pass characters")
    integral, fractional = divmod(width * fraction, 1)
    return "{}{}".format(prog_chars[-1] * int(integral),
                         prog_chars[int((len(prog_chars) - 1) * fractional)]
                            if fractional else "")

def progress_report(fraction, visited, start, unicode, width, file=sys.stderr):
    """
    Display a progress bar at a certain fraction completion.

    The estimate of number of boards is drawn from the total space of possible
    boards, most of which are pruned with the backtracking. It's not meant to
    suggest that boards are actually being processed at that speed. This is only
    done this way because it's really hard to guess in advance how many actual
    board will be looked at (and it looks impressive). Another unfortunate
    consequence of this is that the main progress bar is not linear - it tends
    to jump around unpredictably. This is usually considered a feature of
    progress bars so I'm not hugely fussed.

    It does also directly print the current total number of examined boards,
    just to have a little flex on big O.
    """
    print("\r[{:<{w}}] ({:4.0%}) ~{:7.1e}/{:7.1e} b, {:7.1e} v, {:7.1e} v/s"
            .format(
                format_bar(width, fraction, unicode=unicode),
                fraction, int(fraction * 8 ** 64), 8 ** 64,
                visited, visited / (time() - start),
                w=width),
          end="", file=file, flush=True)

def solve(regs, progress=False, unicode=False, progress_interval=50_000,
        width=40):
    """
    Solve a calcudoku in `board`, using regions defined in `regs`, going from
    position "pos".

    Calcudokus are represented as flat lists. It may be tempting to use a 2-D
    array, but really there's nothing inherently two-dimensional about a
    calcudoku, and it's much better to just think of it as a set of tiles, where
    some subsets happen to correspond to regions with some associated rules.
    """
    if progress:
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
            nonlocal visited
            if visited % progress_interval == 0:
                progress_report(fraction, visited, start, unicode, width)
            visited += 1
        if pos == len(board):
            # erase current progress report, because we assume that execution
            # halts while the caller processes the yielded board
            if progress:
                # write a progress report to a mock output to determine the
                # length, because I'm lazy and only want to keep track of a
                # single thing.
                dummy_progress = StringIO()
                progress_report(fraction, visited, start, unicode, width,
                                file=dummy_progress)
                print("\r{}\r".format(" " * len(dummy_progress.getvalue())),
                        end="", file=sys.stderr, flush=True)
            yield board.copy()
            # rewrite progress report when execution resumes.
            if progress:
                progress_report(fraction, visited, start, unicode, width)
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
            progress_report(1, visited, start, unicode, width)
            print("\nTime elapsed: {:.3f}s".format(time() - start),
                    file=sys.stderr)
    # TODO: no hardcode
    yield from _solve([None] * 64, regs, 0, 0, progress)

# a defense mechanism to protect me from myself
if __name__ == "__main__":
    sys.exit("Not a runnable module: see calcudoku.py")
