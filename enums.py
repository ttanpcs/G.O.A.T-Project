from enum import Enum

class TileType(Enum):
    NO_TILE = 1
    BLACK_TILE = 2
    WHITE_TILE = 3

class ChangeType(Enum):
    VALID_CHANGE = 1
    INVALID_CHANGE = 2
    NEEDS_TILE_REMOVED = 3
    NO_CHANGE = 4
