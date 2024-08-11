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
#       Iterate through a draw side and turn loop until the number of sides is satisfied or the end coordinate is reached.
#
####
import math
import random

class Knob:

    def __init__(self, knob_id, side_length, corner_angle, safe_zone, beginning_coord, heading):
        self.knob_id = knob_id
        self.side_length = side_length
        self.corner_angle = corner_angle
        self.beginning_coord = beginning_coord
        self.safe_zone = safe_zone
        self.end_position = beginning_coord
        self.heading = heading
        self.nub = []
        self.stem = []

    def create_knob(self, turtle):
        self.draw_side(turtle)
        self.draw_stem(turtle)
        self.draw_nub(turtle)

    def draw_side(self, turtle):
        #These variables determine how wide the stem can get.
        stem_start = random.randint(int(.25 * self.side_length), int(.50 * self.side_length))
        stem_end = random.randint(int(.25 * self.side_length), int(.50 * self.side_length))
        side_end = self.side_length - (stem_start + stem_end)
        #Initialize the first coordinate of the stem
        turtle.teleport(self.beginning_coord)
        turtle.down()
        turtle.forward(stem_start)
        self.stem.append(turtle.xcor(), turtle.ycor())
        #Initialize the second coordinate of the stem
        turtle.up()
        turtle.forward(stem_end)
        self.stem.append(turtle.xcor(), turtle.ycor())
        turtle.down()
        # Finish the side to the end coordinate.
        turtle.forward(side_end)
        turtle.up()
        self.end_position = (turtle.xcor(), turtle.ycor())
        self.heading = turtle.heading()
        return

    def draw_stem(self, turtle):
        #This variable determines how long the stem will be for the following knob
        stem_length = random.randint(1, int(self.side_length * .1))
        #Initialize the first side of the knob
        turtle.teleport(self.stem[0])
        turtle.right(90)
        turtle.down()
        turtle.forward(stem_length)
        self.nub.append(turtle.xcor(), turtle.ycor())
        turtle.up()
        #Initialize the second side of the knob
        turtle.teleport(self.stem[1])
        turtle.down()
        turtle.forward(stem_length)
        self.nub.append(turtle.xcor(), turtle.ycor())
        turtle.up()
        return

    def draw_nub(self, turtle):
        #This variable determines what type of shape the nub is drawn in. Adjust the end of this one to be bigger to get closer to a circle
        nub_sides = random.randint(3, 10)
        #This variable grows or shrinks the nub depending on the percentage. Currently it is capped between 10% and 75% of the triangle safe zone
        shape_area = self.safe_zone * random.randint(10, 75) / 100
        # This is how far the turtle will turn to create the shape
        shape_angle = nub_sides - 2 * 180 / nub_sides
        # This is how far the turtle will travel
        shape_side_length = math.sqrt(((self.nub[0][0] - self.nub[1][0])**2)+((self.nub[0][1] - self.nub[1][1])**2))
        # This calculation ensures the shape is within the safe zone
        shape_apothem = shape_side_length / (2 * math.tan((180 / nub_sides) * 3.14159 / 180))
        area_checksum = (nub_sides * shape_side_length * shape_apothem) / 2
        while shape_area <= area_checksum:
            shape_side_length = shape_side_length * .9
        #Initialize the first size of the nub
        turtle.teleport(self.nub[0])
        turtle.left(90)
        turtle.right(shape_angle)
        turtle.down()
        for i in range(nub_sides-1):
            turtle.right(shape_angle)
            turtle.forward(shape_side_length)
            turtle_coords = (turtle.xcor(), turtle.ycor())
        if turtle_coords != self.nub[1]:
            turtle.right(shape_angle)
            turtle.forward(shape_side_length)
        turtle.up()
        turtle.teleport(self.end_position)
        turtle.seth(self.heading)
        return

    def turn_turtle(self, turtle, reflect):
        corner_angle = self.corner_angle
        if reflect == True:
            corner_angle = -self.corner_angle
        turtle.right(corner_angle)
        return



