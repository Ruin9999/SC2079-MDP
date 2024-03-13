import Constants

def is_valid_coord(x : int, y : int):
    return x >= 1 and x < Constants.WIDTH  and y >= 1 and y < Constants.HEIGHT