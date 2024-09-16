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
import copy
import Board
import Piece
import Knob
import EdgeKnob
import turtle
# from svg_turtle import SvgTurtle


class PuzzleFactory:

    def __init__(self, piece_count, x_dim, y_dim, edge_bool, dev):
        self.piece_count = piece_count
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.edge_bool = edge_bool
        self.dev = dev # This flag turns on the svg turtle if it is false
        self.pieces = []
        self.knobs = 0

    # Audits number of knobs if I feel like I need it. Currently, not used
    def plus_knob(self):
        self.knobs = self.knobs + 1
        return self.knobs

    def make_puzzle(self, board_id):
        # Initialization of Turtle for svg is different.
        # Therefore, dev true means traditional turtle where Dev False means svg template.
        if not self.dev:
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

        # Initialize piece creation
        # Piece creation happens when the center of a piece is created. 
        piece_area=puzzle.piece_area_calc()

        # Discover "columns" and "rows".
        # Rows draw the horizontal tops and bottoms of the hexagon.
        # Columns draw all left and right sides.

        # Initialized the knob for consistent side length
        side_length=puzzle.hex_side_calc()

        # Grab the current x-position for the turtle
        x_pos = ziti.xcor()

        # Creates a list of columns and their headings so that the turtle can easily iterate through them
        column_addresses = {ziti.pos(): 300}

        #Carries bottom edge for piece initializations
        bottom_edges = []

        # Maintains a list of bottom edge start and end points for knobs
        bottom_edge_knob = []
        for i in range(puzzle.column_count(side_length)):
            x_pos = x_pos + side_length
            if i % 3 == 0:
                ziti.goto(x_pos, self.y_dim)
                bottom_edge_knob = []
            else:
                ziti.goto(x_pos, self.y_dim)
                bottom_edge_knob.append(ziti.pos())
                if i % 3 == 2:
                    new_edge = EdgeKnob.EdgeKnob(side_length, ziti.pos(), ziti.heading(), ziti)
                    bottom_edges.append(new_edge)
                    # Edge has finished drawing
                    column_addresses[ziti.pos()] = 300
                    ziti.up()
                    # Nothing gets drawn. This is a start position for a knob.
                else:
                    # This is now where the beginning of the edge happens
                    column_addresses[ziti.pos()] = 240
                    # Draws the bottom edge of the columns
                    ziti.down()
        ziti.up()
        new_edge = EdgeKnob.EdgeKnob(side_length, ziti.pos(), ziti.heading(), ziti)
        # Initialize the turtle to draw the columns edges.
        ziti.setpos(0, self.y_dim)
        ziti.seth(column_addresses[(0, self.y_dim)])
        # Creates a list of rows that are used to create bottoms, tops, and centers of the pieces.
        # Also draws right edge
        row_addresses = puzzle.draw_column_edge(ziti, new_edge)

        # Attach those knobs to the corresponding center pieces
        last_column = list(column_addresses.keys())[-1]
        ziti.setpos(last_column)
        ziti.seth(column_addresses[last_column])
        # This draws the left edge of the puzzle.
        puzzle.draw_column_edge(ziti, new_edge)
        # At this point we have initialized the bottom and side edges
        # This prints out all of the rows

        for address in row_addresses:
            ziti.up()
            ziti.setpos(address)
            ziti.seth(0)
            if int(ziti.xcor()) == 0:
                counter = 0
            else:
                counter = 2
                # print every third
            while ziti.xcor() < (self.x_dim - side_length):
                if counter % 3 == 0:
                    ziti.forward(side_length)
                elif counter % 3 == 1:
                    # This creates the center of the next row of hexagons
                    if address[1] > side_length/3:
                        new_piece = Piece.Piece(piece_area, ziti.pos())
                        new_piece.knob_list["Bottom"] = bottom_edges[0]
                        bottom_edges.pop(0)
                        self.pieces.append(new_piece)
                    ziti.forward(side_length)
                elif counter % 3 == 2:
                    # This draws only the top 2 edges of the puzzle
                    if ziti.ycor() <= side_length*4/3:
                        new_knob = EdgeKnob.EdgeKnob(side_length, ziti.pos(), ziti.heading(), ziti)
                        new_knob.draw_edge(ziti)
                        new_knob.end_position = ziti.pos()
                        bottom_edges.append(new_knob)
                        self.pieces[0].knob_list["Top"] = new_knob
                        formatted_id = (round(self.pieces[0].piece_id[0], 2), round(self.pieces[0].piece_id[1], 2))
                        puzzle.piece_lookup[formatted_id] = self.pieces[0]
                        self.pieces.pop(0)
                    # This draws the bottom 2 edges of the puzzle
                    elif ziti.ycor() > (self.y_dim - side_length):
                        new_knob = EdgeKnob.EdgeKnob(side_length, ziti.pos(), ziti.heading(), ziti)
                        new_knob.draw_edge(ziti)
                        new_knob.end_position = ziti.pos()
                        bottom_edges.append(new_knob)
                    # This draws the newest bottom/top edge of the puzzle
                    else:
                        new_knob = Knob.Knob(side_length=side_length, corner_angle=60, beginning_coord=ziti.pos(), heading=0)
                        # insert kissy circle here so bottom and top do not touch
                        new_knob.create_knob(ziti)
                        # Insert into the bottom of the piece above
                        self.pieces[0].knob_list["Top"] = new_knob
                        formatted_id = (round(self.pieces[0].piece_id[0], 2), round(self.pieces[0].piece_id[1], 2))
                        puzzle.piece_lookup[formatted_id] = self.pieces[0]
                        self.pieces.pop(0)
                        # Insert into the top of the piece below
                        bottom_edges.append(new_knob)
                        # Insert the piece into piece lookup in Board (puzzle)
                counter += 1

        column_addresses.pop((0, self.y_dim))
        column_addresses.pop(last_column)
        # This creates the columns in which the pieces get created
        for address in column_addresses.keys():
            # TODO This side currently does not populate in the pieces
            ziti.setpos(address)
            new_knob = EdgeKnob.EdgeKnob(side_length, address, column_addresses[address], ziti)
            ziti.setheading(new_knob.heading)
            new_knob.draw_edge(ziti)
            new_knob.end_position = ziti.pos()
            if column_addresses[address] == 240:
                new_knob.turn_turtle(ziti, True)
            else:
                new_knob.turn_turtle(ziti, False)
            for i in range(len(row_addresses)-2):
                new_knob = Knob.Knob(side_length=side_length, corner_angle=60, beginning_coord=ziti.pos(), heading=ziti.heading())
                if ziti.heading() == 300:
                    top_east_piece = puzzle.piece_lookup[(round(new_knob.beginning_coord[0] + side_length, 2), round(new_knob.beginning_coord[1], 2))]
                    bottom_west_piece = puzzle.piece_lookup[(round(new_knob.end_position[0] - side_length, 2), round(new_knob.end_position[1], 2))]
                    # TODO this needs to check against the previous piece as well. Fortunately it is captured in the pieces above
                    # True is up and
                    # This means True Bottom, and west pieces are inside
                    # False is down and left
                    # Falst top and east pieces are inside
                    if new_knob.reflect_flag:
                        new_knob.check_margins(bottom_west_piece.knob_list["Bottom"])
                    else:
                        new_knob.check_margins(top_east_piece.knob_list["Top"])
                    new_knob.create_knob(ziti)

                    bottom_west_piece.knob_list["BottomWest"] = new_knob
                    top_east_piece.knob_list["TopEast"] = new_knob


                else:
                    top_west_piece = puzzle.piece_lookup[
                        (round(new_knob.beginning_coord[0] - side_length, 2), round(new_knob.beginning_coord[1], 2))]
                    bottom_east_piece = puzzle.piece_lookup[
                        (round(new_knob.end_position[0] + side_length, 2), round(new_knob.end_position[1], 2))]

                    if new_knob.reflect_flag:
                        new_knob.check_margins(bottom_east_piece.knob_list["Bottom"])
                    else:
                        new_knob.check_margins(top_west_piece.knob_list["Top"])

                    new_knob.create_knob(ziti)

                    top_west_piece.knob_list["TopWest"] = new_knob
                    bottom_east_piece.knob_list["BottomEast"] = new_knob

            # TODO This also is not populated in the pieces
            new_knob = copy.deepcopy(new_edge)
            new_knob.beginning_coord = ziti.pos()
            new_knob.draw_edge(ziti)

        if not self.dev:
            ziti.save_as(f'{board_id}.svg')
        else:
            screen.exitonclick()
        return puzzle
