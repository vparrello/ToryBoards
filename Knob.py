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
#           Shape: hex, triangle, square, circle, ellipse, penta, octo, septa
#           Shape Area: How much of the piece is stolen
#           length: used in area
#           Width?: used in area
#       Side:
#           Reflect: inside or outside the piece
#           Arc: does the side go concave or convex
#
# Creation of the knob happens in three parts
# 1. Draw the side.
#       Turtle starts at beginning coord with pen down
#       Grabs a random number between 25% and 50% of the side length
#       Grabs a second random number between 50% and 75% of the side length
#       pen goes up at first number grab co-ords and heading
#       pen goes down at second number grab co-ords and heading
#       turtle stops at end of side length
# 2. Create the stem
#       Turtle starts at first coord from draw side func
#       Turtle turns 90 degrees and goes forward at a random amount between 0 and height of the hexagon triangle
#       Grab the coordinates for starting point of the nub
#       Turtle teleports to the second coord from draw side func and goes forward the same amount as before
#       Grab the coordinates for the end point of the nub
# 3. Draw the Nub
#       Difference between start and end coordinates are the side length
#       Start at first coord from stem function
#       Create side length and corner angle from the number of sides wanted (between 3-10)
#       Iterate through a draw side and turn loop until the number of sides is satisfied
#       or the end coordinate is reached.
#
####
import math
import random


class Knob:

    def __init__(self, side_length, corner_angle, beginning_coord, heading):
        self.side_length = side_length
        self.corner_angle = corner_angle
        self.beginning_coord = beginning_coord
        self.end_position = beginning_coord
        self.heading = heading
        # Turtle Start position, turtle end position
        self.nub = []
        # Turtle start position, Turtle End position, Stem Length
        self.stem = [self.beginning_coord, self.end_position, 0]
        self.circle_center = None

    def create_knob(self, turtle):
        self.insert_stem_dist()
        #insert side distance change here. If Top or Bottom, stem length is random.
        # If BottomSomething, check against bottom of same piece for edges
        # If TopSomething, check against same side bottom and top before allowing entry
        self.draw_side(turtle)
        reflect_flag = self.draw_stem(turtle)
        self.draw_nub(turtle, reflect_flag)
        return

    def draw_side(self, turtle):
        # These variables determine how wide the stem can get.
        # TODO subtract the stem distance from the side length to determine how much of the side is left
        stem_start = random.randint(int(.1 * self.side_length), int(.33 * self.side_length))
        stem_distance = self.stem[2]
        side_end = self.side_length - (stem_start + stem_distance)
        # Initialize the first coordinate of the stem
        turtle.down()
        turtle.forward(stem_start)
        self.stem[0] = turtle.pos()
        # Initialize the second coordinate of the stem
        turtle.up()
        turtle.forward(stem_distance)
        self.stem[1] = turtle.pos()
        turtle.down()
        # Finish the side to the end coordinate.
        turtle.forward(side_end)
        turtle.up()
        self.end_position = (turtle.pos())
        self.heading = turtle.heading()
        return

    def draw_stem(self, turtle):
        # This variable determines how long the stem will be for the following knob
        stem_length = random.randint(0 , int(.33 * self.side_length))
        reflect_randomizer = random.randint(0, 100)
        if reflect_randomizer % 2 == 0:
            reflect_flag = True
            stem_length = -stem_length
        else:
            reflect_flag = False
        # Initialize the first side of the knob
        turtle.up()
        turtle.goto(self.stem[0])
        turtle.left(90)
        turtle.down()
        turtle.forward(stem_length)
        self.nub.append(turtle.pos())
        turtle.up()
        # Initialize the second side of the knob
        turtle.goto(self.stem[1])
        turtle.down()
        turtle.forward(stem_length)
        self.nub.append(turtle.pos())
        turtle.up()
        return reflect_flag

    def draw_nub(self, turtle, reflect_flag):
        # This variable determines what type of shape the nub is drawn in.
        # Adjust the end of this one to be bigger to get closer to a circle
        nub_sides = random.randint(3, 2000)
        # First turn the turtle towards the center of the circle
        turtle.left(150)
        turtle.forward(self.stem[2])
        self.circle_center = turtle.pos()
        turtle.right(150)
        # Up or right
        if reflect_flag:
            turtle.goto(self.nub[1])
            turtle.right(120)
        # Down or left
        else:
            turtle.goto(self.nub[0])
            turtle.left(60)
        turtle.down()
        turtle.circle(-self.stem[2], extent=300, steps=nub_sides)
        turtle.up()
        turtle.goto(self.end_position)
        turtle.seth(self.heading)
        return

    def turn_turtle(self, turtle, reflect):
        corner_angle = self.corner_angle
        if reflect:
            corner_angle = -self.corner_angle
        turtle.right(corner_angle)
        return

    def draw_edge(self, turtle):
        turtle.down()
        turtle.forward(self.side_length)
        self.stem = [self.beginning_coord, self.end_position, 0]
        turtle.up()
        return

    def insert_stem_dist(self):
        self.stem[2] = random.randint(int(.1 * self.side_length), int(.33 * self.side_length))
        return