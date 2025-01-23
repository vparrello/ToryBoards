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
import EdgeKnob
import turtle
from svg_turtle import SvgTurtle


class PuzzleFactory:

    def __init__(self, piece_count, x_dim, y_dim, edge_bool, dev):
        self.piece_count = piece_count
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.edge_bool = edge_bool
        self.dev = dev # This flag turns on the svg turtle if it is false
        self.pieces = []
        self.knobs = 0
        self.x_start = 0
        self.y_start = 0

    def make_puzzle(self, board_id):
        # Initialization of Turtle for svg is different.
        # Therefore, dev true means traditional turtle where Dev False means svg template.
        if not self.dev:
            ziti = SvgTurtle(self.x_dim * 2, self.y_dim * 2)
        else:
            # Initialize the screen and set how big it is
            screen = turtle.Screen()
            screen.setworldcoordinates(self.x_dim, self.y_dim, 0, 0)
            ziti = turtle.Turtle()
            ziti.speed(0)

        # Initialize the Board
        puzzle = Board.Board(board_id=board_id, num_of_pieces=self.piece_count, width=self.x_dim, height=self.y_dim)

        puzzle.draw_inside_border(ziti)
        self.x_dim, self.y_dim, self.x_start, self.y_start = puzzle.draw_outside_border(ziti)
        # Initialize piece creation
        # Piece creation happens when the center of a piece is created. 
        piece_area=puzzle.piece_area

        # Discover "columns" and "rows".
        # Rows draw the horizontal tops and bottoms of the hexagon.
        # Columns draw all left and right sides.

        # Initialized the knob for consistent side length
        side_length=puzzle.side_length

        # Grab the current x-position for the turtle
        ziti.up()
        ziti.setpos(self.x_start, self.y_dim)
        x_pos = ziti.xcor()

        # Creates a list of columns and their headings so that the turtle can easily iterate through them
        column_addresses = {ziti.pos(): 300}

        #Carries bottom edge for piece initializations
        bottom_edges = []

        # Maintains a list of bottom edge start and end points for knobs
        bottom_edge_knob = []
        puzzle.rows
        for i in range(puzzle.columns - 1):
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
        ziti.setpos(self.x_start, self.y_dim)
        ziti.seth(column_addresses[(self.x_start, self.y_dim)])
        # Creates a list of rows that are used to create bottoms, tops, and centers of the pieces.
        # Also draws right edge
        row_addresses = puzzle.draw_column_edge(ziti, new_edge)
        first_row = row_addresses[0]
        row_addresses.pop(0)
        # Attach those knobs to the corresponding center pieces
        column_list = list(column_addresses.keys())
        ziti.setpos(column_list[-1])
        ziti.seth(column_addresses[(column_list[-1])])
        # This draws the left edge of the puzzle.
        end_column_addresses = puzzle.draw_column_edge(ziti, new_edge)
        last_y = max(row_addresses[-2][1], row_addresses[-1][1])
        last_x = min(end_column_addresses[-2][0], end_column_addresses[-1][0])
        # At this point we have initialized the bottom and side edges
        # This prints out all of the rows
        print("Bottom and side edges created")
        for address in row_addresses:
            print(f"Creating row starting at {address}")
            ziti.up()
            ziti.setpos(address)
            ziti.seth(0)
            if int(ziti.xcor()) == int(self.x_start):
                counter = 0
            else:
                counter = 2
                # print every third
            while ziti.xcor() < last_x:
                if counter % 3 == 0:
                    ziti.forward(side_length)
                elif counter % 3 == 1:
                    # This creates the center of the next row of hexagons
                    if address[1] > side_length/3: #This if skips the first row
                        new_piece = Piece.Piece(piece_area, ziti.pos())
                        new_piece.knob_list["Bottom"] = bottom_edges[0]
                        bottom_edges.pop(0)
                        self.pieces.append(new_piece)
                    ziti.forward(side_length)
                elif counter % 3 == 2:
                    # This draws only the top 2 edges of the puzzle
                    if int(ziti.ycor()) <= int(last_y):
                        new_knob = EdgeKnob.EdgeKnob(side_length, ziti.pos(), ziti.heading(), ziti)
                        new_knob.draw_edge(ziti)
                        new_knob.end_position = ziti.pos()
                        bottom_edges.append(new_knob)
                        self.pieces[0].knob_list["Top"] = new_knob
                        formatted_id = (round(self.pieces[0].piece_id[0], 2), round(self.pieces[0].piece_id[1], 2))
                        puzzle.piece_lookup[formatted_id] = self.pieces[0]
                        self.pieces.pop(0)
                    # This draws the bottom 2 edges of the puzzle
                    elif ziti.ycor() == row_addresses[0][1] or ziti.ycor() == first_row: # This is the first two row_addresses[0][1] and row_addresses[1][1]
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
        print("Rows are completed")
        column_addresses.pop(column_list[0])
        column_addresses.pop(column_list[-1])
        # This creates the columns in which the pieces get created
        print(f"Column Addresses: {column_addresses}")
        for address in column_addresses.keys():
            print(f"Starting column at {address}")
            ziti.setpos(address)
            new_knob = EdgeKnob.EdgeKnob(side_length, address, column_addresses[address], ziti)
            ziti.setheading(new_knob.heading)
            new_knob.draw_edge(ziti)
            new_knob.end_position = ziti.pos()
            if column_addresses[address] == 240:
                #Find the piece that fills a bottom east
                bottom_east_piece = puzzle.piece_lookup[
                    (round(new_knob.end_position[0] + side_length, 2), round(new_knob.end_position[1], 2))]
                bottom_east_piece.knob_list["BottomEast"] = new_knob
                new_knob.turn_turtle(ziti, True)
            else:
                # Piece is the bottom west
                bottom_west_piece = puzzle.piece_lookup[
                    (round(new_knob.end_position[0] - side_length, 2), round(new_knob.end_position[1], 2))]
                bottom_west_piece.knob_list["BottomWest"] = new_knob
                new_knob.turn_turtle(ziti, False)
            for i in range(len(row_addresses)-2):
                new_knob = Knob.Knob(side_length=side_length, corner_angle=60, beginning_coord=ziti.pos(), heading=ziti.heading())
                if ziti.heading() == 300:
                    top_east_piece = puzzle.piece_lookup[(round(new_knob.beginning_coord[0] + side_length, 2), round(new_knob.beginning_coord[1], 2))]
                    bottom_west_piece = puzzle.piece_lookup[(round(new_knob.end_position[0] - side_length, 2), round(new_knob.end_position[1], 2))]
                    if new_knob.reflect_flag:
                        new_knob.check_margins(bottom_west_piece.knob_list["Bottom"], top_east_piece.knob_list["Top"])
                    else:
                        max_radius = new_knob.check_margins(top_east_piece.knob_list["Top"], bottom_west_piece.knob_list["Bottom"])
                        if not top_east_piece.knob_list["BottomEast"].reflect_flag:
                            new_knob.check_margins_column(top_east_piece.knob_list["BottomEast"], max_radius)
                    new_knob.create_knob(ziti)
                    bottom_west_piece.knob_list["BottomWest"] = new_knob
                    top_east_piece.knob_list["TopEast"] = new_knob

                else:
                    top_west_piece = puzzle.piece_lookup[
                        (round(new_knob.beginning_coord[0] - side_length, 2), round(new_knob.beginning_coord[1], 2))]
                    bottom_east_piece = puzzle.piece_lookup[
                        (round(new_knob.end_position[0] + side_length, 2), round(new_knob.end_position[1], 2))]
                    if new_knob.reflect_flag:
                        max_radius = new_knob.check_margins(top_west_piece.knob_list["Top"], bottom_east_piece.knob_list["Bottom"])
                        if top_west_piece.knob_list["BottomWest"].reflect_flag:
                            new_knob.check_margins_column(top_west_piece.knob_list["BottomWest"], max_radius)
                    else:
                        new_knob.check_margins(bottom_east_piece.knob_list["Bottom"], top_west_piece.knob_list["Top"])

                    new_knob.create_knob(ziti)
                    top_west_piece.knob_list["TopWest"] = new_knob
                    bottom_east_piece.knob_list["BottomEast"] = new_knob

            new_knob = EdgeKnob.EdgeKnob(side_length, ziti.pos(), ziti.heading(), ziti)
            if ziti.heading() == 240:
                top_west_piece = puzzle.piece_lookup[
                    (round(new_knob.beginning_coord[0] - side_length, 2), round(new_knob.beginning_coord[1], 2))]
                top_west_piece.knob_list["TopWest"] = new_knob
            else:
                top_east_piece = puzzle.piece_lookup[
                    (round(new_knob.beginning_coord[0] + side_length, 2), round(new_knob.beginning_coord[1], 2))]
                top_east_piece.knob_list["TopEast"] = new_knob
            new_knob.draw_edge(ziti)

        if not self.dev:
            ziti.save_as(f'{board_id}.svg')
        else:
            screen.exitonclick()
        return puzzle
