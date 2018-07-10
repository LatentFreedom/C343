from utilities import *

def flood(color_of_tile, flooded_list, screen_size):
    for coord in flooded_list:
        if in_bounds(right(coord), screen_size):
            if color_of_tile[coord] == color_of_tile[right(coord)]:
                if right(coord) not in flooded_list:
                    flooded_list.append(right(coord))
        if in_bounds(left(coord), screen_size):
            if color_of_tile[coord] == color_of_tile[left(coord)]:
                if left(coord) not in flooded_list:
                    flooded_list.append(left(coord))
        if in_bounds(up(coord), screen_size):
            if color_of_tile[coord] == color_of_tile[up(coord)]:
                if up(coord) not in flooded_list:
                    flooded_list.append(up(coord))
        if in_bounds(down(coord), screen_size):
            if color_of_tile[coord] == color_of_tile[down(coord)]:
                if down(coord) not in flooded_list:
                    flooded_list.append(down(coord))
