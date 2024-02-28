import Constants

def is_valid_coord(x : int, y : int):
    return x >= 1 and x < Constants.WIDTH - 1  and y >= 1 and y < Constants.HEIGHT - 1