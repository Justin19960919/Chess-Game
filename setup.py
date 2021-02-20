'''
Sample Code
CS 5001, Fall 2020 - Lecture 12
This file handles the setup of the boardgame, including
initiating Gamestate which controls the chess pieces to
be moved upon, and Draw which handles the updating UI.

'''

# import constants
from constants import NUM_SQUARES, SIZE_OF_SQUARE, BOARD_SIZE, RADIUS

# self defined classes
from draw import Draw
from gamestate import Gamestate

# turtle
import turtle

# NUM_SQUARES -- The number of squares in a 
# column or row
# SIZE_OF_SQUARE -- The size of a board square
# BOARD_SIZE -- The board length
# RADIUS -- The radius of the chess piece

class Setup:

    '''
        Class -- Setup
            Setups the board game
        Attributes:
            pen -- A turtle instance
            window_size -- The length of the window
            boundaries -- The boundaries of the board
        
        Methods:
            setup() -- Setting up the whole game, which 
            includes drawing the board, drawing the checkers,
            initiating gamestate and Draw for UI.
            click_handler() -- The function that gets call
            when the user clicks on the window

    '''

    def __init__(self):
        '''
            Constructor -- Creates a new instance of Setup
            Parameters:
                self -- The current Setup object
        '''
        self.pen = turtle.Turtle()
        self.window_size = BOARD_SIZE + SIZE_OF_SQUARE
        self.boundaries = (-BOARD_SIZE/2, BOARD_SIZE/2) 
        # setup board
        self.setup()

    def setup(self):

        # Create the UI window. This should be the width of the board plus a little margin
        # The extra + SQUARE is the margin
        turtle.setup(self.window_size, self.window_size)

        # Set the drawing canvas size. The should be actual board size
        turtle.screensize(BOARD_SIZE, BOARD_SIZE)
        turtle.bgcolor("white") # The window's background color
        turtle.tracer(0, 0) # makes the drawing appear immediately
        
        self.pen.penup() # This allows the pen to be moved.
        self.pen.hideturtle() # This gets rid of the triangle cursor.
        
        self.background = Draw(self.pen)    
        self.background.draw_settings()
        self.screen = turtle.Screen()

        self.gamestate = Gamestate()
        self.update = Draw(self.pen)
        
        # This is a continuous while loop
        self.screen.onclick(self.click_handler)

        turtle.done()


    def click_handler(self,x,y):

        print("Clicked at ", x, y)
        
        if x < self.boundaries[0] or x > self.boundaries[1] or y < self.boundaries[0] or y > self.boundaries[1]:
            print("Out of bounds")
        
        else:
            print("-------- Clicked ----------")
            self.gamestate.process(x,y,self.update)
            
            print("Tracker arrays: ")
            self.gamestate.print_tracker_arrays()

            print("Positions array: ")
            self.gamestate.print_positions_array()
    





