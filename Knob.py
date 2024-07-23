#### 
# ToryBoards
# Authored by Tory Parrello 7/4/24
#
# This object holds the instructions on how to create a knob on a puzzle piece.
# It will take a distance from piece and create a knob inside that distance.
# It will then assign an ID to that knob and record it into a CSV.
# There will also be an edge knob that returns the same knob every time
####
import Piece

class Knob:
    def __init__(self, knob_id, side_length, corner_angle) -> None:
        self.knob_id = knob_id
        self.side_length = side_length
        self.corner_angle = corner_angle

    def draw_side(self, turtle):
        turtle.down()
        turtle.forward(self.side_length)
        turtle.turn
