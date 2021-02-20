from constants import up_left, up_right, down_left, down_right
from gamestate import Gamestate
from piece import Piece
from move import Move


def test_get_cell():
    gs = Gamestate()
    assert(gs.get_cell(120) == 6)
    assert(gs.get_cell(157) == 7)
    assert(gs.get_cell(190) == 7) 
    assert(gs.get_cell(200) == 8)  

def test_identify_corner():
    gs = Gamestate()
    
    gs.identify_corner(0,0)
    assert(gs.x_array_index == 3)
    assert(gs.y_array_index == 4)
    
    gs.identify_corner(124,0)
    assert(gs.x_array_index == 3)
    assert(gs.y_array_index == 6)

    gs.identify_corner(111,150)
    assert(gs.x_array_index == 0)
    assert(gs.y_array_index == 6)

    gs.identify_corner(140,120)
    assert(gs.x_array_index == 1)
    assert(gs.y_array_index == 6)


def test_find_other_player():

    gs = Gamestate()
    gs.find_other_player()
    assert(gs.current_player == "black")
    assert(gs.other_player == "crimson")
    
    gs2 = Gamestate(current_player="crimson")
    gs2.find_other_player()
    assert(gs2.current_player == "crimson")
    assert(gs2.other_player == "black")


def test_check_boundaries():
    gs = Gamestate()
    assert(not gs.check_boundaries(8,0))
    assert(not gs.check_boundaries(-1,1))
    assert(not gs.check_boundaries(2,10))
    assert(not gs.check_boundaries(5,-2))
    assert(gs.check_boundaries(5,5))
    assert(gs.check_boundaries(4,3))
    assert(gs.check_boundaries(2,2))


# memory error
def test_find_all_moves():
    gs = Gamestate()
    gs.find_all_moves()
    print(gs.all_possible_moves)
    first_round_possible_moves = [
    Move([5,1],[4,0],False),
    Move([5,1],[4,2],False),
    Move([5,3],[4,2],False),
    Move([5,3],[4,4],False),
    Move([5,5],[4,4],False),
    Move([5,5],[4,6],False),
    Move([5,7],[4,6],False)
    ]

    for p in range(len(gs.all_possible_moves)):
        pp = gs.all_possible_moves[p]
        frpm = first_round_possible_moves[p]
        assert(
            pp.start ==frpm.start and pp.end == frpm.end and pp.capture_status == frpm.capture_status
            )
    assert(gs.all_possible_capture_moves == [])


def test_check_end_game():
    gs = Gamestate()
    gs.find_other_player()
    gs.check_end_game()
    assert(not gs.game_end)
    
    gs2 = Gamestate()
    black = Piece("black",directions= [up_left,up_right], king_status = False)
    test_positions = [
    ["empty",black,"empty",black,"empty",black,"empty",black],
    [black,"empty",black,"empty",black,"empty",black,"empty"]
    ]
    gs2.positions = test_positions
    gs2.find_other_player()
    gs2.check_end_game()
    assert(gs2.game_end)
    assert(gs2.winner == "black")


def test_check_any_moves_left():
    gs = Gamestate()
    gs.all_possible_moves = []
    gs.all_possible_capture_moves = []
    gs.find_other_player()
    gs.check_any_moves_left()
    assert(gs.game_end)
    assert(gs.winner == "crimson")


def test_check_capture():
    gs = Gamestate()


    Move1 = Move([5,3],[3,5],True)
    Move2 = Move([5,1],[4,2],False)
    Move3 = Move([5,7],[4,6],False)
    Move4 = Move([5,3],[4,2],False)
    
    possible_moves1 = [Move1, Move2, Move3]
    possible_moves2 = [Move2, Move3, Move4]
    
    assert(gs.check_capture(possible_moves1) == [Move1])
    assert(gs.check_capture(possible_moves2) == [Move2, Move3, Move4])


def test_modify_arrays():
    gs = Gamestate()
    
    gs.history_possible_routes = [1,2,3,4]
    gs.clicked_pattern = ['a','b','c','d']
    
    gs.modify_arrays()
    assert(gs.history_possible_routes == 4)
    assert(gs.clicked_pattern == ['c','d'])


def test_clear_arrays():
    gs = Gamestate()
    gs.history_possible_routes = [1,2,3,4]
    gs.clicked_coordinates_array_index = [5,6,7,8]
    gs.clicked_pattern = ['a','b','c','d']
    gs.clear_arrays()
    assert(gs.history_possible_routes == [])
    assert(gs.clicked_coordinates_array_index == [])
    assert(gs.clicked_pattern == [])


# associated with memory allocation x test failed
def test_update_array_when_move():
    # case 1
    gs = Gamestate()
    Move1 = Move([5,3],[3,5],True)
    Move1.add_captured_indexes(4,4)
    gs.update_array_when_move(Move1)
    assert(gs.positions[3][5].color == "black")
    assert(gs.positions[3][5].directions == [up_left,up_right])
    assert(gs.positions[3][5].king_status == False)

    assert(gs.positions[5][3] == "empty")
    assert(gs.positions[4][4] == "empty")

    # Case2
    gs2 = Gamestate()
    Move2 = Move([5,1],[4,2],False)
    gs2.update_array_when_move(Move2)
    assert(gs2.positions[5][1] == "empty")
    assert(gs2.positions[4][2].color == "black")
    assert(gs2.positions[4][2].directions == [up_left,up_right])
    assert(gs2.positions[4][2].king_status == False)
    





def test_get_multi_capture_moves():
    gs = Gamestate()
    gs.find_other_player()
    gs.update_array_when_move(Move([5,3],[4,2],False))
    gs.update_array_when_move(Move([2,4],[3,3],False))
    gs.positions[0][6] = "empty"
    confirmed_move = Move([4,2],[2,4],True)
    confirmed_move.add_captured_indexes(3,3)
    # make move
    gs.update_array_when_move(confirmed_move)
    move = gs.get_multi_capture_moves(confirmed_move)[0]
    assert(move.start == [2,4])
    assert(move.end == [0,6])
    assert(move.capture_status == True)



def test_find_move():
    gs = Gamestate()
    gs.clicked_pattern = ["black","empty"]
    gs.x_array_index = 5
    gs.y_array_index = 3
    gs.clicked_coordinates_array_index = [[5,3],[4,4]]
    gs.find_all_moves()
    gs.get_possible_moves_for_step()
    gs.x_array_index = 4
    gs.y_array_index = 4
    found_move = gs.find_move()
    assert(found_move.start == [5,3])
    assert(found_move.end == [4,4])
    assert(found_move.capture_status == False)


def test_random_selection():
    gs = Gamestate()
    ls = [0,1,2,3,4]
    selected = gs.random_selection(ls)
    assert(selected in ls)






































