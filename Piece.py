####
# ToryBoards
# Authored by Tory Parrello 7/4/24
#
# This is the Piece object
# Creates a piece with a specific number of sides (currently up to 4) that fit the area given. Most pieces will only need 2 sides as they will be taking knobs from the previous pieces.
# Question: How do I know which knobs to grab from the pieces around? grid system? ID by distance from corner?
# Answer: You only create half the pieces with unique knobs (every other but this only works for even numbered pieces). Then you go back and fill in the rest of the puzzle according to the pieces made.
# Looks up that many knobs and their ID numbers to create the piece; insert the length of the knob here to help scale the distance.
####
import Board
import Knob

class Piece:
    def __init__(self, piece_area, piece_id, piece_width, piece_hieght, knob_list) -> None:
        self.piece_id = piece_id
        self.piece_area = piece_area
        self.piece_width = piece_width
        self.piece_hieght = piece_hieght
        self.knob_list = knob_list