from constants import SIZE_OF_SQUARE

def get_coordinates_given_index(x_index,y_index):
    '''
        Method -- get_coordinates_given_index
            Given x_index and y_index of the positions array in
            gamestate, we return the bottom left corner coordinates
            of the square

        Parameters:
            x_index -- The x array index in the positions array of the piece
            y_index -- The y array index in the positions array of the piece
    '''
    # x
    x_coordinate = abs(y_index - 4) * SIZE_OF_SQUARE
    
    if y_index <= 4:
        x_coordinate = - x_coordinate

    # y
    y_coordinate = abs(x_index - 3) * SIZE_OF_SQUARE

    if x_index > 3:
        y_coordinate = - y_coordinate
    
    return [x_coordinate,y_coordinate]





