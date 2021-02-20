from constants import NUM_SQUARES, SIZE_OF_SQUARE, BOARD_SIZE, RADIUS


class Draw:
    
    def __init__(self,pen):

        self.pen = pen
        self.NUM_SQUARES = NUM_SQUARES
        self.SIZE_OF_SQUARE = SIZE_OF_SQUARE
        self.BOARD_SIZE = BOARD_SIZE
        self.RADIUS = RADIUS


    def draw_square(self,length = SIZE_OF_SQUARE):

        RIGHT_ANGLE = 90
        NUM_SIDES = 4
        self.pen.begin_fill()
        self.pen.pendown()
        for i in range(NUM_SIDES):
            self.pen.forward(length)
            self.pen.left(RIGHT_ANGLE)
        self.pen.end_fill()
        self.pen.penup()

    def draw_circle(self,radius):
        self.pen.begin_fill()
        self.pen.pendown()
        self.pen.circle(radius)
        self.pen.end_fill()
        self.pen.penup()

    def draw_board(self):
    
        self.pen.color("black", "white")
        corner = - self.BOARD_SIZE / 2
        self.pen.setposition(corner, corner)
        self.draw_square(self.BOARD_SIZE)

    def draw_blocks(self):

        corner = - self.BOARD_SIZE / 2
        self.pen.color("black", "light gray")
        for col in range(self.NUM_SQUARES):
            for row in range(self.NUM_SQUARES):
                if col % 2 != row % 2:
                    self.pen.setposition(corner + self.SIZE_OF_SQUARE * col, corner + self.SIZE_OF_SQUARE * row)
                    self.draw_square(self.SIZE_OF_SQUARE)


    def draw_checkers(self):
        '''
            # Function -- draw checkers
            #     Draw the checkers onto the board. The red checkers are on top,
            #     and the black checkers on the bottom initially.
            # Parameters:
            #     pen -- A turtle instance
            # Returns:
            #     Nothing. Draws the checkers in the checker board.
        '''  
        CHESS_COLORS = ('black','crimson')
        HALF = int(self.NUM_SQUARES/2)
        corner = - self.BOARD_SIZE / 2
     
        for col in  range(self.NUM_SQUARES):
            for row in range(self.NUM_SQUARES):
                
                if row < HALF-1:
                    # draw black
                    self.pen.color(CHESS_COLORS[0],CHESS_COLORS[0])
                    if col % 2 != row % 2:
                        self.set_pen_position(corner + self.RADIUS + self.SIZE_OF_SQUARE * col, corner + self.SIZE_OF_SQUARE * row)
                        self.update_checker()
                
                elif row >= HALF +1:
                    # draw red
                    self.pen.color(CHESS_COLORS[1],CHESS_COLORS[1])
                    if col % 2 != row % 2:
                        self.set_pen_position(corner + self.RADIUS + self.SIZE_OF_SQUARE * col, corner + self.SIZE_OF_SQUARE * row)
                        self.update_checker()  


    def draw_settings(self):
        self.draw_board()
        self.draw_blocks()
        self.draw_checkers()

    def set_pen_color_and_fille(self,outer,inner):
        self.pen.color(outer,inner)


    def set_pen_color(self,color):
        self.pen.color(color)

    def set_pen_position(self,x,y):
        self.pen.goto(x,y)

    # this is drawing the outline
    def draw_square_outline(self):
        RIGHT_ANGLE = 90
        NUM_SIDES = 4
        self.pen.pendown()
        for i in range(NUM_SIDES):
            self.pen.forward(self.SIZE_OF_SQUARE)
            self.pen.left(RIGHT_ANGLE)
        self.pen.penup()

    def update_checker(self):
        self.draw_circle(self.RADIUS)


    def game_winner(self,winner):

        style = ('Courier', 40)
        self.pen.color('deep pink')
        # Game over
        self.set_pen_position(0,100)
        self.pen.write('Game Over!', font=style, align="center")
        #  who wins
        self.set_pen_position(0,0)
        self.pen.write(f"{winner} win(s).", font=style, align="center")









