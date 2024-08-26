####
# ToryBoards
# Authored by Tory Parrello 7/4/24
#
# This starts by grabbing the beginning point, side length, and heading a piece.
# Then it populates the stem distance, stem length, end coordinate, and circle center. 
# 
#
#
#
#
####

import math
import random


class EdgeKnob:

    def __init__(self, side_length, beginning_coord, heading, turtle):
        self.side_length = side_length
        self.beginning_coord = beginning_coord
        self.heading = heading
        self.circle_center = None
        self.end_position = beginning_coord
    
    def draw_edge(self, turtle):
        turtle.down()
        turtle.forward(self.side_length)
        turtle.up()
        return turtle.pos()
    
    def turn_turtle(self, turtle, reflect):
        corner_angle = 60
        if reflect:
            corner_angle = -corner_angle
        turtle.right(corner_angle)
        return