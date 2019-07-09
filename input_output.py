"""
Input and output related code
"""

import sys

from regions import REG_MAP, COLUMNS, ROWS

# str.format compatible template to format a calcudoku board
board_temp = ("{} " * 8 + "\n") * 8

def read_regions(in_file, regs):
    """
    Read region definitions from a calcudoku specification file. See ex.txt for
    an example.

    The first section of this file should consist of a name assigment for each
    region to be used on each line. Each definition should have the form
    X=n T
    where X is the name of the group, n is the target number, T is the type of
    operation.

    This section is terminated by the line "START".

    This creates entries in a mapping `regs` to store regions in. `regs` is a
    dictionary of tuples of Region types, targets, and lists of squares, later
    to be compiled into Regions.
    """
    for line in in_file:
        if line == "START\n":
            break
        reg_name, reg_desc = line.strip().split("=")
        reg_targ, reg_type = reg_desc.split()
        regs[reg_name] = (REG_MAP[reg_type], int(reg_targ), [])
    else:
        sys.exit("Invalid input file: no START")
    return regs

def read_board(in_file, regs):
    """
    Read a board from an input file, appending to `regs`. See `ex.txt`, again.
    Basically, expects to read 64 whitespace-separated symbols from the file.
    """
    for ind, sym in enumerate(sym for line in in_file
                                  for sym in line.split()):
        regs[sym][2].append(ind)

def build_regions(regs):
    """
    Compile the Regions read from a calcudoku file.
    """
    return ([Reg(target, positions) for Reg, target, positions in regs.values()]
           + ROWS
           + COLUMNS)

def invert_regions(regs):
    """
    Build an inverse lookup for regions, so that to determine which region a
    square is a member of, we just do an O(1) lookup.
    """
    inv = [[] for _ in range(64)]
    for r in regs:
        for p in r.positions:
            inv[p].append(r)
    return inv

def parse_board(in_file):
    """
    Parse a whole input file, returning a mapping from tiles to regions, like
    solve() wants.
    """
    regs = {}
    read_regions(in_file, regs)
    read_board(in_file, regs)
    return invert_regions(build_regions(regs))


def print_board(board):
    """
    print_board
    """
    print(board_temp.format(*board))

# a defense mechanism to protect me from myself
if __name__ == "__main__":
    sys.exit("Not a runnable module: see calcudoku.py")
