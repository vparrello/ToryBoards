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

# Environment variables
# TODO create arguments asking for number of pieces, piece type (trad, hex, squiggly), and Edge T/F

#Piece count needs to include an inflation amount for the area on the edge of the board. Either .935 or 1.06 factor
PIECE_COUNT = 200
# Board is 18 inches by 24 inches
X_DIMENSION = 2400
Y_DIMENSION = 1800
# Edge pieces toggle
EDGE_YES = True
# Piece Type : Traditional, Hexagon, or Squiggly
PIECE_TYPE = "Hexagon"
DEV = True

puzzle = PuzzleFactory.PuzzleFactory(PIECE_COUNT, X_DIMENSION, Y_DIMENSION, EDGE_YES, PIECE_TYPE, DEV)
turtle = puzzle.make_puzzle(13)