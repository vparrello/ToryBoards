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


    # Start turtle app
    # ziti = SvgTurtle(X_DIMENSION*2, Y_DIMENSION*2)
    # Create the size of the screen with 50 pixel buffer.
    # ziti._Screen.setup(ziti, width=X_DIMENSION+50, height=Y_DIMENSION+50, startx=0, starty=X_DIMENSION)
    def make_puzzle(self):
        screen = turtle.Screen()
        screen.setworldcoordinates(self.x_dim+50, self.y_dim+50, 0, 0)
        #Initialize Turtle in the top left corner of the screen without drawing.
        if self.dev == False:
            ziti = SvgTurtle(self.x_dim * 2 + 50, self.y_dim * 2 + 50)
        else:
            ziti = turtle.Turtle()
            ziti.speed(0)
            ziti.hideturtle()
        ziti.up()
        ziti.setpos(0, self.y_dim)
        all_turtles = []

        # Initialize the Board
        puzzle = Board.Board(board_id=13, num_of_pieces=self.piece_count, width=self.x_dim, height=self.y_dim)
        # If EDGE_YES = True, then call the board to create the edges.
        if self.edge_bool == True:
            ziti.down()
            if self.piece_type == "Rectangle":
                puzzle.make_square_edge(ziti, self.x_dim, self.y_dim)
            elif self.piece_type == "Hexagon":
                puzzle.make_hex_edge(ziti, self.x_dim, self.y_dim)
            ziti.up()
        #Turtle should now be facing south?
        ziti.right(60)

        #Initialize piece creation
        template_piece = Piece.Piece(piece_area=puzzle.piece_area_calc(), piece_id=13)
        # Discover "columns" and "rows". For the purposes of the calculation, we are counting equilateral triangles.
        if self.piece_type == "Hexagon":
            #Initialized the knob and side length
            initial_knob = Knob.Knob(side_length=template_piece.hex_side_calc(), corner_angle=60, knob_id=13, safe_zone=template_piece.piece_area/6, beginning_coord=(ziti.xcor(), ziti.ycor()), heading=ziti.heading())
            #Grab the current xposition for the turtle
            x_pos = ziti.xcor()
            #Add initial turtle to the list
            all_turtles.append(ziti)
            row_addresses = [(0, self.y_dim)]
            for i in range(puzzle.column_count(initial_knob.side_length)):
                x_pos = x_pos + initial_knob.side_length
                if not i % 3 == 0:
                    new_turtle = ziti.clone()
                    new_turtle.speed(0)
                    new_turtle.penup()
                    new_turtle.teleport(x_pos, self.y_dim)
                    # print(new_turtle.pos())
                    if i % 3 == 2:
                        new_turtle.seth(300)
                    else:
                        new_turtle.seth(240)
                    all_turtles.append(new_turtle)

            for i in range(len(all_turtles)):
                if i == 0:
                    while all_turtles[i].ycor() >= initial_knob.side_length:
                        initial_knob.create_knob(all_turtles[i])
                        initial_knob.turn_turtle(all_turtles[i], False)
                        position_tuple = (int(all_turtles[i].xcor()), int(all_turtles[i].ycor()))
                        row_addresses.append(position_tuple)
                        initial_knob.create_knob(all_turtles[i])
                        initial_knob.turn_turtle(all_turtles[i], True)
                        position_tuple = (int(all_turtles[i].xcor()), int(all_turtles[i].ycor()))
                        row_addresses.append(position_tuple)
                    print(f"Row addresses: {row_addresses}")
                elif i % 2 == 0:
                    while all_turtles[i].ycor() >= initial_knob.side_length:
                        initial_knob.create_knob(all_turtles[i])
                        initial_knob.turn_turtle(all_turtles[i], False)
                        initial_knob.create_knob(all_turtles[i])
                        initial_knob.turn_turtle(all_turtles[i], True)
                else:
                    while all_turtles[i].ycor() >= initial_knob.side_length:
                        initial_knob.create_knob(all_turtles[i])
                        initial_knob.turn_turtle(all_turtles[i], True)
                        initial_knob.create_knob(all_turtles[i])
                        initial_knob.turn_turtle(all_turtles[i], False)
            for address in row_addresses:
                ziti.up()
                ziti.setpos(address[0], address[1])
                ziti.seth(0)
                counter = 0
                if ziti.xcor() == 0:
                    while ziti.xcor() <= (self.x_dim - initial_knob.side_length):
                        #print every third to keep away from trapezoids
                        if counter % 3 == 2:
                            initial_knob.create_knob(ziti)
                        else:
                            ziti.forward(initial_knob.side_length)
                        counter += 1
                else:
                    #Print one and skip two
                    while ziti.xcor() <= (self.x_dim - initial_knob.side_length):
                        if counter % 3 == 0:
                            initial_knob.create_knob(ziti)
                        else:
                            ziti.forward(initial_knob.side_length)
                        counter += 1
        else:
            initial_knob = Knob.Knob(side_length=template_piece.hex_side_calc(), corner_angle=60, knob_id=13, safe_zone=template_piece.piece_area/4, beginning_coord=ziti.pos(), heading=ziti.heading())
        if self.dev == False:
            ziti.save_as('templatesmall.svg')
        return ziti