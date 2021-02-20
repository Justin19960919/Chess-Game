from helper import get_coordinates_given_index



def test_get_coordinated_given_index():
	assert(get_coordinates_given_index(0,0) ==[-200, 150])
	assert(get_coordinates_given_index(1,1) ==[-150, 100])
	assert(get_coordinates_given_index(2,0) ==[-200, 50])
	assert(get_coordinates_given_index(5,1) ==[-150, -100])
	assert(get_coordinates_given_index(5,5) ==[50, -100])
	assert(get_coordinates_given_index(3,4) ==[0, 0])