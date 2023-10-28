import math
import sys
import pygame
import numpy as np

ROW_count = 6
COLUMN_count = 7


def create_board():
    board = np.zeros((ROW_count, COLUMN_count))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_location_valid(board, col):
    return board[ROW_count-1][col] == 0


def get_next_free_row(board, col):
    for r in range(ROW_count):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # horizontal win
    for c in range(COLUMN_count-3):
        for r in range(ROW_count):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # vertical win
    for c in range(COLUMN_count):
        for r in range(ROW_count-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # positive sloped diagonal
    for c in range(COLUMN_count-3):
        for r in range(ROW_count-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # negatice sloped diagonal
    for c in range(COLUMN_count-3):
        for r in range(3, ROW_count):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


board = create_board()
game_over = False
turn = 0
