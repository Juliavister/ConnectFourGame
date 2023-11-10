import pygame
import sys
import math
import random
from connect_four_logic import create_board, drop_piece, is_location_valid, get_next_free_row, winning_move, print_board, board, game_over, turn, Player, AI, PlayerPiece, AIpiece, MiniMax, pick_best_move

pygame.init()

BLUE = (127, 127, 240)
BLACK = (0, 0, 0)
RED = (240, 128, 128)
YELLOW = (235, 193, 103)

ROW_count = 6
COLUMN_count = 7
SQUARESIZE = 100

# function to draw the game board
def draw_board(board):
    for c in range(COLUMN_count):
        for r in range(ROW_count):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r *
                             SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(
                c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_count):
        for r in range(ROW_count):
            if board[r][c] == PlayerPiece:
                pygame.draw.circle(screen, RED, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AIpiece:
                pygame.draw.circle(screen, YELLOW, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
pygame.init() 

width = COLUMN_count * SQUARESIZE
height = (ROW_count+1) * SQUARESIZE

size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()


myfont = pygame.font.SysFont("Comic Sans MS", 75)
turn = random.randint(Player, AI)

# main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == Player:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn == Player: # Player 1 Input
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_location_valid(board, col):
                    row = get_next_free_row(board, col)
                    drop_piece(board, row, col, PlayerPiece)

                    if winning_move(board, PlayerPiece):
                        label = myfont.render("Player 1 wins!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board)

    if turn == AI and not game_over:
        col = random.randint(0, COLUMN_count-1)
        col = pick_best_move(board, AIpiece)
        col, minimax_score = MiniMax(board, 5, -math.inf, math.inf, True)

        if is_location_valid(board, col):
            pygame.time.wait(500)
            row = get_next_free_row(board, col)
            drop_piece(board, row, col, AIpiece)

            if winning_move(board, AIpiece):
                label = myfont.render("AI wins!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2
            
    if game_over:
        pygame.time.wait(3000)
    
