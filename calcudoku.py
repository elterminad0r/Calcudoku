"""
Solving calcudokus, as per the README. This part provides the user interface to
the "library" code elsewhere in this repository, and glues it all together.

This is Python 3 code.
"""

import sys
import argparse

# This is mostly because I get confused quite easily, with Arch packaging
# CPython 3 as python, but PyPy 3 as pypy3.
if sys.version_info < (3,):
    sys.exit("Needs Python 3")

from solve import solve
from input_output import parse_board, print_board

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("calcudoku", type=argparse.FileType("r"),
            help="File to read calcudoku from")
    parser.add_argument("-v", "--verbose", action="store_true",
            help="Show progress report")
    return parser.parse_args()

def main():
    """
    Tie it all together
    """
    args = get_args()
    for sol in solve(parse_board(args.calcudoku), progress=args.verbose):
        print_board(sol)

if __name__ == "__main__":
    main()
