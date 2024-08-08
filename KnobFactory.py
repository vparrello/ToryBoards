####
# ToryBoards
# Authored by Tory Parrello 7/4/24
#
# This object holds the creation of the knobs and their randomized settings
# Current settings for the Knob pieces that the factory creates:
#   Knob Pieces:
#       Stem: Has a length and a width for how much of the side length is taken up by the knob
#       Nub: Has a size and shape for how much of the inside of the piece is the nub
#       Begin Co-ord: Where the piece starts
#       End Co-ord: How we know we're done with the knob
#       Side: Concave or convex wiggles to the edges of the knob
#   Settings:
#       Stem:
#           Length: How much of the inside is pushed into
#           Width: How much of the side is the knob
#       Nub:
#           Shape: hex, triangle, square, circle, elipse, penta, octo, septa
#           Shape Area: How much of the piece is stolen
#           length: used in area
#           Width?: used in area
#       Side:
#           Reflect: inside or outside the piece
#           Arc: does the side go concave or convex
#
####

class KnobFactory:

    def __init__(self, side_length, corner_angle):
        self.side_length = side_length
        self.corner_angle = corner_angle
        self.stem = []
        self.nub = []
        self.side = []





