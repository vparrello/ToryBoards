####
# ToryBoards
# Authored by Tory 7/22/24
#
# This object administers the gui with which the puzzle is created.
# It calls the turtle object and draws the outline.
# It then stops the turtle and takes a screenshot. This gets saved with a .jpg extension.
# Name of the file is the database identifier for the puzzle.
# Updates the database with the puzzle name, screenshot, pieces and knob identifiers
# ####

import turtle
import random
import Board
import Piece
import Knob
from turtle import *
import time

# Environment variables
# TODO create arguments asking for number of pieces, piece type (trad, hex, squiggly), and Edge T/F
PIECE_COUNT = 500
# Board is 18 inches by 24 inches
X_DIMENSION = 2400
Y_DIMENSION = 1800
# Edge pieces toggle
EDGE_YES = True
# Piece Type : Traditional, Hexagon, or Squiggly
PIECE_TYPE = "Hexagon"

# Start turtle app
screen = turtle.Screen()
screen.title("ToryBoards")

# Create the size of the screen with 50 pixel buffer.
turtle.setworldcoordinates(0, 0, X_DIMENSION + 50, Y_DIMENSION + 50)

#Initialize Turtle in the top left corner of the screen without drawing.
ziti = turtle.Turtle()
ziti.up()
ziti.setpos(0, Y_DIMENSION)

# Initialize the Board
puzzle = Board.Board(board_id=13, num_of_pieces=PIECE_COUNT, width=X_DIMENSION, height=Y_DIMENSION)
# If EDGE_YES = True, then call the board to create the edges.
if EDGE_YES == True:
    ziti.down()
    puzzle.make_edge(ziti, X_DIMENSION, Y_DIMENSION)
    ziti.up()

#Initialize piece creation
lucky_pieces = Piece.Piece(piece_area=Board.piece_area_calc(), piece_id=13)
if PIECE_TYPE == "Hexagon":
    quintus_knobs = Knob.Knob(side_length=lucky_pieces.hex_side_calc(), corner_angle=60)
    print(f'Piece Area = {lucky_pieces.piece_area}')
    print(f'Side Length: {quintus_knobs.side_length}')
elif PIECE_TYPE == "Rectangle":
    quintus_knobs = Knob.Knob(side_length=lucky_pieces.rectangle_side_calc(), corner_angle=90)
else:
    quintus_knobs = Knob.Knob(side_length=lucky_pieces.rectangle_side_calc(), corner_angle=90)

#TODO Create that number of pieces in the puzzle.
# for i in range(PIECE_COUNT-1):
#   Create a piece, calculate the number of sides, call that many knobs

turtle.done()


