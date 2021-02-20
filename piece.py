'''
Chieh Lin (Justin) Lee
CS 5001, Fall 2020
This file contains the Piece Class. Each Piece object represents
a chess piece on the board.
'''
class Piece:
    '''
        Class -- Piece
            Represents a piece on the chessboard
        Attributes:
            color -- The color of the chess piece: black/ crimson
            directions -- The directions a piece can move, stored
                          in a nested list
            king_status -- Boolean. If the piece is king, then True,
                           else False
        Methods:
            add_directions()
            turn_to_king()
    '''

    def __init__(self,color,directions,king_status):
        '''
            Constructor -- Creates a new instance of Piece
            Parameters:
                color -- The color of the chess piece
                directions -- The directions this piece can go,
                a nested array
                king_status -- Boolean. If the piece is king,
                then True, else False

        '''
        self.color = color
        self.directions = directions
        self.king_status = king_status


    def add_directions(self,up_left,up_right,down_left,down_right):
        '''
            Method -- add_directions
                When a piece turns to king, adds directions to 
                self.directions based on the color of the chess
                piece
            Parameters:
                self -- the current Move object
                capture_x -- The x array index of the captured piece
                capture_y -- The y array index of the captured piece 
        '''
        if self.color == "black":
            self.directions += [down_left,down_right]
        elif self.color == "crimson":
            self.directions += [up_left,up_right]

    def turn_to_king(self):
        self.king_status = True


    def __str__(self):
        output = "Chess piece: Color: {}, Directions: {}, King status: {}".format(self.color,self.directions, self.king_status)
        return output



