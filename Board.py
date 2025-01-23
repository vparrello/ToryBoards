####
# ToryBoards
# Authored by Tory 7/4/24
#
# This object creates a virtual "board" for the puzzle to sit on. 
# It uses the width and height to create a perimeter so that we know how big the puzzle is for framing.
# It also calculates how wide and tall each piece is according to the number of pieces and the overall area.
# Calls the piece object to create pieces and store them in a piece lookup
# saves the puzzle and piece dictionary in a CSV file by ID numbers and a picture of the overall pattern by the same name as the ID number.
####
import Piece
import math

class Board:
    def __init__(self, board_id, num_of_pieces, width, height) -> None:
        self.board_id = board_id
        self.num_of_pieces = num_of_pieces
        self.width = width * .99
        self.height = height * .98
        self.start_x = width * .01
        self.start_y = height * .02
        self.piece_lookup = {}
        self.piece_area = self.piece_area_calc()
        self.side_length = self.hex_side_calc()
        self.rows = self.row_count()
        self.columns = self.column_count()

    def draw_inside_border(self, ziti):
        # Creates a border around the 0 dimensions of the puzzle.
        ziti.up()
        ziti.setpos(self.width, self.height)
        ziti.down()
        ziti.goto(self.width-(self.side_length*self.columns), self.height)
        ziti.goto(self.width-(self.side_length*self.columns), self.height-((self.side_length*math.sqrt(3)/2)*self.rows))
        self.start_x = ziti.xcor()
        self.start_y = ziti.ycor()
        ziti.goto(self.width, self.height-((self.side_length*math.sqrt(3)/2)*self.rows))
        ziti.goto(self.width, self.height)
        ziti.up()
        return self.width, self.height, self.start_x, self.start_y
    

    def draw_outside_border(self, ziti):
        # Creates a border around the 0 dimensions of the puzzle.
        ziti.up()
        ziti.setpos(self.width, self.height)
        ziti.down()
        ziti.goto(self.start_x, self.height)
        ziti.goto(self.start_x, self.start_y)
        ziti.goto(self.width, self.start_y)
        ziti.goto(self.width, self.height)
        ziti.up()
        self.start_x = self.start_x + (self.width * .04)
        self.start_y = self.start_y + (self.height * .05)
        self.width = self.width * .96
        self.height = self.height * .95
        return self.width, self.height, self.start_x, self.start_y





    def piece_area_calc(self):
        '''Calculates Piece Area based on height and width of board'''
        piece_area = (self.width * self.height) / self.num_of_pieces
        return piece_area

    def column_count(self):
        sym_width = int(self.width / 3)
        self.columns = int(sym_width / self.side_length) * 3 - 1
        # TODO need to make this always divisible by 3
        print(f"Number of columns: {self.columns}")
        return self.columns

    def row_count(self):
         self.rows = int(self.height / (self.side_length*math.sqrt(3)/2)) + 1
         print(f"Number of rows: {self.rows}")
         return self.rows

    def hex_side_calc(self):
        '''Calculates 6 sides of a regular hexagon'''
        side_length = math.sqrt(math.sqrt(3)) * math.sqrt(self.piece_area * 2 / 9)
        return side_length

    def draw_column_edge(self, ziti, knob):
        row_addresses = []
        row_addresses.append(ziti.pos())
        # Creates a list of rows that are used to create bottoms, tops, and centers of the pieces while creating the right edge
        while ziti.ycor() >= knob.side_length*2:
            knob.draw_edge(ziti)
            if ziti.heading() == 240:
                knob.turn_turtle(ziti, True)
            else:
                knob.turn_turtle(ziti, False)
            row_addresses.append(ziti.pos())
        knob.draw_edge(ziti)
        row_addresses.append(ziti.pos())
        return row_addresses
