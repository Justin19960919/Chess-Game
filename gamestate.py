'''
Chieh Lin (Justin) Lee
CS 5001, Fall 2020
This file contains the Gamestate class that handles all the logic
and UI updating of this board game.
'''


# import constants
from constants import NUM_SQUARES,SIZE_OF_SQUARE,up_left,up_right,down_left,down_right
# import helper function
from helper import get_coordinates_given_index

# import classes
from piece import Piece
from move import Move

# import modules
import random
import turtle

class Gamestate:

    '''
        Class -- Gamestate
            The gamestate class handles all the logic, including taking turns,
            updating chess pieces and the UI, and when the game ends etc.
        Attributes:
            pen -- A turtle instance
            screen -- turtle.screen() ; used for delays
            current_player -- The current player of the gamestate
            positions -- The positions array
            clicked_coordinates_array_index -- A tracker array for tracking
                        what x,y coordinates the player clicked
            clicked_pattern -- A tracker array for tracking what the pattern
                        the player clicked (EX: black, empty, ...)
            history_possible_routes -- A tracker array for remembering what 
                        the possible routes for this step
            eliminated_a_piece -- Boolean, did we eliminate a piece yet?
                        If yes, we need to check for multiple captures
            game_end -- Boolean, by default is False, if game ends,
                        then we declare who wins on the screen, and end the game
        
        Methods:
            make_positions_array()
            get_cell()
            identify_corner()
            find_other_player()
            check_boundaries()
            find_all_moves()
            check_end_game()
            check_any_moves_left()
            check_capture()
            modify_arrays()
            update_array_when_move()
            get_multi_capture_moves()
            find_move()
            random_selection()
    '''
    # Arrays
    clicked_coordinates_array_index = [] 
    clicked_pattern = []
    history_possible_routes =[]
    
    # Conditionals
    eliminated_a_piece = False
    game_end = False
    pen = turtle.Turtle()
    screen = turtle.Screen()

    def __init__(self,current_player = "black"):
        '''
            Constructor -- Creates a new instance of gamestate
            Parameters:
                #pen -- A turtle instance
                #screen -- turtle.screen() ; used for delays
                current_player -- The current player of the gamestate
                positions -- The positions array
        '''
        # self.pen = pen
        # self.screen = screen
        self.current_player = current_player
        self.positions = self.make_positions_array()


    def make_positions_array(self):
        '''
            Method -- make_positions_array
                Make the positions array
            Parameters:
                self -- the current Gamestate object
            Returns -- The positions array
        '''
        half = int(NUM_SQUARES / 2)
        positions = []
        for row in range(NUM_SQUARES):
            row_array = []
            for col in range(NUM_SQUARES):
                if row < half - 1:
                    if row%2 == col%2:
                        row_array.append(Piece("crimson",directions= [down_left, down_right], king_status = False))
                    else:
                        row_array.append("empty")
                
                elif row >= half -1 and row <= half:
                    row_array.append("empty")
                
                elif row > half:
                    if row%2 == col%2:
                        row_array.append(Piece("black",directions= [up_left, up_right], king_status = False))
                    else:
                        row_array.append("empty")
            positions.append(row_array)
        
        return positions

    
    ################  Identify corner  ####################
    def find_array_index(self,x,y):
        '''
        Given the chess board boxes, we find the array indexes in the self.positions array
        to find out the color
        '''
        CORRECTION_Y = 7
        return (abs(y - CORRECTION_Y), x)


    def get_cell(self,val):
        '''
            Method -- get_cell
                Converts a click coordinate to a cell location.
            Parameters:
                self -- the current Gamestate object
                val -- the click location (x or y)
            Returns:
                The index of the cell that was clicked. Works for row and col.
        '''
        high_bound = SIZE_OF_SQUARE * NUM_SQUARES/2
        low_bound = 0 - high_bound
        scaled = val - low_bound
        return int(scaled // SIZE_OF_SQUARE)


    def identify_corner(self,x,y):
        '''
            Method -- identify_corner
                Identifies the array index of the x,y coordinates for the click
            Parameters:
                self -- the current Gamestate object
                x -- The x coordinate
                y -- The u coordinate
            Returns:
                None.
        '''
        x = self.get_cell(x)
        y = self.get_cell(y)
        self.x_array_index = self.find_array_index(x,y)[0]
        self.y_array_index = self.find_array_index(x,y)[1]
        print("Clicked on: ")
        print(f"X in array index: {self.x_array_index}, Y in array index: {self.y_array_index}")


    def find_other_player(self):
        '''
            Method -- find_other_player
                Find the other player, based on what the 
                current player is
            Parameters:
                self -- the current Gamestate object
            Returns:
                None.
        '''
        if self.current_player == "black":
            self.other_player = "crimson"
        else:
            self.other_player = "black"
        
        print("The current player is currently {}.".format(self.current_player)) 
        print("The other player is currently {}.".format(self.other_player))



    def check_boundaries(self,x,y):
        '''
            Method -- check_boundaries
                Returns a Boolean by checking if the x,y array indexes exceed 
                the boundaries(length) of the positions array.
            Parameters:
                self -- the current Gamestate object
                x -- The x array index
                y -- The y array index
            Returns:
                True if x,y in the array index restrictions, else False
        '''
        if x < 0 or x > 7 or y < 0 or y >7:
            return False

        return True


    def find_all_moves(self):
        '''
            Method -- find_all_moves
                Find all_possible_moves for the current player
            Parameters:
                self -- the current Gamestate object
            Returns:
                None. But creates two new attributes:
                all_possible_moves -- Array of Move objects
                all_possible_capture_moves -- Array of Move objects
        '''

        # define the other player
        self.find_other_player()
        all_possible_moves = []
        all_possible_capture_moves = []

        for row in range(len(self.positions)):
            for col in range(len(self.positions[row])):
                
                piece = self.positions[row][col]
                if piece != "empty":
                    if piece.color == self.current_player:
                         # iterate through all the pieces (directions list)
                         directions_list = piece.directions
                         
                         for directions in directions_list:
                            
                            move_row = row + directions[0]
                            move_col = col + directions[1]
                            
                            # If move_row and move_col is on the board
                            if self.check_boundaries(move_row,move_col):
                                possible_move = self.positions[move_row][move_col]

                            # Two scenarions
                            # 1 if empty
                                if possible_move == "empty": 
                                    all_possible_moves.append(Move(start = [row,col],end = [move_row,move_col],capture_status = False))
                            # 2 if contains an enemy piece
                                elif possible_move.color == self.other_player:
                                    # check if its a capturing move by checking if the next square is empty in the same direction
                                    capture_move_row = move_row + directions[0]
                                    capture_move_col = move_col + directions[1]
                                    # check the bounds of the capture move
                                    if self.check_boundaries(capture_move_row,capture_move_col):
                                        # check if it is empty
                                        capture_piece = self.positions[capture_move_row][capture_move_col]
                                        if capture_piece == "empty":
                                            captured_move = Move(start = [row,col], end = [capture_move_row,capture_move_col],capture_status = True)
                                            
                                            # add captured indexes to he Move object
                                            captured_move.add_captured_indexes(move_row,move_col)
                                            
                                            # append to the possible_capture_moves array
                                            all_possible_capture_moves.append(captured_move)
                            

        
        self.all_possible_moves = all_possible_moves
        self.all_possible_capture_moves = all_possible_capture_moves
    

    def check_end_game(self):
        '''
            Method -- check_end_game
                Check if there are still enemy pieces
                on the board
            Parameters:
                self -- the current Gamestate object 
            Returns:
                None.
                If game ended, declare self.game_end to True
                and self.winner is the current player
        '''

        status = True # assume game ended

        for row in range(len(self.positions)):
            for col in range(len(self.positions[row])):
                piece = self.positions[row][col]
                if piece == "empty":
                    continue
                elif piece.color == self.other_player:
                    # there are still enemies
                    status = False # game hasn't ended
                    break

        if status == True:
            self.game_end = True
            self.winner = self.current_player



    def check_any_moves_left(self):
        '''
            Method -- check_any_moves_left
                Check if there are still any moves that
                can be made by the current player, if no,
                the winner is the other player
            Parameters:
                self -- the current Gamestate object 
            Returns:
                None.
                If game ended, declare self.game_end to True
                and self.winner is the other player (enemy)
        '''
        condition1 = len(self.all_possible_moves) == 0
        condition2 = len(self.all_possible_capture_moves) == 0
        if condition1 and condition2:
            self.game_end = True
            self.winner = self.other_player


    def print_moves(self,move_object_array,adjective):
        '''
            Method -- print_moves
                Print an array out for debugging
                This is an internal method.
            Parameters:
                self -- the current Gamestate object
                move_object_array -- An array with Move objects
                adjective - An adjective to describe the move_object_array
            Returns:
                None.
        '''
        print(f"Total of {len(move_object_array)} moves. ({adjective})")
        for move in move_object_array:
            print(f"Start: {move.start}. End: {move.end}. Capture Status: {move.capture_status}")
        print("\n")



    def check_capture(self,possible_moves_for_this_step):
        '''
            Method -- check_capture
                Check if there exists a capture move in possible moves
                for the current step, if there is, then we take it out,
                and append it to another array. (If there is a capture
                move, we must take it)
            Parameters:
                self -- the current Gamestate object
                possible_moves_for_this_step -- A array with Move objects
            Returns:
                output -- After filtering, we return the correct possible
                moves for this step.
        '''
        output = []
        possible_moves_truth = list(map(lambda x: x.capture_status == True, possible_moves_for_this_step))
        if True in possible_moves_truth:
            for index in range(len(possible_moves_for_this_step)):
                if possible_moves_truth[index] == True:
                    output.append(possible_moves_for_this_step[index])
        else:
            output = possible_moves_for_this_step

        return output


    def get_possible_moves_for_step(self):
        '''
            Method -- get_possible_moves_for_step
                Based on all_possible_moves, first check if there are possible capture
                moves,if there are possible capture moves, then possible_moves_for_this_step
                can only be capture moves. If there isn't a capture move to be taken, 
                get the possible moves for this click (step)
            Parameters:
                self -- the current Gamestate object
            Returns:
                None.
                After filtering, append possible moves for this step to history possible 
                routes array
        '''
        if len(self.all_possible_capture_moves) > 0:
            possible_moves_for_this_step = self.all_possible_capture_moves
        else:
            possible_moves_for_this_step = []
            if self.current_player == "black":
                target = [self.x_array_index, self.y_array_index]            
                for possible_move in self.all_possible_moves:
                    if possible_move.start == target:
                        possible_moves_for_this_step.append(possible_move)
            else:
                possible_moves_for_this_step = self.all_possible_moves

        self.print_moves(possible_moves_for_this_step, "Possible moves for this step")
        possible_moves_for_this_step = self.check_capture(possible_moves_for_this_step)
        
        print("Check if capture is inside possible moves for this step... (Modified) ")
        self.print_moves(possible_moves_for_this_step, "Possible moves for this step")
        
        self.history_possible_routes.append(possible_moves_for_this_step)
        self.possible_moves_for_this_step = possible_moves_for_this_step



    ########################  outline_possible_moves_for_step  ##############################

    def adjust_outline(self,color,routes,draw):
        '''
            Method -- adjust_outline
                Given a array with Move objects, we iterate through
                the array, and outline it with the color specified,
                so as to outline possible moves or remove possible 
                moves for this step.
            Parameters:
                self -- The current Gamestate object
                color -- The color of the outline
                routes -- The array with Move objects (history possible route array)
                draw -- A Draw object, to update the UI
            Returns:
                None.
        '''
        for route in routes:
            x_array_index =route.end[0]
            y_array_index = route.end[1]
            x_coordinate, y_coordinate = get_coordinates_given_index(x_array_index,y_array_index)
            draw.set_pen_color(color)
            draw.set_pen_position(x_coordinate,y_coordinate)
            draw.draw_square_outline()
    

    def outline_possible_routes(self,draw):
        '''
            Method -- outline_possible_routes
                Outline the possible routes (steps) for
                this step, and update UI
            Parameters:
                self -- The current Gamestate object
                draw -- A Draw object, to update the UI
            Returns:
                None.
        '''
        # To red
        current_possible_coordinates = self.history_possible_routes[-1]
        # Draw the current possible coordinates blocks to red         
        self.adjust_outline("red",current_possible_coordinates,draw)



    def cover_previous_routes(self,draw):
        '''
            Method -- cover_previous_routes
                Cover up the previous red outline possible 
                routes. (Used when the user clicked on the 
                black chess piece, then clicked again on a
                black chess piece)
            Parameters:
                self -- The current Gamestate object
                draw -- A Draw object, to update the UI
            Returns:
                None.
        '''
        # Redraw all the previous possible coordinates blocks to black
        previous_possible_routes = self.history_possible_routes[:-1]
        self.adjust_outline("black",previous_possible_routes,draw)


    def modify_arrays(self):
        '''
            Method -- modify_arrays
                Modifies the array every step, since we only need
                to keep the last two clicks, and the possible
                routes for the previous step.
            Parameters:
                self -- The current Gamestate object
            Returns:
                None.
        '''
        # delete out all except the last one since we already marked them black
        self.history_possible_routes = self.history_possible_routes[-1]
        # save only leave the last two clicks in the clicked pattern
        self.clicked_pattern = self.clicked_pattern[-2:]
        print("History possible routes: ",self.history_possible_routes)


    # check how to modify this
    def outline_possible_moves_for_step(self,draw):
        '''
            Method -- outline_possible_moves_for_step
                If the user is clicking on its own piece,
                then we cover the previous possible routes,
                and outline the possible routes for this 
                click. Then we modify the array.
            Parameters:
                self -- The current Gamestate object
                draw -- A Draw object, to update the UI
            Returns:
                None.
        '''
        if self.current_player in self.clicked_pattern[-1]:
            # redraw previous possible routes outline to black
            self.cover_previous_routes(draw)
            print("Covered previous possible moves...")
            # draw red outline of current possible routes
            self.outline_possible_routes(draw)
            print("Outlined current possible moves...")
            # modify arrays
            self.modify_arrays()



    ########################  move()  ##############################
    # after clicking an empty piece, we need to remove all previous outlines, and move chess piece

    def remove_all_outlines(self,draw):
        '''
            Method -- remove_all_outlines
                Once we make a move, we outline all the history
                possible routes to black, and return the board
                to normal
            Parameters:
                self -- The current Gamestate object
                draw -- A Draw object, to update the UI
            Returns:
                None.
        '''
        print("Removing all routes: ",self.history_possible_routes)
        self.adjust_outline("black",self.history_possible_routes,draw)


    def clear_arrays(self):
        '''
            Method -- clear_arrays
                Once players switch players, we clear all tracker
                arrays for a new start
            Parameters:
                self -- The current Gamestate object
            Returns:
                None.
        '''
        self.history_possible_routes = []
        self.clicked_coordinates_array_index = [] 
        self.clicked_pattern = []
    

    def update_array_when_move(self,move):
        '''
            Method -- update_array_when_move
                Once we move a chess, we need to update
                the positions array. Update the destination
                to the original piece, and the original place
                to empty if there is a capture, we make the
                captured piece empty also.
            Parameters:
                self -- The current Gamestate object
                move -- A move object
            Returns:
                None.
        '''
        start_x ,start_y = move.start
        end_x, end_y = move.end

        self.positions[end_x][end_y] = self.positions[start_x][start_y]
        self.positions[start_x][start_y] = "empty"

        if move.capture_status == True:
            captured_x, captured_y = move.captured
            self.positions[captured_x][captured_y] = "empty"
            # Add a new condition to check for multiple captures
            self.eliminated_a_piece = True


    def check_if_turn_to_king(self,move,draw):
        '''
            Method -- check_if_turn_to_king
                Check a piece turned into king in this move.
            Parameters:
                self -- The current Gamestate object
                move -- A move object
                draw -- A Draw object
            Returns:
                None.
        '''
        chessboard_top = 0
        chessboard_bottom = len(self.positions)-1

        end_x, end_y = move.end
        moved_piece = self.positions[end_x][end_y]
        print("Moved Piece: ",moved_piece)

        satisfy_black = moved_piece.color == "black" and end_x == chessboard_top
        satisfy_crimson = moved_piece.color == "crimson" and end_x == chessboard_bottom
        
        
        # if black reaches the top or crimson reaches the bottom
        if satisfy_black or satisfy_crimson:
            print("----------- Turned the piece to king -----------")
            # draw the white circle onto the piece
            move.crown_king(draw,self.current_player)
            moved_piece.turn_to_king()
            moved_piece.add_directions(up_left,up_right,down_left,down_right)
            self.print_positions_array()

        # if it is already king
        if moved_piece.king_status == True:
            move.crown_king(draw,self.current_player)



    def get_multi_capture_moves(self,confirmed_move):
        '''
            Method -- get_multi_capture_moves
                Get multiple capture moves for a capture step.
            Parameters:
                self -- The current Gamestate object
                confirmed_move -- Check if there is a multiple
                capture move from a confirmed move.
            Returns:
                An array of move objects.
        '''
        multi_capture_moves = []
        
        end_x, end_y = confirmed_move.end
        chess = self.positions[end_x][end_y]

        directions = chess.directions
        
        for direction in directions:
            
            dx = direction[0]
            dy = direction[1]

            captured_index = (end_x + dx, end_y + dy)
            landing_index = (end_x + dx*2, end_y + dy*2)
            print("Check capture: (captured_index) ",captured_index)
            print("Check capture: (landing_index)",landing_index)

            if self.check_boundaries(captured_index[0],captured_index[1]) and \
                self.check_boundaries(landing_index[0],landing_index[1]):

                captured_piece = self.positions[captured_index[0]][captured_index[1]]
                landing_piece = self.positions[landing_index[0]][landing_index[1]]

                if type(captured_piece)!= str and captured_piece.color == self.other_player \
                    and type(landing_piece)== str and landing_piece == "empty":

                    print("There exists a multiple capture move.")
                    move = Move(start = [end_x,end_y],end = [landing_index[0],landing_index[1]],capture_status = True)
                    move.add_captured_indexes(captured_index[0],captured_index[1])
                    multi_capture_moves.append(move)
        
        return multi_capture_moves


    def check_multiple_capture(self,confirmed_move,draw):
        '''
            Method -- check_multiple_capture
                Returns True or False if there exists a multiple
                capture move
            Parameters:
                self -- The current Gamestate object
                confirmed_move -- Check if there is a multiple
                draw -- A Draw object
            Returns:
                Boolean.
        '''
        if self.eliminated_a_piece:
            print("Checking for multiple captures ...")
            
            multi_capture_moves = self.get_multi_capture_moves(confirmed_move)
            
            # if there is a multiple capture
            if len(multi_capture_moves) > 0:
                # if the current_player is black, let the player choose
                if self.current_player == "black":
                    print("--- Black has multiple capture moves (wait for player to make move)")
                    self.history_possible_routes.append(multi_capture_moves)
                    self.clicked_pattern.append(self.current_player)
                    self.outline_possible_moves_for_step(draw) # draw the possible moves
                    return True

                # if the current_player is computer, the computer can choose
                else:
                    # choose a move by the computer
                    AI_multi_capture = self.random_selection(multi_capture_moves)
                    AI_multi_capture.move_chess(draw,self.current_player)
                    self.update_array_when_move(AI_multi_capture)
                    self.check_if_turn_to_king(AI_multi_capture,draw)
                    self.switch_player(AI_multi_capture,draw)
                    return True
        else:
            return False


    def switch_player(self,confirmed_move,draw):
        '''
            Method -- switch_player
                If there is a multiple capture move, we need to 
                switch turns, which involves: check if the game
                ended,changing the current player, clearing all 
                tracker arrays. If the switched player is the AI,
                then we call self.AI()
            Parameters:
                self -- The current Gamestate object
                confirmed_move -- Check if there is a multiple
                draw -- A Draw object
            Returns:
                None.
        '''
        # if no multiple captures
        if not self.check_multiple_capture(confirmed_move,draw):
            # check if there are any enemy pieces left first,to determine if game should end
            print("Checking if there are any enemy pieces left")
            self.check_end_game()
            self.declare_winner(draw)
            
            # switch player
            self.current_player = self.other_player
            print("Changed the current player to: ", self.current_player)
            # Clear all arrays
            self.clear_arrays()
            print("Cleared all arrays ...")
            # Reset it to False          
            self.eliminated_a_piece = False 
            print("---------------------------- Change Turns --------------------------------------------")
            
            if self.current_player == "crimson" and not self.game_end:
                # Ai makes move
                self.screen.ontimer(self.AI(draw),1000)


    def find_move(self):
        '''
            Method -- find_move
                Find the move for this click amongst all possible
                moves for this step. If this click exists in the 
                possible moves array, then we make it confirm move.
                Else it remains None.
                
                Checking conditions:
                if the last two clicks consecutively in self.clicked_pattern are:
                1. a players chess + empty click
                2. The previous click is Move.start
                3. The current click is in one of the possible_route_coordinates
                   Move object, and the Move.end is this click
            
            Parameters:
                self -- The current Gamestate object
            Returns:
                The confirmed move of the click
        '''
        confirmed_move = None
        if self.clicked_pattern[-2:] == [self.current_player,"empty"]:
            print("Yes, the user has now first clicked on chess piece, then empty space.")
            # for possible_move in self.history_possible_routes:
            for possible_move in self.possible_moves_for_this_step:
                if possible_move.end == [self.x_array_index,self.y_array_index]:
                    if possible_move.start == self.clicked_coordinates_array_index[-2]:
                        confirmed_move = possible_move
                        print("This move is valid, and we found it from the history_possible_routes array! ")
                        break
        return confirmed_move


    def move(self, draw):
        
        '''
            Method -- move
                If the move is a valid move: (find using find_move())
                    1. move the piece using the Move.move_chess
                    2. update the positions array
                    3. check if the piece is now king
                    4. Remove all possible routes outlines
                    5. switch player to other player
                Else:
                    print("This is not a valid move.")
            Parameters:
                self -- The current Gamestate object
                draw -- A Draw object
            Returns:
                None.
        '''        
        confirmed_move = self.find_move()
        if confirmed_move != None:
            # now we have a confirmed move
            print("Confirmed Move: ",confirmed_move)
            confirmed_move.move_chess(draw,self.current_player)
            # udpate positions array
            self.update_array_when_move(confirmed_move)
            # check if turn to king
            self.check_if_turn_to_king(confirmed_move,draw)
            # remove all red outlines
            self.remove_all_outlines(draw)
            # switch player
            self.switch_player(confirmed_move,draw)

        else:
            print("This is not a valid move.")


    def print_tracker_arrays(self):
        '''
            Method -- print_tracker_arrays
                Print tracker arrays to the terminal
            Parameters:
                self -- The current Gamestate object
            Returns:
                None.
        '''
        print("Clicked coordinated array index:",self.clicked_coordinates_array_index)
        print("Clicked Pattern",self.clicked_pattern)


    ########################  Main process used in click handler  ##############################

    def process(self,x,y,draw):
        '''
            Method -- process
                The main process used in the click handler function in Setup.
                Three scenarios:
                    1. The user clicks on a black piece
                    2. The user clicks on an empty piece
                    3. Neither
            Parameters:
                self -- The current Gamestate object
                x -- The clicked x coordinate
                y -- The clicked y coordinate
                draw -- The Draw object
            Returns:
                None.
        '''

        # Upon click, identify x_corner,y_corner,x_array_index,y_array_index
        self.identify_corner(x,y)
        # append to the clicked_coordinates list for tracking
        self.clicked_coordinates_array_index.append([self.x_array_index,self.y_array_index])
        # Get the clicked chess piece from the self.positions array (A Piece Object)
        self.clicked_chess = self.positions[self.x_array_index][self.y_array_index]

        if self.current_player == "black" and self.clicked_chess == "empty":
            print("Player clicked on an empty piece.")
            self.clicked_pattern.append("empty")
            self.move(draw)



        elif self.current_player == "black" and self.current_player == self.clicked_chess.color:
            print("Player clicked on its own piece.")
            self.clicked_pattern.append(self.current_player)
            # find all possible moves for the current player
            self.find_all_moves()
            self.check_any_moves_left()
            self.declare_winner(draw)
            # printing all possible moves onto the chessboard
            self.print_moves(self.all_possible_moves,"all possible moves")
            self.print_moves(self.all_possible_capture_moves,"all possible capture moves")
            # get possible moves for this current click
            self.get_possible_moves_for_step()
            self.outline_possible_moves_for_step(draw)

        else:
            print("You can't move another Person's chess")
    

    def print_positions_array(self):
        '''
            Method -- print_positions_array
                Print the current state of the positions array
                print the color, whether the piece is king, and the length
                of the directions attribute
            Parameters:
                self -- The current Gamestate object
            Returns:
                None.
        '''
        for chess_row in self.positions:
            for item in chess_row:
                if item == "empty":
                    print("empty",end=",")
                else:
                    print("["+item.color + "/" + str(item.king_status)+"/"+str(len(item.directions))+"]", end = ",")
            print("\n")


    # @helper function for AI
    def random_selection(self,ls):
        '''
            Method -- random_selection
                Randomly select an item from a list
            Parameters:
                self -- The current Gamestate object
                ls -- The list to select from
            Returns:
                A random object from the list
        '''
        random_number = random.randint(0,len(ls)-1)
        return ls[random_number]


    def AI(self,draw):
        '''
            Method -- AI
                The AI implementation of the game.
                Functionalities -- 
                1. find_all_moves()
                2. get_possible_moves_for_step()   -- saved in history_possible_routes
                3. outline possible_moves_for_step()
                4. randomly select a move (a move object) inside the history possible routes array (this is now the     confirmed_move)
                5. self.update_array_when_move(confirmed_move)
                6. self.check_if_turn_to_king(confirmed_move,draw) (# check if turn to king)
                7. self.remove_all_outlines(draw)
                8. self.switch_player(move,draw)
            Parameters:
                self -- The current Gamestate object
                draw -- A Draw object to update the UI
            Returns:
                None.
        '''
        # Click on a chess piece / wait 1000 milliseconds
        print("Computer (AI) clicked on a piece....")
        #self.screen.ontimer(self.clicked_pattern.append(self.current_player),1000)
        self.clicked_pattern.append(self.current_player) 
        # find all moves of crimson
        print("Computer (AI) finding all moves....")
        self.find_all_moves()
        self.check_any_moves_left()
        self.declare_winner(draw)
        self.print_moves(self.all_possible_moves,"all possible moves")
        self.print_moves(self.all_possible_capture_moves,"all possible capture moves")
        self.get_possible_moves_for_step()
        print("Computer outlining possible moves....")
        # self.outline_possible_moves_for_step(draw)
        AI_selected_move = self.random_selection(self.possible_moves_for_this_step)
        print("Computer (AI) clicked on an empty piece. (selected a move)")
        self.clicked_pattern.append("empty")
        print(AI_selected_move)
        # do the actual UI / move chess
        print("Computer(AI) moves piece")
        AI_selected_move.move_chess(draw,self.current_player) 
        # updating positions array
        self.update_array_when_move(AI_selected_move)
        self.check_if_turn_to_king(AI_selected_move,draw)
        self.switch_player(AI_selected_move,draw)


    def declare_winner(self,draw):
        '''
            Method -- declare_winner
                Declare the winner if the game ends.
            Parameters:
                self -- The current Gamestate object
                draw -- The Draw object to update the UI.
            Returns:
                None.
        '''
        if self.game_end == True:
            print(f"The winner is {self.winner}.")
            # display game winner on UI
            if self.winner == "black":
                winner = "You"
            else:
                winner = "Computer"
            draw.game_winner(winner)



