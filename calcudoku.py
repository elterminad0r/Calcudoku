"""
Solving calcudokus, as per the README.

This part provides the user interface to the "library" code elsewhere in this
repository, and glues it all together.

This is Python 3 code.
"""

import sys
import argparse

# This is mostly because I get confused quite easily, with Arch packaging
# CPython 3 as python, but PyPy 3 as pypy3.
if sys.version_info < (3,):
    sys.exit("Needs Python 3, not\n\"{}\"".format(sys.version))

from backtrack import solve
from input_output import parse_board, print_board

def get_args():
    parser = argparse.ArgumentParser(
            # just take the first paragraph of __doc__, because I can't be asked
            # to ship this with smartparse.py
            description=__doc__.split("\n\n")[0],
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("calcudoku", type=argparse.FileType("r"),
            help="File to read calcudoku from")
    parser.add_argument("-v", "--verbose", action="store_true",
            help="Show progress report")
    parser.add_argument("-a", "--ascii", action="store_true",
            help="Use just ASCII characters for the progress report")
    parser.add_argument("-w", "--width", type=int, default=40,
            help="Width of the progress bar")
    parser.add_argument("-i", "--interval", type=int, default=50_000,
            help="Progress interval - number of board to process between each "
                 "update")
    return parser.parse_args()

def main():
    """
    Tie it all together
    """
    args = get_args()
    for sol in solve(parse_board(args.calcudoku), progress=args.verbose,
                     unicode=not args.ascii, progress_interval=args.interval,
                     width=args.width):
        print_board(sol)

if __name__ == "__main__":
    main()
