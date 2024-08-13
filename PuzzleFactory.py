####
# ToryBoards
# Authored by Tory Parrello 7/25/24
#
# This object takes the knobs, pieces and board and creates a puzzle with that information.
# It uses the Board to create the edge and calculate the piece area
# It takes that piece and calculates columns and rows.
# Then it draws the pieces side by side first by columns and then by rows
#
####

import Board
import Piece
import Knob
import turtle
from svg_turtle import SvgTurtle

class PuzzleFactory:

    def __init__(self, piece_count, x_dim, y_dim, edge_bool, piece_type, DEV):
        self.piece_count = piece_count
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.edge_bool = edge_bool
        self.piece_type = piece_type
        self.dev = DEV
        self.pieces = 0
        self.knobs = 0

    def plus_piece(self):
        self.pieces = self.pieces+1
        return self.pieces

    def plus_knob(self):
        self.knobs = self.knobs+1
        return self.knobs

    # Start turtle app
    # ziti = SvgTurtle(X_DIMENSION*2, Y_DIMENSION*2)
    # Create the size of the screen with 50 pixel buffer.
    # ziti._Screen.setup(ziti, width=X_DIMENSION+50, height=Y_DIMENSION+50, startx=0, starty=X_DIMENSION)
    def make_puzzle(self, board_id):

        #Initialize Turtle for svg is different for a dev drawing
        if self.dev == False:
            ziti = SvgTurtle(self.x_dim * 2 + 50, self.y_dim * 2 + 50)
        else:
            # Initialize the screen and set how big it is
            screen = turtle.Screen()
            screen.setworldcoordinates(self.x_dim + 50, self.y_dim + 50, 0, 0)
            ziti = turtle.Turtle()
            ziti.speed(0)
        ziti.up()
        ziti.setpos(0, self.y_dim)

        # Initialize the Board
        puzzle = Board.Board(board_id=board_id, num_of_pieces=self.piece_count, width=self.x_dim, height=self.y_dim)
        #Initialize piece creation
        template_piece = Piece.Piece(piece_area=puzzle.piece_area_calc(), piece_id=self.plus_piece())
        # Discover "columns" and "rows". For the purposes of the calculation, we are counting equilateral triangles.
        #Initialized the knob and side length
        initial_knob = Knob.Knob(side_length=template_piece.hex_side_calc(), corner_angle=60, knob_id=self.plus_knob(), safe_zone=template_piece.piece_area/6, beginning_coord=(ziti.xcor(), ziti.ycor()), heading=ziti.heading())
        #Grab the current xposition for the turtle
        x_pos = ziti.xcor()

        #Creates a list of columns and their headings so that the turtle can easily iterate through them
        column_addresses = {(0, self.y_dim): 300}
        for i in range(puzzle.column_count(initial_knob.side_length)):
            x_pos = x_pos + initial_knob.side_length
            if not i % 3 == 0:
                ziti.goto(x_pos, self.y_dim)
                # add drawing an edge to this point of the process on the non piece center columns
                if i % 3 == 2:
                    column_addresses[ziti.pos()] = 300
                    ziti.up()
                else:
                    column_addresses[ziti.pos()] = 240
                    #Draws the bottom edge of the columns
                    ziti.down()
        ziti.up()
        print(column_addresses)

        row_addresses = []
        ziti.setpos(0, self.y_dim)
        ziti.seth(column_addresses[(0, self.y_dim)])
        #Creates a list of rows that are used to create bottoms, tops, and centers of the pieces while creating the right edge
        while ziti.ycor() >= initial_knob.side_length:
            initial_knob.draw_edge(ziti)
            initial_knob.turn_turtle(ziti, False)
            row_addresses.append(ziti.pos())
            initial_knob.draw_edge(ziti)
            initial_knob.turn_turtle(ziti, True)
            row_addresses.append(ziti.pos())

        #This draws the left edge of the puzzle. Refactor this to only need to go to the last item in the column addresses.keys list
        for address in column_addresses.keys():
            if address[0] > (self.x_dim - initial_knob.side_length):
                ziti.setpos(address)
                ziti.seth(column_addresses[address])
                while ziti.ycor() >= initial_knob.side_length:
                    initial_knob.draw_edge(ziti)
                    initial_knob.turn_turtle(ziti, True)
                    initial_knob.draw_edge(ziti)
                    initial_knob.turn_turtle(ziti, False)
                print(f"Row addresses: {row_addresses}")

        piece_centers = []
        #At this point we have initialized the bottom and right edges. We need to switch to the horizontal edges and then move on to the columns.
        for address in row_addresses:
            ziti.up()
            ziti.setpos(address)
            ziti.seth(0)
            counter = 0
            if int(ziti.xcor()) == 0:
                # print every third to keep away from trapezoids
                while ziti.xcor() <= (self.x_dim - initial_knob.side_length):
                    if counter % 3 == 2:
                        if ziti.ycor() <= initial_knob.side_length or ziti.ycor() > (self.y_dim - initial_knob.side_length):
                            initial_knob.draw_edge(ziti)
                        else:
                            initial_knob.create_knob(ziti)
                    elif counter % 3 == 1:
                        piece_centers.append(ziti.pos())
                        ziti.forward(initial_knob.side_length)
                    else:
                        ziti.forward(initial_knob.side_length)
                    counter += 1
            else:
                #Print one and skip two
                while ziti.xcor() <= (self.x_dim - initial_knob.side_length):
                    if counter % 3 == 0:
                        if ziti.ycor() < (initial_knob.side_length*2) or ziti.ycor() > (self.y_dim - initial_knob.side_length):
                            initial_knob.draw_edge(ziti)
                        else:
                            initial_knob.create_knob(ziti)
                    elif counter % 3 == 2:
                        piece_centers.append(ziti.pos())
                        ziti.forward(initial_knob.side_length)
                    else:
                        ziti.forward(initial_knob.side_length)
                    counter += 1
        print(len(piece_centers))
        last_column_address = list(column_addresses)[-1]
        column_addresses.pop((0, self.y_dim))
        column_addresses.pop(last_column_address)
        #This creates the columns in which the pieces get created
        for address in column_addresses.keys():
            ziti.setpos(address)
            ziti.seth(column_addresses[address])
            initial_knob.draw_edge(ziti)
            while ziti.ycor() >= (initial_knob.side_length*2):
                if ziti.heading() == 300:
                    initial_knob.turn_turtle(ziti, False)
                    initial_knob.create_knob(ziti)
                else:
                    initial_knob.turn_turtle(ziti, True)
                    initial_knob.create_knob(ziti)
            if ziti.heading() == 300:
                initial_knob.turn_turtle(ziti, False)
            else:
                initial_knob.turn_turtle(ziti, True)
            initial_knob.draw_edge(ziti)
        if self.dev == False:
            ziti.save_as('templatesmall.svg')
        else:
            screen.exitonclick()
        return ziti