from move import Move



def test_add_captured_indexes():
    
    move1 = Move(start = [0,0], end = [2,2], capture_status=False)
    move1.add_captured_indexes(1,1)
    assert(move1.captured == [1,1])

    move2 = Move(start = [7,1], end = [5,3], capture_status=False)
    move2.add_captured_indexes(6,2)
    assert(move2.captured == [6,2])

    move3 = Move(start = [5,3], end = [3,5], capture_status=False)
    move3.add_captured_indexes(4,4)
    assert(move3.captured == [4,4])



