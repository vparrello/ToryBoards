####
# ToryBoards
# Authored by Tory Parrello 7/4/24
#
# This is the Piece object
# Creates a piece with a specific number of sides (currently only 6) that fit the area given. Most pieces will only need 3 sides as they will be taking knobs from the previous pieces.
# Question: How do I know which knobs to grab from the pieces around? grid system? ID by distance from corner?
# Answer: You only create half the pieces with unique knobs (every other but this only works for even numbered pieces). Then you go back and fill in the rest of the puzzle according to the pieces made.
# Looks up that many knobs and their ID numbers to create the piece; insert the length of the knob here to help scale the distance.
####
import Board
import Knob
import math

class Piece:
    def __init__(self, piece_area, piece_id) -> None:
        self.piece_id = piece_id
        self.piece_area = piece_area
        self.knob_margin = 10
        self.knob_list = {
            "Top":"",
            "Bottom":"",
            "TopLeft":"",
            "TopRight":"",
            "BottomLeft":"",
            "BottomRight":""
        }

    def hex_side_calc(self):
        '''Calculates 6 sides of a regular hexagon'''
        side_length = math.sqrt(math.sqrt(3)) * math.sqrt(self.piece_area * 2 / 9)
        return side_length

    def rectangle_side_calc(self):
        '''Calculates 4 sides of a square'''
        side_length = math.sqrt(self.piece_area)
        return side_length

    def margin_security(self, place1, place2):
        # This needs to constrain or populate in the second knob:
        # Radius = stem distance
        # Stem Length
        # Stem Start
        stem_distance1 = self.knob_list[place1].stem[2]
        start_point = self.knob_list[place1].beginning_coord
        circle_center1 = self.knob_list[place1].circle_center
        circle_center2 = self.knob_list[place2].circle_center
        centers_dist = math.sqrt(((circle_center1[0]-circle_center2[0])**2) + ((circle_center1[1]-circle_center2[1])**2))
        # TODO Margin needs to be bigger than 10 pixels
        new_stem_distance = centers_dist - (self.knob_margin + stem_distance1)
        return new_stem_distance

