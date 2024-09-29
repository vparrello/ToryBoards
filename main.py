####
# ToryBoards
# Authored by Tory 7/22/24
#
# This object administers the gui with which the puzzle is created.
# It starts the application
# Name of the file is the database identifier for the puzzle.
# Updates the database with the puzzle name, screenshot, pieces and knob identifiers
####

import PuzzleFactory
import time

# Environment variables
# TODO create arguments asking for number of pieces, piece type (trad, hex, squiggly), and Edge T/F
start = time.time()

#Piece count needs to include an inflation amount for the area on the edge of the board. Either .935 or 1.06 factor
PIECE_COUNT = 500
# Board is 18 inches by 24 inches
X_DIMENSION = 1800
Y_DIMENSION = 2400
# Edge pieces toggle. Currently does nothing
EDGE_YES = True
# DEV true means traditional turtle where Dev False means svg file creation.
DEV = True
# This determines what the file is saved as
BOARD_ID = 12

puzzle = PuzzleFactory.PuzzleFactory(PIECE_COUNT, X_DIMENSION, Y_DIMENSION, EDGE_YES, DEV)
board_data = puzzle.make_puzzle(BOARD_ID)
end = time.time()
print(f'Puzzle {BOARD_ID}.svg has been created after {(end-start)/60} minutes.')
# TODO put board data into a database that holds all pieces, knobs, and board configurations