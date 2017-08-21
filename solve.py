def solve(board, regs, pos=0):
    if pos == 64:
        yield board
    else:
        for i in range(8):
            board[pos] = i
            if all(r.isvalid(board) for r in regs[pos]):
                yield from solve(board, regs, pos + 1)
