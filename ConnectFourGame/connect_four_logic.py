import math
import sys
import pygame
import numpy as np
import random

ROW_count = 6
COLUMN_count = 7
WINDOW_LENGTH = 4

Player = 0
AI = 1

PlayerPiece = 1 #Player
AIpiece =  2 #AI
EMPTY = 0


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

    # negative sloped diagonal
    for c in range(COLUMN_count-3):
        for r in range(3, ROW_count):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def is_terminal_node(board):
    return winning_move(board, PlayerPiece) or winning_move(board, AIpiece) or len(is_location_valid(board)) == 0


def evaluate_window(window, piece):
    score = 0
    opp_piece = PlayerPiece
    if piece == PlayerPiece:
        opp_piece = AIpiece
    
    if window.count(piece) == 4:
        score += 100
    
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
    
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN_count//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # horizontal score
    for r in range(ROW_count):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_count-3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # vertical score
    for c in range(COLUMN_count):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_count-3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    
    # positive sloped diagonal score
    for r in range(ROW_count-3):
        for c in range(COLUMN_count-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    
    # negative sloped diagonal score
    for r in range(ROW_count-3):
        for c in range(COLUMN_count-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    
    return score

def get_valid_location(board):
    valid_locations = []
    for col in range(COLUMN_count):
        if is_location_valid(board, col):
            valid_locations.append(col)
    return valid_locations



def MiniMax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_location(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AIpiece):
                return (None, 100000000000000)
            elif winning_move(board, PlayerPiece):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AIpiece))
    
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_free_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AIpiece)
            new_score = MiniMax(b_copy, depth-1, alpha, beta, False)[1]

            if new_score > value:
                value = new_score
                column = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break
            return column, value
    
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_free_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PlayerPiece)
            new_score = MiniMax(b_copy, depth-1, alpha, beta, True)[1]

            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value



board = create_board()
game_over = False
turn = random.randint(PlayerPiece, AIpiece)
