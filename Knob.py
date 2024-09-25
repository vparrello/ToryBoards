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
        self.radius = 0
        # Turtle Start position, turtle end position
        self.nub = []
        # First distance, third distance, stem height, start coord, end coord
        self.stem = [self.side_length, 0, 0]
        self.populate_random()

    def populate_random(self):
        # Initialize Stem distances and stem height and end position
        min_stem_0 = max(1, int(0.15 * self.side_length))
        self.stem[0] = random.randint(min_stem_0, int(0.6 * self.side_length))
        stem_leftovers = self.side_length - self.stem[0]
        min_radius = max(1, int(0.15 * stem_leftovers))
        self.radius = random.randint(min_radius, int(0.33 * stem_leftovers))
        self.stem[1] = stem_leftovers - self.radius
        # This is stem height
        min_stem_2 = max(1, int(0.05 * self.side_length))
        self.stem[2] = random.randint(min_stem_2, int(0.30 * self.side_length))

        # Distance to closest edge of the circle
        # (q1 + r1/2 - q2/2 - 7r2/4 -h2*sqrt3/2 + w/2)
        if self.heading == 300:
            self.end_position = ((self.beginning_coord[0] + self.side_length/2), (self.beginning_coord[1] - self.side_length*(math.sqrt(3)/2)))

        elif self.heading == 240:
            self.end_position = ((self.beginning_coord[0] - self.side_length/2), (self.beginning_coord[1] - self.side_length*(math.sqrt(3)/2)))

        else:
            self.end_position = ((self.beginning_coord[0] + self.side_length), self.beginning_coord[1])

        self.reflect_flag = random.choice([True, False])
        if self.reflect_flag:
            self.stem[2] = -abs(self.stem[2])
        else:
            self.stem[2] = abs(self.stem[2])
        return

    def create_knob(self, turtle):
        # insert side distance change here. If Top or Bottom, stem length is random.
        # If BottomSomething, check against bottom of same piece for edges
        # If TopSomething, check against same side bottom and top before allowing entry
        self.draw_side(turtle)
        self.draw_stem(turtle)
        # Down or left
        if self.reflect_flag:
            turtle.right(120)
        # Up or right
        else:
            turtle.goto(self.nub[0])
            turtle.left(60)
            # self.radius = -self.radius
        self.draw_nub(turtle)
        if self.heading == 240:
            self.turn_turtle(turtle, True)
        elif self.heading == 300:
            self.turn_turtle(turtle, False)
        return

    def draw_side(self, turtle):
        # Initialize the first coordinate of the stem
        turtle.down()
        turtle.forward(self.stem[0])
        self.stem.append(turtle.pos())
        # Initialize the second coordinate of the stem
        turtle.up()
        turtle.forward(self.radius)
        self.stem.append(turtle.pos())
        turtle.down()
        # Finish the side to the end coordinate.
        turtle.forward(self.stem[1])
        turtle.up()
        self.end_position = (turtle.pos())
        return

    def draw_stem(self, turtle):
        # This variable determines how long the stem will be for the following knob
        # Initialize the first side of the knob
        turtle.up()
        turtle.goto(self.stem[3])

        turtle.circle(90, 90)  # Quarter-circle turn
        turtle.down()
        turtle.forward(self.stem[2])
        self.nub.append(turtle.pos())
        turtle.up()
        # Initialize the second side of the knob
        turtle.goto(self.stem[4])
        turtle.down()
        turtle.forward(self.stem[2])
        self.nub.append(turtle.pos())
        turtle.up()
        return

    def draw_nub(self, turtle):
        # This variable determines what type of shape the nub is drawn in.
        # Adjust the end of this one to be bigger to get closer to a circle
        nub_sides = random.randint(3, 2000)

        turtle.down()
        turtle.circle(-self.radius, extent=300, steps=nub_sides)
        turtle.up()
        turtle.goto(self.end_position)
        turtle.setheading(self.heading)
        return

    def turn_turtle(self, turtle, reflect):
        corner_angle = 60
        if reflect:
            corner_angle = -corner_angle
        turtle.circle(90, corner_angle)
        return

    def check_margins(self, other_knob):
        self.populate_random()
                
        # Calculate the distance between the two centers
        distance = math.sqrt((self.circle_center[0] - other_knob.circle_center[0])**2 + (self.circle_center[1] - other_knob.circle_center[1])**2)
        
        # Calculate the required distance (sum of radii + margin)
        required_distance = (self.radius + other_knob.radius + 10)  # 10 pixels margin
        
        # If the distance is less than the required distance, re-populate random values
        while distance < required_distance:
            self.populate_random()
            distance = math.sqrt((self.circle_center[0] - other_knob.circle_center[0])**2 + (self.circle_center[1] - other_knob.circle_center[1])**2)
        
        return