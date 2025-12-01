"""
Environment module for Vacuum Cleaner Robot Simulation
Handles grid world, tile states, and environment logic
"""

import random
from typing import List, Tuple, Set

class TileState:
    """Represents the state of a tile in the environment"""
    CLEAN = 0
    DIRTY = 1
    OBSTACLE = 2

class Environment:
    """Grid environment for vacuum cleaner robot"""
    
    def __init__(self, width: int = 20, height: int = 15, dirt_probability: float = 0.3, obstacle_probability: float = 0.1):
        """
        Initialize the environment
        
        Args:
            width: Grid width
            height: Grid height
            dirt_probability: Probability of a tile being dirty initially
            obstacle_probability: Probability of a tile being an obstacle
        """
        self.width = width
        self.height = height
        self.grid = [[TileState.CLEAN for _ in range(width)] for _ in range(height)]
        self.robot_pos = (0, 0)
        self.total_dirt = 0
        self.cleaned_dirt = 0
        
        # Initialize grid with obstacles and dirt
        self._initialize_grid(dirt_probability, obstacle_probability)
        
    def _initialize_grid(self, dirt_prob: float, obstacle_prob: float):
        """Initialize grid with random dirt and obstacles"""
        for y in range(self.height):
            for x in range(self.width):
                # Skip robot starting position
                if (x, y) == self.robot_pos:
                    continue
                    
                # Place obstacle
                if random.random() < obstacle_prob:
                    self.grid[y][x] = TileState.OBSTACLE
                # Place dirt
                elif random.random() < dirt_prob:
                    self.grid[y][x] = TileState.DIRTY
                    self.total_dirt += 1
    
    def get_tile_state(self, x: int, y: int) -> int:
        """Get the state of a tile"""
        if not self.is_valid_position(x, y):
            return TileState.OBSTACLE
        return self.grid[y][x]
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within grid bounds"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_walkable(self, x: int, y: int) -> bool:
        """Check if position is walkable (not obstacle)"""
        return self.is_valid_position(x, y) and self.grid[y][x] != TileState.OBSTACLE
    
    def move_robot(self, new_x: int, new_y: int) -> bool:
        """
        Move robot to new position if valid
        
        Returns:
            True if move was successful, False otherwise
        """
        if self.is_walkable(new_x, new_y):
            self.robot_pos = (new_x, new_y)
            return True
        return False
    
    def clean_current_tile(self) -> bool:
        """
        Clean the tile at robot's current position
        
        Returns:
            True if tile was dirty and is now clean, False otherwise
        """
        x, y = self.robot_pos
        if self.grid[y][x] == TileState.DIRTY:
            self.grid[y][x] = TileState.CLEAN
            self.cleaned_dirt += 1
            return True
        return False
    
    def get_dirty_tiles(self) -> List[Tuple[int, int]]:
        """Get list of all dirty tile positions"""
        dirty_tiles = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == TileState.DIRTY:
                    dirty_tiles.append((x, y))
        return dirty_tiles
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get valid neighboring positions (4-directional)"""
        neighbors = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_walkable(nx, ny):
                neighbors.append((nx, ny))
        
        return neighbors
    
    def is_all_clean(self) -> bool:
        """Check if all tiles are clean"""
        return self.cleaned_dirt >= self.total_dirt
    
    def get_cleanliness_percentage(self) -> float:
        """Get percentage of cleaned tiles"""
        if self.total_dirt == 0:
            return 100.0
        return (self.cleaned_dirt / self.total_dirt) * 100
    
    def reset(self):
        """Reset environment to initial state"""
        self.__init__(self.width, self.height)
