from utilities import *

def flood(color_of_tile, flooded_list, screen_size):
    for coord in flooded_list:
        if in_bounds(right(coord), screen_size) and color_of_tile[coord] == color_of_tile[right(coord)] and right(coord) not in flooded_list:
            flooded_list.append(right(coord))
        if in_bounds(left(coord), screen_size) and color_of_tile[coord] == color_of_tile[left(coord)] and left(coord) not in flooded_list:
            flooded_list.append(left(coord))
        if in_bounds(up(coord), screen_size) and color_of_tile[coord] == color_of_tile[up(coord)] and up(coord) not in flooded_list:
            flooded_list.append(up(coord))
        if in_bounds(down(coord), screen_size) and color_of_tile[coord] == color_of_tile[down(coord)] and down(coord) not in flooded_list:
            flooded_list.append(down(coord))
