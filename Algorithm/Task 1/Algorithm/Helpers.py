import Constants

def is_valid_coord(x : int, y : int):
    return x >= 0 and x < Constants.WIDTH and y >= 0 and y < Constants.HEIGHT