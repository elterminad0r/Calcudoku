import sys
import argparse

from functools import partial

from regions import PlusRegion, MinusRegion, TimesRegion, DivideRegion, RowRegion, ColumnRegion
from solve import solve

REG_MAP = dict(zip("+-*/", [PlusRegion, MinusRegion, TimesRegion, DivideRegion]))
COLUMNS = [ColumnRegion(i) for i in range(8)]
ROWS = [RowRegion(i) for i in range(8)]

board_temp = ("{} " * 8 + "\n") * 8

def read_regions(in_file, regs):
    for line in iter(in_file.readline, "START\n"):
        reg_name, reg_desc = line.strip().split("=")
        reg_targ, reg_type = reg_desc.split()
        regs[reg_name] = (REG_MAP[reg_type], int(reg_targ), [])
    return regs

def read_board(in_file, regs):
    for ind, token in enumerate(iter(partial(in_file.read, 2), "")):
        sym = token[0]
        regs[sym][2].append(ind)

def build_regions(regs):
    return [Reg(target, positions) for Reg, target, positions in regs.values()] + ROWS + COLUMNS

def invert_regions(regs):
    inv = [[] for _ in range(64)]
    for r in regs:
        for p in r.positions:
            inv[p].append(r)
    return inv

def print_board(board):
    print(board_temp.format(*board))

def solve(board, regs, pos=0):
    #print_board(board)
    if pos == 64:
        yield board
    else:
        for i in range(1, 9):
            #print(i)
            board[pos] = i
            if all(r.isvalid(board) for r in regs[pos]):
                yield from solve(board, regs, pos + 1)
        board[pos] = None

def main():
    board = [None for _ in range(64)]
    regs = {}
    read_regions(sys.stdin, regs)
    read_board(sys.stdin, regs)
    lregs = invert_regions(build_regions(regs))
    #list(map(print, enumerate(lregs)))
    for sol in solve(board, lregs):
        print_board(sol)


if __name__ == "__main__":
    main()
