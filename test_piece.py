from piece import Piece
from constants import up_left,up_right,down_left,down_right

def test_add_directions():
	
	piece1 = Piece("black",[up_left,up_right],False)
	piece1.add_directions(up_left,up_right,down_left,down_right)
	assert(piece1.directions == [up_left,up_right,down_left,down_right])

	piece2 = Piece("crimson",[down_left,down_right],False)
	piece2.add_directions(up_left,up_right,down_left,down_right)
	assert(piece2.directions == [down_left,down_right,up_left,up_right])


def test_turn_to_king():
	piece1 = Piece("black",[up_left,up_right],False)
	piece1.turn_to_king()
	assert(piece1.king_status)

	piece2 = Piece("crimson",[down_left,down_right],False)
	assert(not piece2.king_status)
