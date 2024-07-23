####
# ToryBoards
# Authored by Tory 7/4/24
#
# This object creates a virtual "board" for the puzzle to sit on. 
# It uses the width and height to create a perimeter so that we know how big the puzzle is for framing.
# It also calculates how wide and tall each piece is according to the number of pieces and the overall area.
# Calls the piece object to create pieces and store them in a piece lookup
# saves the puzzle and piece dictionary in a CSV file by ID numbers and a picture of the overall pattern by the same name as the ID number.
####
import Piece
import math

class Board:
    def __init__(self, board_id, num_of_pieces, width, height) -> None:
        self.board_id = board_id
        self.num_of_pieces = num_of_pieces
        self.width = width
        self.height = height
        self.piece_lookup = {}

    def make_edge(self, turtle_object, x_dimension, y_dimension):
        '''Used to create the edge of a puzzle according to rectangular dimensions'''
        turtle_object.forward(x_dimension)
        turtle_object.right(90)
        turtle_object.forward(y_dimension)
        turtle_object.right(90)
        turtle_object.forward(x_dimension)
        turtle_object.right(90)
        turtle_object.forward(y_dimension)
        turtle_object.right(90)
        return

    def piece_area_calc(self):
        '''Calculates Hexagon Piece Area based on height and width of board'''
        piece_area = self.width * self.height / self.num_of_pieces
        return piece_area
        