from typing import List

import Constants
from Cell import Cell
from Direction import Direction
from Helpers import is_valid_coord

class Obstacle(Cell):
    def __init__(self, x : int, y : int, direction : Direction , obstacle_id : int):
        super().__init__(x, y, direction)
        self.obstacle_id = obstacle_id

    def get_view_state(self) -> List[Cell]:
        cells = []

        if self.direction == Direction.NORTH:
            if is_valid_coord(self.x, self.y + 1 + Constants.EXPANDED_CELL * 2):
                cells.append(Cell(self.y, self.y + 1 + Constants.EXPANDED_CELL * 2, Direction.SOUTH, self.obstacle_id, 5))
            if is_valid_coord(self.x, self.y + 2 + Constants.EXPANDED_CELL * 2):
                cells.append(Cell(self.y, self.y + 2 + Constants.EXPANDED_CELL * 2, Direction.SOUTH, self.obstacle_id, 0))
            if is_valid_coord(self.x + 1, self.y + 2 + Constants.EXPANDED_CELL * 2):
                cells.append(Cell(self.y + 1, self.y + 2 + Constants.EXPANDED_CELL * 2, Direction.SOUTH, self.obstacle_id, Constants.SCREENSHOT_COST))
            if is_valid_coord(self.x - 1, self.y + 2 + Constants.EXPANDED_CELL * 2):
                cells.append(Cell(self.x - 1, self.y + 2 + Constants.EXPANDED_CELL * 2, Direction.SOUTH, self.obstacle_id, Constants.SCREENSHOT_COST))

        elif self.direction == Direction.SOUTH:
            if is_valid_coord(self.x, self.y - 1 - Constants.EXPANDED_CELL * 2):
                cells.append(Cell(self.x, self.y - 1 - Constants.EXPANDED_CELL * 2, Direction.NORTH, self.obstacle_id, 5))
            if is_valid_coord(self.x, self.y - 2 - Constants.EXPANDED_CELL * 2):
                cells.append(Cell(self.x, self.y - 2 - Constants.EXPANDED_CELL * 2, Direction.NORTH, self.obstacle_id, 0))
            if is_valid_coord(self.x - 1, self.y - 2 - Constants.EXPANDED_CELL * 2):
                cells.append(Cell(self.x - 1, self.y - 2 - Constants.EXPANDED_CELL * 2, Direction.NORTH, self.obstacle_id, Constants.SCREENSHOT_COST))
            if is_valid_coord(self.x + 1, self.y - 2 - Constants.EXPANDED_CELL * 2):
                cells.append(Cell(self.x + 1, self.y - 2 - Constants.EXPANDED_CELL * 2, Direction.NORTH, self.obstacle_id, Constants.SCREENSHOT_COST))

        elif self.direction == Direction.EAST:
            if is_valid_coord(self.x + 1 + Constants.EXPANDED_CELL * 2, self.y):
                cells.append(Cell(self.x + 1 + Constants.EXPANDED_CELL * 2, self.y, Direction.WEST, self.obstacle_id, 5))
            if is_valid_coord(self.x + 2 + Constants.EXPANDED_CELL * 2, self.y):
                cells.append(Cell(self.x + 2 + Constants.EXPANDED_CELL * 2, self.y, Direction.WEST, self.obstacle_id, 0))
            if is_valid_coord(self.x + 2 + Constants.EXPANDED_CELL * 2, self.y - 1):
                cells.append(Cell(self.x + 2 + Constants.EXPANDED_CELL * 2, self.y - 1, Direction.WEST, self.obstacle_id, Constants.SCREENSHOT_COST))
            if is_valid_coord(self.x + 2 + Constants.EXPANDED_CELL * 2, self.y + 1):
                cells.append(Cell(self.x + 2 + Constants.EXPANDED_CELL * 2, self.y + 1, Direction.WEST, self.obstacle_id, Constants.SCREENSHOT_COST))

        elif self.direction == Direction.WEST:
            if is_valid_coord(self.x - 1 - Constants.EXPANDED_CELL * 2, self.y):
                cells.append(Cell(self.x - 1 - Constants.EXPANDED_CELL * 2, self.y, Direction.EAST, self.obstacle_id, 5))
            if is_valid_coord(self.x - 2 - Constants.EXPANDED_CELL * 2, self.y):
                cells.append(Cell(self.x - 2 - Constants.EXPANDED_CELL * 2, self.y, Direction.EAST, self.obstacle_id, 0))
            if is_valid_coord(Cell(self.x - 2 - Constants.EXPANDED_CELL * 2, self.y - 1)):
                cells.append(Cell(self.x - 2 - Constants.EXPANDED_CELL * 2, self.y - 1, Direction.EAST, self.obstacle_id, Constants.SCREENSHOT_COST))
            if is_valid_coord(Cell(self.x - 2 - Constants.EXPANDED_CELL * 2, self.y + 1)):
                cells.append(Cell(self.x - 2 - Constants.EXPANDED_CELL * 2, self.y + 1, Direction.EAST, self.obstacle_id, Constants.SCREENSHOT_COST))
        
        return cells