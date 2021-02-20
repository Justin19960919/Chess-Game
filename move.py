'''
Chieh Lin (Justin) Lee
CS 5001, Fall 2020
This file contains the Move class that represents a move that a piece makes.
It contains functions that interacts with the draw class, and handles making
moves on the board (UI).
'''


from constants import SIZE_OF_SQUARE, RADIUS
from helper import get_coordinates_given_index


class Move:
    '''
        Class -- Move
            Represents a move that a chess piece on the board can make
        Attributes:
            start -- A list [x,y] that represents the where the move starts
                    [x,y] are array indexes for the positions array
            end -- A list [x,y] that represents the where the move ends
                   [x,y] are array indexes for the positions array 
            capture_status -- Indicating if this move is a capture move
                              or not
            RADIUS -- The radius of the chess piece
            SIZE_OF_SQUARE -- The size of a board square
        Methods:
            add_captured_indexes()
            move_chess()
            crown_king()

    '''

    def __init__(self,start,end,capture_status):
        '''
            Constructor -- Creates a new instance of Move
            Parameters:
                self -- The current Move object
        '''
        self.start = start
        self.end = end
        self.capture_status = capture_status
        self.RADIUS = RADIUS
        self.SIZE_OF_SQUARE = SIZE_OF_SQUARE


    def add_captured_indexes(self,capture_x,capture_y):
        '''
            Method -- add_captured_indexes
                Adds the array indexes of the captured piece
                to the move object and assign it to a new 
                attribute self.captured
            Parameters:
                self -- the current Move object
                capture_x -- The x array index of the captured piece
                capture_y -- The y array index of the captured piece
            Returns -- None
        '''
        self.captured = [capture_x, capture_y]

    

    def remove_old_chess(self,draw):
        '''
            Method -- remove_old_chess
                Takes the start point of the Move object,
                and removes it (Covers it up)
            Parameters:
                self -- The current Move object
                draw -- A Draw object, to update UI
            Returns -- None
        '''  
        ## Override the original chess piece with the background (gray or white)
        override_x, override_y = self.start
        override_x_coordinates, override_y_coordinates = get_coordinates_given_index(override_x,override_y)
        print(f"The corner to cover in self.positions is : {override_x},{override_y}")
        # all chesses move on gray square, take this out when refactor
        # fille = self.detect_block_color(override_x,override_y)
        self.cover_old_chess(override_x_coordinates,override_y_coordinates,draw)
        print("Covered the old chess piece....")



    # helper function of remove_old_chess
    def cover_old_chess(self,x,y,draw):
        '''
            Method -- cover_old_chess
                Takes x,y coordinates and use the draw object
                functionalities to draw a black outlined, 
                light gray filled square
            Parameters:
                x -- The x coordinates on the board to start
                y -- The y coordinates on the board to start
                draw -- A Draw object, to update UI
            Returns -- None
        '''  
        draw.set_pen_color_and_fille("black","light gray")
        draw.set_pen_position(x,y)
        draw.draw_square()
        



    def update_new_chess(self,draw,current_player):
        '''
            Method -- update_new_chess
                Takes the end point of the Move object,
                and draw a chess piece based on the 
                color of the current player

            Parameters:
                draw -- A Draw object, to update UI
                current_player -- The current players (a color)
            Returns -- None
        '''  
        new_x, new_y = self.end
        new_x_coordinates, new_y_coordinates = get_coordinates_given_index(new_x,new_y)
        self.draw_new_chess(new_x_coordinates,new_y_coordinates,current_player,draw)


    def draw_new_chess(self,x,y,current_player,draw):
        '''
            Method -- draw_new_chess
                Takes x,y coordinates and use the draw object
                functionalities to draw a checker based on the 
                color of the current player
            Parameters:
                x -- The x coordinates on the board to start
                y -- The y coordinates on the board to start
                current_player -- The current players (a color)
                draw -- A Draw object, to update UI
            Returns -- None
        '''
        draw.set_pen_color(current_player)
        draw.set_pen_position(x + self.RADIUS, y)
        draw.update_checker()
        print("Moved the chess piece to new square....")


    def eliminate_chess_piece(self,draw):        
        '''
            Method -- eliminate_chess_piece
                Takes the captured point of the Move object,
                and let it disappear (cover it)
            Parameters:
                self -- The current move object
                draw -- A Draw object, to update UI
        '''  
        
        eliminate_x, eliminate_y = self.captured
        print("Eliminated x:",eliminate_x,"Eliminated y: ",eliminate_y)
        eliminate_x_coordinates, eliminate_y_coordinates = get_coordinates_given_index(eliminate_x,eliminate_y)
        self.cover_old_chess(eliminate_x_coordinates,eliminate_y_coordinates,draw)
        print("Eliminated an enemy chess piece....")
        


    def move_chess(self,draw,current_player):
        '''
            Method -- move_chess
                Using the move object, and make a move
                using three inner functions: remove_old_chess,
                update_new_chess, and if there is a capture move,
                eliminate_chess_piece()
            Parameters:
                self -- The current move object
                draw -- A Draw object, to update UI
                current_player -- The current player of the game
            Returns -- None
        ''' 

        # remove old
        self.remove_old_chess(draw)
        # draw new
        self.update_new_chess(draw,current_player)
        # if capture_status = True, also remove ememy piece
        if self.capture_status == True:
            # do the capture movement
            self.eliminate_chess_piece(draw)


    def crown_king(self,draw,current_player):
        '''
            Method -- crown_king
                When a chess becone king, we use the draw object
                to add a white circle in the middle, crowning it
                king
            Parameters:
                self -- The current move object
                draw -- A Draw object, to update UI
                current_player -- The current player of the game
            Returns -- None
        ''' 

        end_x, end_y = self.end
        end_x_coordinates, end_y_coordinates = get_coordinates_given_index(end_x,end_y)
        
        # draw a white inner circle inside the checker piece to crown king
        draw.set_pen_color_and_fille("white",current_player)
        draw.set_pen_position(end_x_coordinates + self.RADIUS, end_y_coordinates + 10)
        draw.draw_circle(self.RADIUS - 10)


    def __str__(self):
        output = "Start position: {}. End Position: {}. Capture status: {}".format(self.start,self.end,self.capture_status)
        return output














