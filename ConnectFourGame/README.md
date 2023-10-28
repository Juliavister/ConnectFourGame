CONNECT FOUR GAME

Objective: The goal of Connect Four is to be the first player to connect four of your discs in a row, either vertically, horizontally, or diagonally on the game board.

Game Board: The game is played on a 6x7 grid, resulting in 42 cells.

Players: Two players take turns: one uses red discs, and the other uses yellow discs.

Gameplay: Players take turns dropping one of their colored discs into any column. The disc falls to the lowest available position within that column.

Winning: A player wins when they create a sequence of four of their discs in a row. They can do this horizontally, vertically, or diagonally.

Draw: If the game board is completely filled, and no player has connected four discs in a row, the game is a draw.

The AI's objective is to make strategic moves to prevent the player from winning while aiming to win itself, and will be implemented with the MiniMax algorithm. 

The algorithm explores all possible future moves for both players (the player and the AI) and assigns scores to each move based on the current game state. The AI (Max) aims to maximize its score, while the player (Min) aims to minimize it. The AI selects moves that lead to higher scores, while the player selects moves that lead to lower scores.

The Minimax algorithm explores a game tree, with each node representing a possible game state after a move. The tree depth is limited to control the AI's search depth and computational complexity.

In Connect Four, the algorithm evaluates game states by considering factors like the number of AI's discs in a row, potential threats from the player, and other strategic elements.

