from dataclasses import dataclass
from typing import Optional

ROWS = 6
COLUMNS = 7
DEFAULT_WIN_LENGTH = 4

EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2

AXES = [(0,1), (1,0), (1,1), (1,-1)]

Board = list[list[int]]

@dataclass
class MakeMoveResult:
    board: Board
    row: int
    column: int

def create_board() -> Board:
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def deep_board_copy(board: Board) -> Board:
    return [row.copy() for row in board]

def print_board(board: Board):
    for row in board:
        print('|', end='')
        for cell in row:
            print(cell, '|', end='', sep='')
        print('')

def available_moves(board: Board) -> list[int]:
    return [i for i, cell in enumerate(board[0]) if cell == EMPTY]

def winner(make_move_result: MakeMoveResult) -> Optional[int]:
    board = make_move_result.board
    row = make_move_result.row
    column = make_move_result.column
    player = board[row][column]

    if player == EMPTY:
        return None

    for delta_row, delta_column in AXES:
        connected = 1
        connected += _count_consecutive_in_dir(board, row, column, delta_row, delta_column, player)
        connected += _count_consecutive_in_dir(board, row, column, -delta_row, -delta_column, player)

        if connected >= DEFAULT_WIN_LENGTH:
            return player
    
    return None

def _count_consecutive_in_dir(board: Board, row: int, col: int, delta_row: int, delta_column: int, player: int) -> int:
    count = 0
    r = row + delta_row
    c = col + delta_column

    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
        count += 1
        r += delta_row
        c += delta_column

    return count

def is_final(make_move_result: MakeMoveResult) -> bool:
    return winner(make_move_result) is not None or board_is_full(make_move_result.board)

def board_is_full(board: Board) -> bool:
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True

def next_player(board: Board) -> int:
    player1_count = 0
    player2_count = 0

    for row in board:
        for cell in row:
            if cell == PLAYER1:
                player1_count += 1
            elif cell == PLAYER2:
                player2_count += 1
    return PLAYER1 if player1_count == player2_count else PLAYER2

def make_move(board: Board, move: int, player: int) -> MakeMoveResult:
    if not (0 <= move < COLUMNS):
        raise ValueError(f"Invalid column: {move}")
    
    new_board = deep_board_copy(board)

    for row_idx in range(ROWS - 1, -1, -1):
        if new_board[row_idx][move] == EMPTY:
            new_board[row_idx][move] = player
            return MakeMoveResult(new_board, row_idx, move)

    raise ValueError(f"Column {move} is full")