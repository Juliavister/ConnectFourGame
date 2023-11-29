import numpy as np
import random
import pygame
import sys
import math

#board colors
BLUE = (127, 127, 240)
BLACK = (0, 0, 0)
RED = (240, 128, 128)
YELLOW = (235, 193, 103)

#board parameters
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def create_board(): #creates a 6x7 board for the game
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece): #drops the game piece in the board
	board[row][col] = piece #make it fill the board with whatever piece the player just dropped

def is_valid_location(board, col): #checks if the column is valid, the players choice is passed to this
	return board[ROW_COUNT-1][col] == 0 #location of row and column, if the row is 0, then it is open

def get_next_open_row(board, col): #gets the next open row
	for r in range(ROW_COUNT):
		if board[r][col] == 0: #check board position, if the row is 0, then it is open
			return r  #returns the first instance of an open row

def print_board(board):
	print(np.flip(board, 0)) #numpy command to flip the board, so the pieces drop to the bottom

#Base game function
def winning_move(board, piece):
	#horizontal locations
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	#vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	#positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	#negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window, piece): #evaluate the window and assign a score to it
	score = 0
	opp_piece = PLAYER_PIECE #so equal to 1
	if piece == PLAYER_PIECE: #if the piece is the player piece, then the opponent piece is the AI piece
		opp_piece = AI_PIECE

	#preferences in moves
	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1: #opponent has 3 pieces in a row and there is an empty space, then the AI should block it
		score -= 4

	return score

def score_position(board, piece): #assign the score to the board
	score = 0
	#center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])] #want every row position, but only the center column therefore COLUMN_COUNT//2 -> middle column
	center_count = center_array.count(piece)
	score += center_count * 3 #add 3 points to the score for every piece in the center column

	#Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])] #all the pieces in the row (all the tiles in the row) in an array. ; means  all the column positions for that row, r.
		for c in range(COLUMN_COUNT-3): #to look at the next 4 pieces in the row, a window of 4. -3 because we don't want to go out of bounds and actually look at the last/next 4 pieces
			window = row_array[c:c+WINDOW_LENGTH] #from starting position c, to c+4
			score += evaluate_window(window, piece) #evaluate the window and add the score to the score variable

	#Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])] #same concept as horizontal, but for the columns, get every row pos for a specific column
		for r in range(ROW_COUNT-3): #iterate the window down the column
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	#positive sloped diagonal - from low left to right side
	for r in range(ROW_COUNT-3): #iterate through the rows, cut off the last 3 rows
		for c in range(COLUMN_COUNT-3): #iterate through the columns, cut off the last 3 columns
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)] #[r+i] = row position start 0 and then increase positivly upwards, [c+i] = the same for the columns
			score += evaluate_window(window, piece)

	#negative sloped diagonal - from top and downwards
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)] #[r+3-i] = starting from botton window, + 3 windows to get a correct position from the top to get 4 in a row diagonally
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board): #whenever a game is won, or game is over(pieces used up) - reaches a terminal node
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0
#if its a win, or when the board is full/no more valid moves --> then its a terminal node

#AI function - look down at branches and evaluate the best branch to take using score function
def minimax(board, depth, alpha, beta, maximizingPlayer): #depth- how far we search down, maximizingPlayer - true for AI, false for player when looking at their moves
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board) #checks terminal node

	if depth == 0 or is_terminal:
		if is_terminal: #figure out which of the terminal node cases we are in
			if winning_move(board, AI_PIECE): #if AI wins, then return a high score
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE): #if player wins, then return a low score
				return (None, -10000000000000)
			else: 
				return (None, 0) #game is over, no more valid moves
		else:
			return (None, score_position(board, AI_PIECE)) #if depth is 0, then return the score of the board
		
	if maximizingPlayer: 
		value = -math.inf #initial score to a very low value
		column = random.choice(valid_locations)
		for col in valid_locations: #for each position we can drop 
			row = get_next_open_row(board, col)
			b_copy = board.copy() #to not use the same memeory space
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1] #recursive call. Get the first index to get the score
			if new_score > value: #if the new score is better than the value, then update the value and column
				value = new_score
				column = col
				#implement alpha beta pruning -- allows us to have a deeper depth by eliminating some moves
			alpha = max(alpha, value) #alpha - maximizing player
			if alpha >= beta: #if alpha is greater than or equal to beta, then break out of the loop - no need to look further in the tree
				break
		return column, value

	else: #minimizing player always tries take the lowest value
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1] #true allows us to switch to the maximizing player
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value) #beta - minimizing player
			if alpha >= beta: #if alpha is greater than or equal to beta, then break out of the loop
				break
		return column, value

#AI function
def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col) #append the column to the valid locations list
	return valid_locations

#AI function
def pick_best_move(board, piece): #so that the AI can pick the best move to counterattack the player
	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations) #set an initial value for the best column
	for col in valid_locations: #simulate dropping the piece in the board and pass this to the score position function
		row = get_next_open_row(board, col)
		temp_board = board.copy() #copy the board bc we don't want to change the original board
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score: #if the temp score is better than the best score, then update the best score and best column
			best_score = score
			best_col = col
	return best_col

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

board = create_board() #draws the board
print_board(board)
game_over = False #game is not over yet, to be used in the main game loop

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("Comic Sans MS", 75)

turn = random.randint(PLAYER, AI) #makes the first turn random, either player 1 or player 2


#main game loop
while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION: #detects where the mouse is
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#Player 1 Input
			if turn == PLAYER: # == 0
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE)) #the column where the player wants to drop the piece

				#call the main functions
				if is_valid_location(board, col): #checks if the column is valid
					row = get_next_open_row(board, col) #gets the next open row
					drop_piece(board, row, col, PLAYER_PIECE) #drops the piece in the board

					if winning_move(board, PLAYER_PIECE):
						label = myfont.render("Player 1 wins!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1 #increase this to change the turn
					turn = turn % 2 #alternate between 0 and 1, so player 1 and player 2's turn

					print_board(board)
					draw_board(board)


	#Player 2 Input (AI player)
	if turn == AI and not game_over: # == 1		
		col, minimax_score = minimax(board, 5, -math.inf, math.inf, True) #True bc this is maximizing player

		if is_valid_location(board, col):
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if winning_move(board, AI_PIECE):
				label = myfont.render("AI wins!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1 
			turn = turn % 2 

	if game_over:
		pygame.time.wait(4000)