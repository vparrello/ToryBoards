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
        self.rows = 0
        self.columns = 0

    def piece_area_calc(self):
        '''Calculates Piece Area based on height and width of board'''
        piece_area = self.width * self.height / self.num_of_pieces
        return piece_area

    def column_count(self, knob_side_length):
        self.columns = int(self.width / knob_side_length)
        return self.columns

    def row_count(self, knob_side_length):
         self.rows = int(self.height / knob_side_length)
         return self.rows
